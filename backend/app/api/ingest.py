from fastapi import APIRouter, HTTPException, Body, Request
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Literal
import re
from pathlib import Path

router = APIRouter()

# ---------------------------------------------------------------------------
# Modelos de Datos para JSON estructurado
# ---------------------------------------------------------------------------

class TILPayload(BaseModel):
    title: str = Field(..., description="Título de la nota o aprendizaje")
    content: str = Field(..., description="Cuerpo del texto en Markdown")
    tags: list[str] = Field(default_factory=list, description="Lista de tags")
    snippet: str | None = Field(default=None, description="Resumen breve o snippet")

class BlogPayload(BaseModel):
    title: str = Field(..., description="Título del ensayo")
    description: str = Field(..., description="Resumen o bajada del ensayo")
    content: str = Field(..., description="Cuerpo completo del ensayo en Markdown")
    tags: list[str] = Field(default_factory=list, description="Lista de tags")
    topic: Literal["tecnología", "tecno-política", "gaming", "hardware", "general"] = "general"
    draft: bool = Field(default=false, description="Si es borrador o público")

class LabPayload(BaseModel):
    title: str = Field(..., description="Nombre del proyecto o experimento")
    description: str = Field(..., description="Descripción técnica")
    content: str = Field(..., description="Detalles, arquitectura y notas del proyecto")
    status: Literal["active", "prototype", "wip", "archived"] = "wip"
    stack: list[str] = Field(default_factory=list, description="Tecnologías usadas")
    repoUrl: str | None = Field(default=None, description="URL del repositorio")
    demoUrl: str | None = Field(default=None, description="URL de demo en vivo")

class HobbiesPayload(BaseModel):
    title: str = Field(..., description="Título de la entrada")
    content: str = Field(..., description="Notas de la colección, partida o compra")
    category: Literal["pokemon", "gaming", "hardware", "coleccionismo", "curiosidades"] = "gaming"
    status: str | None = Field(default=None, description="Estado (ej. completando set)")
    tags: list[str] = Field(default_factory=list, description="Etiquetas")

class RawTextPayload(BaseModel):
    raw_text: str = Field(..., description="Texto plano o nota rápida sin procesar")
    target_collection: Literal["til", "blog", "lab", "hobbies"] = "til"

# ---------------------------------------------------------------------------
# Utilidades
# ---------------------------------------------------------------------------

def get_content_dir(collection: str) -> Path:
    """Resuelve la ruta absoluta hacia la carpeta de contenido de Astro."""
    current_dir = Path(__file__).resolve().parent
    base_dir = current_dir.parents[2] / "frontend" / "src" / "content" / collection
    base_dir.mkdir(parents=True, exist_ok=True)
    return base_dir

def slugify(text: str) -> str:
    """Convierte texto a un slug limpio para nombres de archivo."""
    text = text.lower().strip()
    text = re.sub(r'[^\w\s-]', '', text)
    slug = re.sub(r'[-\s]+', '-', text)
    return slug or "nota-sin-titulo"

def format_tags(tags: list[str]) -> str:
    """Formatea la lista de tags para YAML frontmatter."""
    clean_tags = [f'"{t.strip().lstrip("#")}"' for t in tags if t.strip()]
    return f"[{', '.join(clean_tags)}]"

# ---------------------------------------------------------------------------
# Endpoints de Ingesta Estructurada (JSON)
# ---------------------------------------------------------------------------

