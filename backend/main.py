from fastapi import FastAPI, UploadFile, File
import os
from backend.services.ai_agent import detect_file_type, process_file

app = FastAPI()

# Folder to store uploaded files
UPLOAD_FOLDER = "data/raw"

# Ensure folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.get("/")
def home():
    return {"message": "DataVerse API is running"}


# 🔹 Upload only (classification)
@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    try:
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)

        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)

        file_type = detect_file_type(file_path)

        return {
            "filename": file.filename,
            "type": file_type,
            "message": "File uploaded and classified successfully",
            "path": file_path
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }


# 🔹 Upload + Process (main pipeline)
@app.post("/process")
async def process_uploaded_file(file: UploadFile = File(...)):
    try:
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)

        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)

        result = process_file(file_path)

        return result

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }