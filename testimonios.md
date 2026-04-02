from pathlib import Path


class ContextLoader:

    def load_skill(self) -> str:
        path = Path("skills/asistente-estudio.md")
        if not path.exists():
            return "Eres un asistente útil del estudio fotográfico."
        return path.read_text(encoding="utf-8")

    def load_knowledge(self) -> str:
        knowledge_path = Path("knowledge")
        if not knowledge_path.exists():
            return ""
        files = sorted(knowledge_path.glob("*.md"))
        if not files:
            return ""
        return "\n\n---\n\n".join(
            f.read_text(encoding="utf-8") for f in files
        )

    def load_full_context(self) -> str:
        skill = self.load_skill()
        knowledge = self.load_knowledge()
        if knowledge:
            return f"{skill}\n\n## Base de conocimiento del estudio:\n\n{knowledge}"
        return skill
