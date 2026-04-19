from models.image_model import process_image

def process_handwritten(file_path):
    """
    Reuse image OCR pipeline for handwritten text.
    """
    return process_image(file_path)