import pytesseract
import cv2
import re
import os
# Try to set Tesseract path
# Note: The installer at C:\Users\Admin\Downloads\tesseract-ocr-w64-setup-5.5.0.20241111.exe
# will install Tesseract to C:\Program Files\Tesseract-OCR\tesseract.exe
TESSERACT_PATHS = [
    r'C:\Program Files\Tesseract-OCR\tesseract.exe',  # 64-bit default installation
    r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe',  # 32-bit alternative
    '/usr/bin/tesseract',  # Linux
    '/usr/local/bin/tesseract'  # macOS
]

for path in TESSERACT_PATHS:
    if os.path.exists(path):
        pytesseract.pytesseract.tesseract_cmd = path
        break

OUTPUT_FOLDER = os.path.join(os.getcwd(), "data", "processed")
os.makedirs(OUTPUT_FOLDER, exist_ok=True)


def preprocess_image(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.medianBlur(gray, 3)
    thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)[1]
    return thresh


def extract_text(image):
    try:
        return pytesseract.image_to_string(image)
    except Exception as e:
        raise Exception(f"Tesseract OCR error: {str(e)}. Please install Tesseract from https://github.com/UB-Mannheim/tesseract/wiki")


def clean_text(text):
    return re.sub(r'\s+', ' ', text).strip()


def save_text(text, filename="image_output.txt"):
    path = os.path.join(OUTPUT_FOLDER, filename)

    with open(path, "w", encoding="utf-8") as f:
        f.write(text)

    return path


def process_image(file_path):
    try:
        image = cv2.imread(file_path)

        if image is None:
            return {
                "status": "error",
                "message": "Invalid image file or unsupported format"
            }

        processed = preprocess_image(image)
        raw_text = extract_text(processed)
        cleaned_text = clean_text(raw_text)

        if not cleaned_text:
            return {
                "status": "error",
                "message": "No text detected in image"
            }

        saved_file = save_text(cleaned_text)

        return {
            "status": "success",
            "data": {
                "extracted_text": cleaned_text,
                "length": len(cleaned_text)
            },
            "output_file": saved_file,
            "message": "Image OCR processed successfully"
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }

        if not cleaned_text:
            return {
                "status": "error",
                "message": "No text detected in image"
            }

        saved_file = save_text(cleaned_text)

        return {
            "status": "success",
            "data": {
                "extracted_text": cleaned_text,
                "length": len(cleaned_text)
            },
            "output_file": saved_file,
            "message": "Image OCR processed successfully"
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }