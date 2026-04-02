import os
import re
import time
import google.generativeai as genai
from domain.interfaces import IModelAdapter

# Patrones comunes de prompt injection
_INJECTION_PATTERNS: list[str] = [
    r"olvida\s+(todas?\s+)?(tus\s+)?(instrucciones|reglas)",
    r"ignora\s+(todas?\s+)?(tus\s+)?(instrucciones|reglas)",
    r"actúa\s+como",
    r"actua\s+como",
    r"eres\s+ahora",
    r"nuevo\s+rol",
    r"system\s*prompt",
    r"prompt\s*injection",
    r"jailbreak",
    r"deja\s+de\s+ser",
    r"finge\s+que\s+eres",
    r"pretend\s+you\s+are",
    r"ignore\s+(all\s+)?(previous\s+)?(instructions|rules)",
    r"forget\s+(all\s+)?(your\s+)?(instructions|rules)",
]

_INJECTION_REGEX = re.compile(
    "|".join(_INJECTION_PATTERNS),
    flags=re.IGNORECASE
)

_BLOCKED_RESPONSE = (
    "Solo estoy capacitado para brindarte información sobre los servicios "
    "fotográficos de Daniel Fotografía. ¿Te gustaría conocer nuestros "
    "paquetes disponibles? 📸"
)

_MAX_RETRIES: int = 4
_RETRY_DELAYS: list[int] = [15, 30, 60, 90]  # segundos entre reintentos


def _contains_injection(text: str) -> bool:
    return bool(_INJECTION_REGEX.search(text))


class GeminiAdapter(IModelAdapter):

    def __init__(self) -> None:
        api_key: str | None = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY no está configurada en las variables de entorno.")
        genai.configure(api_key=api_key)
        self._base_model_name: str = "gemini-2.0-flash-lite"

    def complete(
        self,
        system: str,
        user: str,
        history: list[dict] | None = None
    ) -> tuple[str, int | None]:

        # 1. Bloquear prompt injection antes de llegar al modelo
        if _contains_injection(user):
            return _BLOCKED_RESPONSE, 0

        last_error: Exception | None = None

        for attempt in range(_MAX_RETRIES):
            try:
                # 2. Modelo con system_instruction como canal inmutable
                model = genai.GenerativeModel(
                    model_name=self._base_model_name,
                    system_instruction=system
                )

                # 3. Construir historial compatible con Gemini
                chat_history: list[dict] = []
                if history:
                    for msg in history:
                        role: str = "user" if msg.get("role") == "user" else "model"
                        chat_history.append({
                            "role": role,
                            "parts": [msg.get("content", "")]
                        })

                # 4. Enviar solo el mensaje del usuario
                chat = model.start_chat(history=chat_history)
                response = chat.send_message(
                    user,
                    generation_config=genai.GenerationConfig(max_output_tokens=500)
                )

                respuesta: str = response.text
                tokens: int | None = None
                if hasattr(response, "usage_metadata") and response.usage_metadata:
                    tokens = response.usage_metadata.total_token_count

                return respuesta, tokens

            except Exception as e:
                last_error = e
                error_str: str = str(e)

                # Si es error de cuota (429), esperar y reintentar
                if "429" in error_str or "quota" in error_str.lower() or "rate" in error_str.lower():
                    if attempt < _MAX_RETRIES - 1:
                        wait: int = _RETRY_DELAYS[attempt]
                        print(f"[GeminiAdapter] Cuota excedida. Reintento {attempt + 1}/{_MAX_RETRIES - 1} en {wait}s...")
                        time.sleep(wait)
                        continue

                # Si es otro error, no reintentar
                raise RuntimeError(f"Error en GeminiAdapter: {error_str}") from e

        raise RuntimeError(f"Error en GeminiAdapter tras {_MAX_RETRIES} intentos: {str(last_error)}")
