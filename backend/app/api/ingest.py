from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from datetime import datetime
import re
from pathlib import Path

router = APIRouter()

class TILIngestPayload(BaseModel):
    title: str = Field(..., description="Título de la nota o aprendizaje")
    content: str = Field(..., description="Cuerpo del texto en formato Markdown")
    tags: list[str] = Field(default_factory=list, description="Lista de etiquetas")
    snippet: str | None = Field(default=None, description="Resumen breve o snippet representativo")

def slugify(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r'[^\w\s-]', '', text)
    return re.sub(r'[-\s]+', '-', text)

@router.post("/til")
def ingest_til(payload: TILIngestPayload):
    try:
        # Resolver ruta a la carpeta de contenido de Astro
        current_dir = Path(__file__).resolve().parent
        content_dir = current_dir.parents[2] / "frontend" / "src" / "content" / "til"
        content_dir.mkdir(parents=True, exist_ok=True)

        date_str = datetime.now().strftime("%Y-%m-%d")
        slug = slugify(payload.title)
        filename = f"{date_str}-{slug}.md"
        file_path = content_dir / filename

        tags_formatted = ", ".join([f'"{t}"' for t in payload.tags])
        snippet_frontmatter = f'snippet: "{payload.snippet}"\n' if payload.snippet else ""

        markdown_file_content = f"""---
title: "{payload.title}"
publishDate: {date_str}
tags: [{tags_formatted}]
{snippet_frontmatter}---

{payload.content}
"""

        file_path.write_text(markdown_file_content, encoding="utf-8")

        return {
            "success": True,
            "filename": filename,
            "path": str(file_path),
            "message": "Entrada TIL registrada con éxito en el jardín digital."
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

