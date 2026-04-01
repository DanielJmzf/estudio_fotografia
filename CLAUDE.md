# CLAUDE.md — Estudio de Fotografía AI

**Proyecto:** Asistente Virtual para Estudio de Fotografía — Backend FastAPI con RAG y Factory Pattern

---

## I. VISIÓN DEL PROYECTO

Este proyecto encarna las **4 capas de desarrollo inteligente**:

1. **RULES** ← Este archivo (estándares siempre activos que deberás darle a la IA cuando programes).
2. **SKILLS** ← `.agent/skills/backend-fastapi/SKILL.md` (instrucciones técnicas de código).
3. **RAG** ← `knowledge/*.md` + `ContextLoader` (conocimiento inyectado sobre el estudio fotográfico).
4. **FACTORY** ← `infrastructure/model_factory.py` (desacoplamiento total para usar Gemini, OpenAI o Claude).

El objetivo: **construir un sistema que responde sobre los servicios, paquetes y portafolio de un estudio de fotografía sin entrenar nada, solo inyectando conocimiento en tiempo de ejecución.**

---

## II. ARQUITECTURA HEXAGONAL

### A. Estructura de capas

```text
estudio-foto-ai/
├── src/
│   ├── domain/                          # La lógica pura, sin dependencias
│   │   ├── schemas.py                   # AIProvider enum, ChatRequest, ChatResponse
│   │   └── interfaces.py (opcional)     # IModelAdapter
│   │
│   ├── services/                        # Orquestación, sin detalles técnicos
│   │   └── chat_service.py              # ChatService con lógica de negocio
│   │
│   └── infrastructure/                  # Detalles técnicos, integraciones
│       ├── model_factory.py             # Factory Pattern
│       ├── gemini_adapter.py            # Adaptador Gemini
│       ├── openai_adapter.py            # Adaptador OpenAI
│       ├── claude_adapter.py            # Adaptador Claude
│       ├── context_loader.py            # Carga skills/*.md + knowledge/*.md
│
├── knowledge/                           # Base de datos de texto (RAG Semántico)
│   ├── servicios.md                     # Qué tipos de sesiones hacen (Bodas, Retratos)
│   ├── paquetes.md                      # Catálogo, precios y entregables
│   ├── portafolio.md                    # Descripción de estilo y trabajos previos
│   └── politicas.md                     # Cómo reservar, anticipos y cancelaciones
│
├── skills/                              # System prompt del chatbot
│   └── asistente-estudio.md             # Instrucciones al modelo para responder al cliente
│
├── .agent/skills/                       # Skills para tu editor de código (Cursor/Claude Code)
│   └── backend-fastapi/
│       ├── SKILL.md                     # Instrucciones al agente para programar
│
├── main.py                              # Entrypoint FastAPI
├── requirements.txt                     # Dependencias con versiones fijas
├── vercel.json                          # Configuración de despliegue
├── .env.example                         # Template de variables de entorno
└── .gitignore                           # Excluir .env, __pycache__, etc.
```

### B. Regla de oro: flujo descendente

```text
domain/ (lógica pura, schemas de Pydantic)
    ↓ importa desde
services/ (orquestación, une request con las respuestas)
    ↓ importa desde
infrastructure/ (detalles como llamadas a las APIs de IA)

NUNCA invertir este flujo. Si domain/ sabe que usas FastAPI o Gemini, violaste la arquitectura.
```

---

## III. PYTHON — ESTÁNDARES DE CÓDIGO

### A. Type hints obligatorios en TODO

Toda función, variable, parámetro y retorno **DEBE** tener type hint.

```python
# ✓ CORRECTO
def chat(
    pregunta: str,
    provider: str,
    historial: list[dict] | None = None
) -> dict[str, str]:
    """Procesa una pregunta sobre fotos y retorna cotización."""
    respuesta: str = ""
    tokens_usados: int = 0
    return {"respuesta": respuesta, "tokens": tokens_usados}
```

### B. Pydantic v2 para schemas

Toda entrada/salida de API **DEBE** ser un schema Pydantic.

```python
from pydantic import BaseModel, Field

class ChatRequest(BaseModel):
    pregunta: str = Field(..., min_length=1, max_length=500)
    provider: str = Field(default="gemini", description="gemini|openai|claude")
    historial: list[dict] = Field(default_factory=list)

class ChatResponse(BaseModel):
    respuesta: str
    tokens_usados: int | None = None
    proveedor_usado: str
```

### C. Naming conventions

- **Constantes:** `OPENAI_API_KEY`, `MAX_TOKENS`, `DEFAULT_PROVIDER`
- **Clases:** `ChatService`, `GeminiAdapter`, `ContextLoader`
- **Funciones:** `load_knowledge()`, `responder()`, `create_adapter()`

---

## IV. MODELOS DE IA — FACTORY PATTERN

