from prefect import flow, task, get_run_logger
from mcp_server import obtener_perfil_instagram, listar_fotos_recientes
import json

@task
def fetch_profile() -> dict:
    """Wrapper to fetch the Instagram profile."""
    logger = get_run_logger()
    logger.info("Fetching Instagram profile...")
    result_str = obtener_perfil_instagram()
    try:
        return json.loads(result_str)
    except json.JSONDecodeError:
        logger.error(f"Failed to decode JSON from profile result: {result_str}")
        return {"error": result_str}

@task
def fetch_recent_photos(cantidad: int = 6) -> dict:
    """Wrapper to fetch recent photos from Instagram."""
    logger = get_run_logger()
    logger.info(f"Fetching {cantidad} recent photos...")
    result_str = listar_fotos_recientes(cantidad)
    try:
        return json.loads(result_str)
    except json.JSONDecodeError:
        logger.error(f"Failed to decode JSON from photos result: {result_str}")
        return {"error": result_str}

@flow(name="instagram-sync", log_prints=True)
def instagram_sync_flow(cantidad_fotos: int = 6):
    """
    Flow that fetches the profile and recent photos from Instagram.
    These tools correspond to the logic used by the MCP server.
    """
    logger = get_run_logger()
    logger.info("Starting Instagram Synchronization Flow")

    profile_data = fetch_profile()
    if "error" not in profile_data:
        logger.info(f"Profile: {profile_data.get('usuario')} - {profile_data.get('seguidores')} followers")
    else:
        logger.warning(f"Error fetching profile: {profile_data['error']}")
        
    photos_data = fetch_recent_photos(cantidad_fotos)
    if "error" not in photos_data:
        logger.info(f"Fetched {photos_data.get('total_mostradas', 0)} recent photos.")
    else:
        logger.warning(f"Error fetching photos: {photos_data['error']}")
        
    logger.info("Instagram Synchronization Flow Completed")
    
    return {
        "profile": profile_data,
        "recent_photos": photos_data
    }

if __name__ == "__main__":
    instagram_sync_flow()
