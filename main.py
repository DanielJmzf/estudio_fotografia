from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse

from src.domain.schemas import ChatRequest, ChatResponse
from src.services.chat_service import ChatService

load_dotenv()

app = FastAPI(
    title="Chatbot — Daniel Fotografía",
    description="Asistente virtual con RAG para Daniel Fotografía",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

_chat_service = ChatService()


@app.get("/", response_class=HTMLResponse)
def frontend() -> HTMLResponse:
    html = Path("index.html").read_text(encoding="utf-8")
    return HTMLResponse(content=html)

@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest) -> ChatResponse:
    try:
        return _chat_service.responder(request)
    except RuntimeError as e:
        print(f">>> ERROR: {str(e)}")   # agrega esta línea
        raise HTTPException(status_code=502, detail=str(e))
    except Exception as e:
        print(f">>> ERROR INESPERADO: {str(e)}")   # y esta
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")