### A. NUNCA instanciar directamente

```python
# ✗ PROHIBIDO en services/ o domain/
from infrastructure.gemini_adapter import GeminiAdapter
adapter = GeminiAdapter()  # Acoplamiento directo

# ✓ CORRECTO siempre
from infrastructure.model_factory import AIModelFactory, AIProvider
adapter = AIModelFactory.create(AIProvider.GEMINI)
```

### B. Interface IModelAdapter 

```python
from abc import ABC, abstractmethod

class IModelAdapter(ABC):
    @abstractmethod
    def complete(
        self,
        system: str,
        user: str,
        history: list[dict] | None = None
    ) -> tuple[str, int | None]:
        pass
```

---

## V. CONOCIMIENTO — RAG SIMPLIFICADO

### A. System prompt SIEMPRE desde `skills/asistente-estudio.md`

NUNCA hardcodees instrucciones en el código.

```python
# ✓ CORRECTO
from infrastructure.context_loader import ContextLoader

loader = ContextLoader()
system_prompt = loader.load_skill()  # Lee skills/asistente-estudio.md
```

**Contenido útil de `skills/asistente-estudio.md`:**

```markdown
# Asistente Virtual del Estudio de Fotografía

Eres "Pixel", el asistente experto en ventas y agendamientos del estudio fotográfico.

## Instrucciones
- Sé entusiasta, creativo y persuasivo. Queremos vender sesiones de fotos.
- Utiliza la información de contexto proporcionada para dar precios exactos.
- SIEMPRE menciona los descuentos por pagos en efectivo si te preguntan por rebajas.
- Si te piden un estilo de foto que no está en el portafolio (Ej: fotos submarinas), discúlpate y ofrece retratos en exterior como alternativa.
- Al final de tu respuesta, pregunta si desean reservar su fecha garantizándola con un abono.

## Restricciones
- NUNCA inventes precios o paquetes.
- Si el usuario requiere hablar con el fotógrafo principal, indícale que dejen su número.
```

### B. Knowledge SIEMPRE desde `knowledge/*.md`

**Ejemplo de contenido de `knowledge/paquetes.md`:**

```markdown
# Paquetes y Precios de Fotografía 2024

## 1. Paquete Bodas de Ensueño (Premium)
- **Precio**: $1,200 USD.
- **Incluye**: 
  - Cobertura completa (12 horas).
  - Sesión previa a la boda de 2 horas.
  - Edición estilo "Moody & Cinematic".
  - USB con 800 fotos de alta resolución + Álbum Físico Premium.
- **Abono**: 50% para separar fecha.

## 2. Sesión Retrato Business (Ejecutivos)
- **Precio**: $150 USD.
- **Incluye**: 
  - 1 hora en estudio con fondo infinito negro/blanco.
  - 2 cambios de vestuario.
  - 15 fotos editadas y retocadas digitalmente (remoción de imperfecciones).
```

### C. ContextLoader: la magia de RAG simplificado

```python
class ContextLoader:
    def load_skill(self) -> str:
        """Lee skills/asistente-estudio.md."""
        pass # Código igual al de tu archivo CLAUDE original

    def load_knowledge(self) -> str:
        """Lee todos los .md en knowledge/."""
        pass 
```

---

## VI. SEGURIDAD — SIN EXCEPCIONES

### A. NUNCA hardcodear API keys

```python
# ✓ CORRECTO
import os
from dotenv import load_dotenv

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
```

### B. Rutas SIEMPRE relativas a la raíz del proyecto

```python
from pathlib import Path
# ✓ CORRECTO
knowledge_path = Path("knowledge/paquetes.md")
```

---

## VII. DESPLIEGUE — VERCEL

### A. Entrypoint: `main.py` expone `app`

Vercel busca la variable `app` directamente, por eso evitamos el bloque `if __name__ == "__main__":`.

```python
# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Estudio Fotografía AI")

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"])
```

### B. `vercel.json`

```json
{
    "buildCommand": "pip install -r requirements.txt",
    "outputDirectory": ".",
    "env": {
        "GEMINI_API_KEY": "@gemini_api_key"
    }
}
```

---

## VIII. CHECKLIST ANTES DE CADA COMMIT

- [ ] **Type hints:** Toda función tiene type hints.
- [ ] **Try/except:** Excepciones en los ModelProviders están manejadas (Si Gemini se cae, debe lanzar un 502 al cliente).
- [ ] **Factory:** ¿Usaste `AIModelFactory.create()`?
- [ ] **Conocimiento Estudio:** Modifiqué los paquetes en la capeta `knowledge` y no quemé texto en el código Python.
- [ ] **Sin API Keys:** Mi `.env` no subió a Github.
- [ ] **main.py:** Expone `app` para que Vercel levante.

**Vigencia:** Para la creación del nuevo sistema de gestión comercial del Estudio Fotográfico.