@router.post("/til", summary="Ingestar nota TIL (Stream principal)")
def ingest_til(payload: TILPayload):
    try:
        content_dir = get_content_dir("til")
        date_str = datetime.now().strftime("%Y-%m-%d")
        slug = slugify(payload.title)
        filename = f"{date_str}-{slug}.md"
        file_path = content_dir / filename

        snippet_yaml = f'snippet: "{payload.snippet}"\n' if payload.snippet else ""
        markdown_content = f"""---
title: "{payload.title}"
publishDate: {date_str}
tags: {format_tags(payload.tags)}
{snippet_yaml}---

{payload.content.strip()}
"""
        file_path.write_text(markdown_content, encoding="utf-8")
        return {"success": True, "collection": "til", "filename": filename, "path": str(file_path)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/blog", summary="Ingestar ensayo o artículo largo")
def ingest_blog(payload: BlogPayload):
    try:
        content_dir = get_content_dir("blog")
        date_str = datetime.now().strftime("%Y-%m-%d")
        slug = slugify(payload.title)
        filename = f"{date_str}-{slug}.md"
        file_path = content_dir / filename

        markdown_content = f"""---
title: "{payload.title}"
description: "{payload.description}"
publishDate: {date_str}
tags: {format_tags(payload.tags)}
topic: "{payload.topic}"
draft: {str(payload.draft).lower()}
---

{payload.content.strip()}
"""
        file_path.write_text(markdown_content, encoding="utf-8")
        return {"success": True, "collection": "blog", "filename": filename, "path": str(file_path)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/lab", summary="Ingestar proyecto o experimento")
def ingest_lab(payload: LabPayload):
    try:
        content_dir = get_content_dir("lab")
        date_str = datetime.now().strftime("%Y-%m-%d")
        slug = slugify(payload.title)
        filename = f"{slug}.md"
        file_path = content_dir / filename

        repo_yaml = f'repoUrl: "{payload.repoUrl}"\n' if payload.repoUrl else ""
        demo_yaml = f'demoUrl: "{payload.demoUrl}"\n' if payload.demoUrl else ""

        markdown_content = f"""---
title: "{payload.title}"
description: "{payload.description}"
status: "{payload.status}"
stack: {format_tags(payload.stack)}
{repo_yaml}{demo_yaml}updatedDate: {date_str}
---

{payload.content.strip()}
"""
        file_path.write_text(markdown_content, encoding="utf-8")
        return {"success": True, "collection": "lab", "filename": filename, "path": str(file_path)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/hobbies", summary="Ingestar registro de hobbies, Pokémon o gaming")
def ingest_hobbies(payload: HobbiesPayload):
    try:
        content_dir = get_content_dir("hobbies")
        date_str = datetime.now().strftime("%Y-%m-%d")
        slug = slugify(payload.title)
        filename = f"{date_str}-{slug}.md"
        file_path = content_dir / filename

        status_yaml = f'status: "{payload.status}"\n' if payload.status else ""

        markdown_content = f"""---
title: "{payload.title}"
category: "{payload.category}"
date: {date_str}
{status_yaml}tags: {format_tags(payload.tags)}
---

{payload.content.strip()}
"""
        file_path.write_text(markdown_content, encoding="utf-8")
        return {"success": True, "collection": "hobbies", "filename": filename, "path": str(file_path)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ---------------------------------------------------------------------------
# Endpoint de Ingesta Inteligente de Texto Plano / Notas Rápidas
# ---------------------------------------------------------------------------

@router.post("/quick", summary="Ingesta rápida desde texto plano con auto-parsing")
async def ingest_quick_note(
    request: Request,
    payload: RawTextPayload | None = None
):
    """
    Recibe texto sin procesar (vía JSON {"raw_text": "..."} o directamente Content-Type: text/plain).
    
    Reglas de parsing automático:
    1. Si incluye una etiqueta [blog], [lab], [hobbies] o [til] al inicio, elige esa colección.
    2. La primera línea se toma como título.
    3. Extrae automáticamente cualquier #hashtag del texto como tags.
    4. El resto de las líneas se convierte en el cuerpo Markdown.
    """
    # Manejar si enviaron texto plano como cuerpo HTTP o JSON
    raw_content = ""
    target_collection = "til"

    content_type = request.headers.get("content-type", "")
    if "text/plain" in content_type:
        body_bytes = await request.body()
        raw_content = body_bytes.decode("utf-8").strip()
    elif payload:
        raw_content = payload.raw_text.strip()
        target_collection = payload.target_collection
    else:
        # Intentar leer texto crudo
        body_bytes = await request.body()
        raw_content = body_bytes.decode("utf-8").strip()

    if not raw_content:
        raise HTTPException(status_code=400, detail="El cuerpo del texto no puede estar vacío.")

    # 1. Detectar colección objetivo si tiene prefijo [seccion]
    first_line_match = re.match(r'^\[(til|blog|lab|hobbies)\]\s*(.*)', raw_content, re.IGNORECASE)
    if first_line_match:
        target_collection = first_line_match.group(1).lower()
        # Eliminar el prefijo de la primera línea
        raw_content = first_line_match.group(2) + "\n" + "\n".join(raw_content.splitlines()[1:])

    lines = [line for line in raw_content.splitlines()]
    non_empty_lines = [l.strip() for l in lines if l.strip()]

    # 2. Extraer Título (primera línea no vacía, quitando marcas '#' de markdown si las tiene)
    first_line = non_empty_lines[0] if non_empty_lines else "Nota Rápida"
    title = re.sub(r'^#+\s*', '', first_line).strip()

    # 3. Extraer hashtags automáticos (ej. #python #terminal)
    hashtags = re.findall(r'#([a-zA-Z0-9_\-]+)', raw_content)

    # 4. Cuerpo de la nota (todas las líneas después del título)
    remaining_lines = []
    found_title = False
    for line in lines:
        if not found_title and line.strip() == first_line:
            found_title = True
            continue
        if found_title:
            remaining_lines.append(line)

    body_markdown = "\n".join(remaining_lines).strip()
    if not body_markdown:
        body_markdown = title

    # 5. Despachar a la colección correspondiente
    if target_collection == "til":
        return ingest_til(TILPayload(
            title=title,
            content=body_markdown,
            tags=list(set(hashtags)),
            snippet=body_markdown[:140] if len(body_markdown) > 140 else None
        ))
    elif target_collection == "blog":
        return ingest_blog(BlogPayload(
            title=title,
            description=body_markdown[:160],
            content=body_markdown,
            tags=list(set(hashtags)),
            topic="general"
        ))
    elif target_collection == "lab":
        return ingest_lab(LabPayload(
            title=title,
            description=body_markdown[:140],
            content=body_markdown,
            status="wip",
            stack=list(set(hashtags))
        ))
    elif target_collection == "hobbies":
        return ingest_hobbies(HobbiesPayload(
            title=title,
            content=body_markdown,
            category="gaming",
            tags=list(set(hashtags))
        ))
    else:
        raise HTTPException(status_code=400, detail=f"Colección '{target_collection}' no soportada.")
