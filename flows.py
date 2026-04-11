"""
flows.py — Prefect flow principal del proyecto estudio_fotografia.

Carga el bloque de GitHub llamado 'chatbot-fotografia' usando
GitHubRepository.load() de prefect-github, y ejecuta el código
del repositorio remoto desde un flow de Prefect.
"""

from prefect import flow, get_run_logger
from prefect_github import GitHubRepository


@flow(name="estudio-fotografia-flow", log_prints=True)
async def main_flow():
    """
    Flow principal que:
    1. Carga el bloque GitHubRepository 'chatbot-fotografia' desde Prefect Cloud.
    2. Clona/accede al repositorio remoto.
    3. Ejecuta la lógica principal del proyecto.
    """
    logger = get_run_logger()

    # Cargar el bloque de GitHub registrado en Prefect Cloud
    logger.info("Cargando bloque GitHubRepository 'chatbot-fotografia'...")
    repo_block = await GitHubRepository.load("chatbot-fotografia")

    logger.info(f"Bloque cargado: {repo_block}")
    logger.info(f"Repositorio: {repo_block.repository_url}")
    logger.info(f"Referencia (branch/tag): {repo_block.reference}")

    # Obtener el contenido del repositorio (lo clona localmente)
    logger.info("Obteniendo contenido del repositorio...")
    await repo_block.get_directory()

    logger.info("✅ Repositorio clonado correctamente. Flow completado.")


if __name__ == "__main__":
    import asyncio
    asyncio.run(main_flow())
