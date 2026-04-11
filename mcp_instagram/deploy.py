from instagram_flow import instagram_sync_flow

if __name__ == "__main__":
    # Registra formalmente el deploiment en Prefect Cloud y permite programarlo
    instagram_sync_flow.serve(
        name="instagram-sync-deployment",
        tags=["instagram", "mcp", "analytics"],
        description="Deployment de la lógica de estadísticas de Instagram conectada al MCP.",
    )
