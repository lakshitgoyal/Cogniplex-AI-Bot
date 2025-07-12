import os
import shutil
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse, StreamingResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from dotenv import load_dotenv
import google.generativeai as genai
from PIL import Image
import io

from .rag_handler import process_and_store_document, get_context_from_query

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

app = FastAPI()

class ChatRequest(BaseModel):
    query: str
    use_rag: bool = False

chat_history = {} 


@app.post("/api/chat")
async def chat_handler(request: ChatRequest):
    """Handles text-based chat, with optional RAG."""
    user_id = "default_user" 
    if user_id not in chat_history:
        chat_history[user_id] = genai.GenerativeModel('gemini-1.5-pro-latest').start_chat(history=[])

    try:
        prompt = request.query
        if request.use_rag:
            context = get_context_from_query(request.query)
            if context:
                prompt = f"""Based on the following information, answer the user's question.
                If the information is not relevant, say you don't know from the provided documents.

                Context:
                {context}

                Question: {request.query}
                """
        
        chat = chat_history[user_id]
        response_stream = chat.send_message(prompt, stream=True)

        async def stream_generator():
            for chunk in response_stream:
                if chunk.text:
                    yield chunk.text
        
        return StreamingResponse(stream_generator(), media_type="text/plain")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/upload/document")
async def upload_document(file: UploadFile = File(...)):
    """Accepts PDF uploads, processes them, and stores in the vector DB."""
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")
    
    file_path = f"uploads/{file.filename}"
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    result = process_and_store_document(file_path)
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])

    return JSONResponse(content=result)


@app.post("/api/analyze/media")
async def analyze_media(file: UploadFile = File(...), query: str = Form(...)):
    """Analyzes an uploaded image or video frames."""
    model = genai.GenerativeModel('gemini-1.5-pro-latest')
    
    contents = await file.read()
    
    if "image" not in file.content_type:
        raise HTTPException(status_code=400, detail="Only image analysis is supported in this demo.")

    try:
        img = Image.open(io.BytesIO(contents))
        prompt = [query, img]
        response = model.generate_content(prompt)
        return JSONResponse(content={"analysis": response.text})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to analyze image: {str(e)}")


app.mount("/", StaticFiles(directory="frontend", html=True), name="static")