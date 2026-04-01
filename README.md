# Chatbot — Daniel Fotografía 📸

Asistente virtual con **RAG simplificado** para el estudio de fotografía.
Construido con FastAPI + Gemini + Factory Pattern. Desplegable en Vercel.

## Arquitectura

```
Usuario → POST /chat → ChatService → AIModelFactory → GeminiAdapter
                                ↑
                         ContextLoader
                    skills/asistente-estudio.md
                    knowledge/*.md (RAG)
```

## Estructura del proyecto

```
estudio_fotografia/
├── main.py                          # Entrypoint FastAPI
├── requirements.txt
├── vercel.json
├── .env.example
├── CLAUDE.md                        # Rules del proyecto
│
├── skills/
│   └── asistente-estudio.md         # System prompt del chatbot
│
├── knowledge/                       # Base de conocimiento (RAG)
│   ├── servicios.md
│   ├── paquetes.md
│   ├── politicas.md
│   └── equipo.md
│
└── src/
    ├── domain/
    │   ├── schemas.py               # ChatRequest, ChatResponse, AIProvider
    │   └── interfaces.py            # IModelAdapter (ABC)
    ├── services/
    │   └── chat_service.py          # Orquestación
    └── infrastructure/
        ├── context_loader.py        # Lee skills/ + knowledge/
        ├── model_factory.py         # Factory Pattern
        └── gemini_adapter.py        # Adaptador Gemini
```

## Instalación local

```bash
git clone https://github.com/Criss16JAP/estudio_fotografia.git
cd estudio_fotografia
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
copy .env.example .env
# Editar .env y agregar GEMINI_API_KEY
uvicorn main:app --reload
```

## Endpoint principal

```bash
POST /chat
{ "pregunta": "¿Cuánto cuesta una boda?", "provider": "gemini", "historial": [] }
```

## Despliegue en Vercel

1. Import este repo en vercel.com
2. Agregar variable de entorno: `GEMINI_API_KEY`
3. Deploy ✅
