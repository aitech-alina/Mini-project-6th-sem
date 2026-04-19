from fastapi import FastAPI, UploadFile, File
import os

app = FastAPI()

UPLOAD_FOLDER = "data/raw"

# Ensure folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.get("/")
def home():
    return {"message": "DataVerse API is running"}


@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)

    with open(file_path, "wb") as f:
        content = await file.read()
        f.write(content)

    return {
        "filename": file.filename,
        "message": "File uploaded successfully",
        "path": file_path
    }