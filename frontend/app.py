import gradio as gr
import requests

API_URL = "http://127.0.0.1:8000/process"


def process_file(file):
    try:
        with open(file.name, "rb") as f:
            response = requests.post(API_URL, files={"file": f})

        result = response.json()

        if result["status"] == "success":
            output = f"✅ {result['message']}\n\n"

            # CSV
            if "summary" in result:
                output += f"📊 Summary:\n{result['summary']}\n\n"

            # Text outputs (PDF/Image)
            if "data" in result:
                output += f"📄 Data:\n{result['data']}\n\n"

            # Visualizations
            visuals = result.get("visualizations", [])
            return output, visuals

        else:
            return f"❌ Error: {result['message']}", []

    except Exception as e:
        return f"❌ Failed: {str(e)}", []


# UI
with gr.Blocks() as app:
    gr.Markdown("# 🚀 DataVerse - AI Data Preprocessing System")

    file_input = gr.File(label="Upload your file (CSV / PDF / Image)")
    output_text = gr.Textbox(label="Result", lines=15)
    gallery = gr.Gallery(label="Visual Reports")

    btn = gr.Button("Process")

    btn.click(
        fn=process_file,
        inputs=file_input,
        outputs=[output_text, gallery]
    )

app.launch()