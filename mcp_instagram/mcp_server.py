from fastmcp import FastMCP
import instaloader
import json
from datetime import datetime

mcp = FastMCP("daniel-fotografia-instagram")

# Instancia reutilizable de instaloader
_loader = instaloader.Instaloader(
    download_pictures=False,
    download_videos=False,
    download_video_thumbnails=False,
    download_geotags=False,
    download_comments=False,
    save_metadata=False,
    quiet=True,
)

INSTAGRAM_USER = "danielfotografia_2003"


@mcp.tool()
def obtener_perfil_instagram() -> str:
    """
    Obtiene la información pública del perfil de Instagram de Daniel Fotografía:
    número de publicaciones, seguidores, seguidos y biografía.
    Úsala cuando el usuario pregunte por el perfil, estadísticas o descripción del fotógrafo.
    """
    try:
        profile = instaloader.Profile.from_username(
            _loader.context, INSTAGRAM_USER
        )

        datos = {
            "usuario": profile.username,
            "nombre": profile.full_name,
            "biografia": profile.biography,
            "publicaciones": profile.mediacount,
            "seguidores": profile.followers,
            "seguidos": profile.followees,
            "url_perfil": f"https://instagram.com/{profile.username}",
            "verificado": profile.is_verified,
            "es_privado": profile.is_private,
        }

        return json.dumps(datos, ensure_ascii=False, indent=2)

    except instaloader.exceptions.ProfileNotExistsException:
        return f"Error: El perfil @{INSTAGRAM_USER} no existe en Instagram."
    except instaloader.exceptions.ConnectionException as e:
        return f"Error de conexión con Instagram: {str(e)}"
    except Exception as e:
        return f"Error inesperado al obtener el perfil: {str(e)}"


@mcp.tool()
def listar_fotos_recientes(cantidad: int = 6) -> str:
    """
    Lista las fotos más recientes del Instagram de Daniel Fotografía.
    Retorna título (caption), fecha, número de likes y URL de cada publicación.
    Úsala cuando el usuario pregunte por las fotos recientes, el portafolio o
    los trabajos más nuevos del fotógrafo. Cantidad máxima recomendada: 12.
    """
    try:
        # Limitar para no hacer demasiadas requests
        cantidad = min(cantidad, 12)

        profile = instaloader.Profile.from_username(
            _loader.context, INSTAGRAM_USER
        )

        if profile.is_private:
            return "El perfil es privado. No se pueden ver las fotos sin seguir la cuenta."

        fotos = []
        for post in profile.get_posts():
            if len(fotos) >= cantidad:
                break

            # Caption limpia (primeras 120 chars)
            caption = (post.caption or "Sin descripción").strip()
            caption_corta = caption[:120] + "..." if len(caption) > 120 else caption

            foto = {
                "numero": len(fotos) + 1,
                "fecha": post.date_utc.strftime("%d/%m/%Y"),
                "likes": post.likes,
                "comentarios": post.comments,
                "tipo": "video" if post.is_video else "foto",
                "descripcion": caption_corta,
                "url": f"https://instagram.com/p/{post.shortcode}/",
            }
            fotos.append(foto)

        if not fotos:
            return "No se encontraron publicaciones en el perfil."

        resultado = {
            "perfil": f"@{INSTAGRAM_USER}",
            "total_mostradas": len(fotos),
            "publicaciones": fotos,
            }

        return json.dumps(resultado, ensure_ascii=False, indent=2)

    except instaloader.exceptions.ProfileNotExistsException:
        return f"Error: El perfil @{INSTAGRAM_USER} no existe."
    except instaloader.exceptions.ConnectionException as e:
        return f"Error de conexión con Instagram: {str(e)}"
    except Exception as e:
        return f"Error inesperado al listar fotos: {str(e)}"


if __name__ == "__main__":
    mcp.run()
