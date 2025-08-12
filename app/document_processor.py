import base64

import fitz
import requests
import os
from typing import List, Dict
import base64
import os


def extract_pdf_text(file_path: str) ->str:
    doc = fitz.open(file_path)
    text = ""
    for page in doc:
        text+= page.get_text()
    doc.close()
    return text
def analyze_image(image_path:str) -> str:
    with open(image_path, "rb") as file:
        image_data = file.read()
    encoded_image = base64.b64encode(image_data).decode('utf-8')

    payload = {
        "model": "llava:7b",  # Vision model
        "prompt": "Analyze this engineering diagram and describe what you see",
        "images": [encoded_image],
        "stream": False
    }


    response = requests.post("http://localhost:11434/api/generate",json=payload)
    ai_response = response.json().get("response", "Could not analyze image")
    return ai_response

def extract_images_from_pdf(file_path:str) -> List[str]:
    doc = fitz.open(file_path)
    image_descriptions = []

    for page_num in range(0, len(doc)):
        page = doc[page_num]
        image_list = page.get_images(full=True)
        for img_index, img in enumerate(image_list):
           xref = img[0]
           pix = fitz.Pixmap(doc,xref)
           img_path = f"uploads/temp_img_{page_num}_{img_index}.png"
           pix.save(img_path)
           description = analyze_image(img_path)
           image_descriptions.append(f"Image from page {page_num + 1}: {description}")
           os.remove(img_path)
           pix = None
    doc.close()
    return image_descriptions








if __name__ == "__main__":
    # Test PDF text extraction with real bridge document
    pdf_text = extract_pdf_text("../uploads/bridge_design.pdf")
    print("PDF Text Length:", len(pdf_text))
    print("First 500 characters:")
    print(pdf_text[:500])
    print("\n" + "="*50 + "\n")
    print("Last 500 characters:")
    print(pdf_text[-500:])

