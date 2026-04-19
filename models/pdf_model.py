import PyPDF2
import re
import os

OUTPUT_FOLDER = os.path.join(os.getcwd(), "data", "processed")
os.makedirs(OUTPUT_FOLDER, exist_ok=True)


def extract_text_from_pdf(file_path):
    text = ""

    try:
        with open(file_path, "rb") as file:
            reader = PyPDF2.PdfReader(file)

            for page in reader.pages:
                try:
                    extracted = page.extract_text()
                    if extracted:
                        text += extracted + " "
                except Exception as e:
                    continue  # Skip problematic pages

    except Exception as e:
        raise Exception(f"Error reading PDF: {str(e)}")

    return text


def clean_text(text):
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


def save_text(text, filename="pdf_output.txt"):
    path = os.path.join(OUTPUT_FOLDER, filename)

    with open(path, "w", encoding="utf-8") as f:
        f.write(text)

    return path


def process_pdf(file_path):
    try:
        raw_text = extract_text_from_pdf(file_path)

        if not raw_text.strip():
            return {
                "status": "error",
                "message": "No readable text found in PDF"
            }

        cleaned_text = clean_text(raw_text)

        file_path_saved = save_text(cleaned_text)

        return {
            "status": "success",
            "data": {
                "preview": cleaned_text[:500],
                "length": len(cleaned_text)
            },
            "output_file": file_path_saved,
            "message": "PDF processed successfully"
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }