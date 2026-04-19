import gradio as gr
import requests
import os
from pathlib import Path

API_URL = "http://127.0.0.1:8000/process"
REQUEST_TIMEOUT = 30  # seconds


def check_backend():
    """Check if backend is running"""
    try:
        response = requests.get("http://127.0.0.1:8000/", timeout=2)
        return response.status_code == 200
    except:
        return False


# -------- FORMATTERS --------
def format_summary(summary):
    lines = []
    for key, value in summary.items():
        key_clean = key.replace("_", " ").title()
        lines.append(f"{key_clean}: {value}")
    return "\n".join(lines)


def format_data_preview(data):
    try:
        preview_lines = []
        for key, values in data.items():
            vals = list(values.values())[:5]
            preview_lines.append(f"{key}: {vals}")
        return "\n".join(preview_lines)
    except:
        return str(data)[:800]


# -------- MAIN FUNCTION --------
def process_file(file):
    if file is None:
        return "ERROR\n" + "-"*30 + "\nNo file selected. Please upload a file.", []
    
    # Check if backend is running
    if not check_backend():
        return "ERROR\n" + "-"*30 + "\nBackend server not running. Start it with:\nuvicorn backend.main:app --reload", []
    
    try:
        with open(file.name, "rb") as f:
            response = requests.post(API_URL, files={"file": f}, timeout=REQUEST_TIMEOUT)

        result = response.json()

        if result.get("status") == "success":

            output = "PROCESSING REPORT\n"
            output += "=" * 50 + "\n\n"

            # Summary
            if "summary" in result:
                output += "DATA SUMMARY\n"
                output += "-" * 30 + "\n"
                output += format_summary(result["summary"]) + "\n\n"

            # Data Preview
            if "data" in result:
                output += "DATA PREVIEW\n"
                output += "-" * 30 + "\n"
                output += format_data_preview(result["data"]) + "\n\n"

            # Status
            output += "STATUS\n"
            output += "-" * 30 + "\n"
            output += f"{result.get('message', '')}\n"

            # Visuals - convert relative paths to absolute
            visuals = result.get("visualizations", [])
            valid_visuals = []
            for img_path in visuals:
                # Handle both relative and absolute paths
                if not os.path.isabs(img_path):
                    abs_path = os.path.join(os.getcwd(), img_path)
                else:
                    abs_path = img_path
                
                if os.path.exists(abs_path):
                    valid_visuals.append(abs_path)
                else:
                    output += f"\n⚠️ Warning: Visualization not found at {abs_path}"

            return output, valid_visuals

        else:
            error_msg = result.get('message', 'Unknown error')
            return f"ERROR\n{'-'*30}\n{error_msg}", []

    except requests.exceptions.Timeout:
        return f"ERROR\n{'-'*30}\nRequest timed out. Backend may be slow or unresponsive.", []
    except requests.exceptions.ConnectionError:
        return f"ERROR\n{'-'*30}\nCannot connect to backend. Make sure it's running on http://127.0.0.1:8000", []
    except Exception as e:
        return f"ERROR\n{'-'*30}\n{str(e)}", []


# -------- UI --------
custom_css = """
body {
    font-family: Arial, sans-serif;
}

.gradio-container {
    max-width: 1100px;
    margin: auto;
}

h1 {
    text-align: center;
}

.section {
    margin-top: 20px;
}
"""


with gr.Blocks() as app:

    gr.Markdown("# DataVerse")
    gr.Markdown("AI-Based Data Preprocessing and Analysis System")

    with gr.Row():
        with gr.Column(scale=1):
            gr.Markdown("### Input")
            file_input = gr.File(label="Upload file")

            process_btn = gr.Button("Run Processing")

        with gr.Column(scale=2):
            gr.Markdown("### Output Report")
            output_text = gr.Textbox(label="Processing Report", lines=20)

    gr.Markdown("### Visual Analytics")
    gallery = gr.Gallery(columns=3, height="auto")

    process_btn.click(
        fn=process_file,
        inputs=file_input,
        outputs=[output_text, gallery]
    )

app.launch(theme=gr.themes.Base(), css=custom_css)