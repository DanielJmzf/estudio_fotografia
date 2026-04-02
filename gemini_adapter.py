from domain.interfaces import IModelAdapter
from domain.schemas import AIProvider


class AIModelFactory:

    @staticmethod
    def create(provider: AIProvider) -> IModelAdapter:
        if provider == AIProvider.GEMINI:
            from infrastructure.gemini_adapter import GeminiAdapter
            return GeminiAdapter()

        if provider == AIProvider.OPENAI:
            from infrastructure.openai_adapter import OpenAIAdapter
            return OpenAIAdapter()

        if provider == AIProvider.CLAUDE:
            from infrastructure.claude_adapter import ClaudeAdapter
            return ClaudeAdapter()

        raise ValueError(f"Proveedor no soportado: {provider}")
