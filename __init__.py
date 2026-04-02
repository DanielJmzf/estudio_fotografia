from enum import Enum
from pydantic import BaseModel, Field


class AIProvider(str, Enum):
    GEMINI = "gemini"
    OPENAI = "openai"
    CLAUDE = "claude"


class ChatRequest(BaseModel):
    pregunta: str = Field(..., min_length=1, max_length=300)  # 300 chars max — limita ataques largos
    provider: AIProvider = Field(default=AIProvider.GEMINI)
    historial: list[dict] = Field(default_factory=list, max_length=20)  # máx 20 turnos de historia


class ChatResponse(BaseModel):
    respuesta: str
    tokens_usados: int | None = None
    proveedor_usado: str
