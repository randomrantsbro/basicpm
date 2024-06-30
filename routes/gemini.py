# app/routes/gemini.py

from fastapi import APIRouter, HTTPException
from app.gemini_client import GeminiClient

router = APIRouter()
gemini_client = GeminiClient()

@router.get("/generate_content")
async def generate_content(prompt: str):
    content = gemini_client.generate_content(prompt)
    if "Error occurred" in content:
        raise HTTPException(status_code=500, detail=content)
    return {"generated_content": content}
