import os

# Import all processing modules
from models.csv_model import process_csv
from models.pdf_model import process_pdf
from models.image_model import process_image
from models.handwritten_model import process_handwritten


def detect_file_type(file_path):
    ext = os.path.splitext(file_path)[1].lower()

    if ext in [".csv", ".xlsx"]:
        return "csv"
    elif ext in [".pdf"]:
        return "pdf"
    elif ext in [".png", ".jpg", ".jpeg"]:
        return "image"
    elif ext in [".txt"]:
        return "text"
    else:
        return "unknown"


def process_file(file_path):
    file_type = detect_file_type(file_path)

    if file_type == "csv":
        return process_csv(file_path)

    elif file_type == "pdf":
        return process_pdf(file_path)

    elif file_type == "image":
        return process_image(file_path)

    elif file_type == "text":
        return process_handwritten(file_path)

    else:
        return {
            "status": "error",
            "message": "Unsupported file type"
        }