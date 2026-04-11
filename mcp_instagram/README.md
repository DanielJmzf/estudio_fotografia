# MCP — Instagram Daniel Fotografía

Servidor MCP con 2 tools para consultar el Instagram público de `@danielfotografia_2003`.

## Tools disponibles

### `obtener_perfil_instagram`
Retorna info del perfil: bio, seguidores, publicaciones, verificado, etc.

### `listar_fotos_recientes(cantidad: int = 6)`
Retorna las N fotos más recientes con: fecha, likes, comentarios, descripción y URL.

---

## Instalación

```bash
# 1. Crear entorno virtual
python -m venv venv
venv\Scripts\activate       # Windows
source venv/bin/activate    # Mac/Linux

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Correr el servidor MCP
python mcp_server.py
```

---

## Conectar con Claude Desktop

Edita el archivo de configuración de Claude Desktop:

**Windows:** `%APPDATA%\Claude\claude_desktop_config.json`
**Mac:** `~/Library/Application Support/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "daniel-instagram": {
      "command": "python",
      "args": ["C:/ruta/completa/a/mcp_server.py"]
    }
  }
}
```

Reinicia Claude Desktop y verás las tools disponibles.

---

## Ejemplo de uso

Una vez conectado, puedes preguntarle a Claude:
- *"¿Cuántos seguidores tiene Daniel en Instagram?"*
- *"Muéstrame las últimas 6 fotos de Daniel"*
- *"¿Cuál es la foto con más likes de Daniel?"*

---

## Notas

- Solo funciona con perfiles **públicos**
- Instagram puede bloquear requests frecuentes — usar con moderación
- `instaloader` no requiere login para perfiles públicos
