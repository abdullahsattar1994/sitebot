from typing import List

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import HTMLResponse

import requests


# Add extract_images_from_pdf to this line
from document_processor import extract_pdf_text, analyze_image, extract_images_from_pdf

# Add these imports at the top
from rag_system import DocumentRAG

# Create RAG instance
rag = DocumentRAG()


app = FastAPI(title="Sitebot")
#app.mount("/static", StaticFiles(directory="../frontend"), name="static")


@app.get("/", response_class=HTMLResponse)
def homepage():
    with open("../frontend/index.html", "r") as file:
        content = file.read()
    return content

@app.post("/upload")
def upload(files: List[UploadFile] = File(...)):
    import os
    os.makedirs("uploads", exist_ok=True)
    for file in files:
       file_path = f"uploads/{file.filename}"
       with open(file_path, "wb") as f:
           f.write(file.file.read())

       if file.filename.endswith('.pdf'):
           text = extract_pdf_text(file_path)
           rag.add_document(text, file.filename)


#uncomment here for images

           image_descriptions = extract_images_from_pdf(file_path)
           for description in image_descriptions:
               rag.add_document(description, f"{file.filename}_images")

    return {
    "message": "Files uploaded successfully",
    "count": len(files)  # What goes here?
    }


@app.post("/chat")
def chat(payload: dict):
    user_message = payload.get("message", "No message provided")

    # NEW: Search for relevant document chunks
    relevant_chunks = rag.search_documents(user_message, 3)

    # Create enhanced prompt with context
    if relevant_chunks:
        context = "\n".join(relevant_chunks)
        enhanced_prompt = f"""You are an AI assistant for engineering documents. 

Context from uploaded documents:
{context}

User question: {user_message}

Please answer based on the provided context."""
    else:
        enhanced_prompt = user_message

    ollama_payload = {
        "model": "qwen2.5:3b",
        "prompt": enhanced_prompt,  # Use enhanced prompt with context
        "stream": False
    }

    response = requests.post("http://localhost:11434/api/generate", json=ollama_payload)
    ai_response = response.json().get("response")

    return {"response": ai_response}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)



