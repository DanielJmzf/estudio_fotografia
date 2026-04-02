from domain.schemas import AIProvider, ChatRequest, ChatResponse
from infrastructure.context_loader import ContextLoader
from infrastructure.model_factory import AIModelFactory


class ChatService:

    def __init__(self) -> None:
        self._context_loader = ContextLoader()

    def responder(self, request: ChatRequest) -> ChatResponse:
        try:
            # 1. Cargar system prompt + knowledge (RAG simplificado)
            system_prompt: str = self._context_loader.load_full_context()

            # 2. Crear el adaptador via Factory (desacoplado del proveedor)
            adapter = AIModelFactory.create(request.provider)

            # 3. Llamar al modelo
            respuesta, tokens = adapter.complete(
                system=system_prompt,
                user=request.pregunta,
                history=request.historial
            )

            return ChatResponse(
                respuesta=respuesta,
                tokens_usados=tokens,
                proveedor_usado=request.provider.value
            )

        except Exception as e:
            raise RuntimeError(f"Error en ChatService: {str(e)}") from e
