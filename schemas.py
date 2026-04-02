from abc import ABC, abstractmethod


class IModelAdapter(ABC):

    @abstractmethod
    def complete(
        self,
        system: str,
        user: str,
        history: list[dict] | None = None
    ) -> tuple[str, int | None]:
        """
        Envía un mensaje al modelo y retorna (respuesta, tokens_usados).
        """
        pass
