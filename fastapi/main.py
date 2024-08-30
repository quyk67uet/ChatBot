from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from dotenv import load_dotenv
import os
import google.generativeai as genai
from PIL import Image
from io import BytesIO
import logging

# Load environment variables
load_dotenv()

# Configure Google Gemini API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

app = FastAPI()

class ChatRequest(BaseModel):
    question: str

class VisionRequest(BaseModel):
    input: Optional[str] = ""

class VisionResponse(BaseModel):
    response: str

@app.post("/chat/")
async def get_gemini_response(request: ChatRequest):
    try:
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(request.question)
        return {"response": response.text}
    except Exception as e:
        logging.error(f"Error in /qa/ endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/vision/", response_model=VisionResponse)
async def vision(input: str = "", image: UploadFile = File(...)):
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')  # Use the updated model
        
        # Convert uploaded image to PIL format
        image_data = await image.read()
        image_pil = Image.open(BytesIO(image_data))
        
        if input:
            response = model.generate_content([input, image_pil])
        else:
            response = model.generate_content(image_pil)
        
        return VisionResponse(response=response.text)
    except Exception as e:
        logging.error(f"Error in /vision/ endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))