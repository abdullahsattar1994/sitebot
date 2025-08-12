from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import os
import shutil
from typing import List
import requests
import json

app = FastAPI(title="SiteBot - AI Engineering Assistant")

# Mount frontend files
app.mount("/static", StaticFiles(directory="frontend"), name="static")

# Create uploads directory if it doesn't exist
os.makedirs("uploads", exist_ok=True)

# Ollama API endpoint
OLLAMA_URL = "http://localhost:11434/api/generate"


@app.get("/", response_class=HTMLResponse)
async def root():
    with open("frontend/index.html", "r") as f:
        return HTMLResponse(content=f.read())


@app.post("/upload")
async def upload_files(files: List[UploadFile] = File(...)):
    uploaded_files = []

    for file in files:
        # Save file to uploads directory
        file_path = f"uploads/{file.filename}"
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        uploaded_files.append({
            "filename": file.filename,
            "size": os.path.getsize(file_path)
        })

    return {"message": f"Uploaded {len(uploaded_files)} files", "files": uploaded_files}


@app.post("/chat")
async def chat_with_documents(message: dict):
    user_message = message.get("message", "")

    # Simple test response for now - we'll enhance this
    ollama_response = {
        "model": "qwen2.5:3b",
        "prompt": f"You are an AI assistant for engineering documents. User asks: {user_message}",
        "stream": False,
        "temperature": 0.1
    }

    try:
        response = requests.post(OLLAMA_URL, json=ollama_response)
        result = response.json()
        return {"response": result.get("response", "Error processing request")}
    except Exception as e:
        return {"response": f"Error: {str(e)}"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)