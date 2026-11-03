import os
import sys
import json
import re
import time
import subprocess
import asyncio
from pathlib import Path
from datetime import datetime

import httpx
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Cargar variables de entorno
BASE_DIR = Path(__file__).resolve().parents[2]
ENV_PATH = BASE_DIR / "backend" / ".env"
load_dotenv(ENV_PATH)

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not TELEGRAM_BOT_TOKEN or not GEMINI_API_KEY:
    print("[!] ERROR: Faltan credenciales en backend/.env")
    sys.exit(1)

# Inicializar cliente Gemini
ai_client = genai.Client(api_key=GEMINI_API_KEY)

TELEGRAM_API = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}"
CONTENT_DIR = BASE_DIR / "frontend" / "src" / "content"

SYSTEM_PROMPT = """
Eres el editor técnico de mi bitácora personal y jardín digital (Digital Garden).
Tu misión es transformar el dictado o nota (audio o texto) en una entrada limpia, sobria y concisa.

DIRECTRICES DE CLASIFICACIÓN Y COLECCIÓN:
1. Elige la colección adecuada:
   - "til": Aprendizajes del día a día, notas breves, trucos de ingeniería, datos históricos o curiosidades aprendidas hoy (Today I Learned).
   - "blog": Ensayos estructurados y reflexiones largas.
   - "lab": Proyectos de código, herramientas, prototipos, scripts o arquitectura.
   - "hobbies": Curiosidades no técnicas, Pokémon, gaming, coleccionismo, consolas y ocio.

2. CERO clichés de IA: nada de frases vacías ("En este fascinante post...", "Bienvenidos...", "En conclusión..."). Ve al grano.

3. Devuelve ÚNICAMENTE un objeto JSON válido con los siguientes campos:
   - "title": Título conciso y claro (sin comillas dobles internas).
   - "collection": "til" | "blog" | "lab" | "hobbies"
   - "tags": Lista de 2 a 4 tags en minúsculas y sin '#' (ej: ["historia", "chile", "botanica"]).
   - "snippet": Resumen de una sola frase (máximo 120 caracteres).
   - "content": Contenido completo en Markdown limpio.
   - "topic": (Solo si collection es "blog") Uno de: "tecnología" | "tecno-política" | "gaming" | "hardware" | "general".
   - "category": (Solo si collection es "hobbies") Uno de: "pokemon" | "gaming" | "hardware" | "coleccionismo" | "curiosidades".
"""

def slugify(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r'[^\w\s-]', '', text)
    slug = re.sub(r'[-\s]+', '-', text)
    return slug or "nota"

def send_telegram_message(chat_id: int, text: str):
    try:
        with httpx.Client(timeout=15.0) as client:
            client.post(f"{TELEGRAM_API}/sendMessage", json={"chat_id": chat_id, "text": text, "parse_mode": "Markdown"})
    except Exception as e:
        print(f"[!] Error enviando mensaje a Telegram: {e}")

def process_with_gemini(audio_bytes: bytes | None = None, text_content: str | None = None) -> dict:
    contents = []
    if audio_bytes:
        contents.append(types.Part.from_bytes(data=audio_bytes, mime_type="audio/ogg"))
        contents.append("Transcribe y formatea esta nota de voz técnica para mi bitácora:")
    elif text_content:
        contents.append(f"Formatea esta nota para mi bitácora técnica:\n\n{text_content}")

    # Lista de modelos con fallback automático
    models_to_try = ["gemini-3.5-flash-lite", "gemini-3.1-flash-lite", "gemini-3.8-flash", "gemini-flash-lite-latest"]
    last_err = None

    for model_name in models_to_try:
        try:
            response = ai_client.models.generate_content(
                model=model_name,
                contents=contents,
                config=types.GenerateContentConfig(
                    system_instruction=SYSTEM_PROMPT,
                    response_mime_type="application/json",
                    temperature=0.3
                )
            )
            return json.loads(response.text)
        except Exception as e:
            last_err = e
            continue

    raise RuntimeError(f"Error procesando con Gemini: {last_err}")

def save_and_commit(entry: dict) -> tuple[str, str]:
    collection = entry.get("collection", "til")
    if collection not in ["til", "blog", "lab", "hobbies"]:
        collection = "til"

    target_dir = CONTENT_DIR / collection
    target_dir.mkdir(parents=True, exist_ok=True)

    date_str = datetime.now().strftime("%Y-%m-%d")
    slug = slugify(entry["title"])
    filename = f"{date_str}-{slug}.md"
    file_path = target_dir / filename

    tags_formatted = ", ".join([f'"{t}"' for t in entry.get("tags", [])])

    valid_topics = ["tecnología", "tecno-política", "gaming", "hardware", "general"]
    topic = entry.get("topic", "general")
    if topic not in valid_topics:
        topic = "general"

    valid_categories = ["pokemon", "gaming", "hardware", "coleccionismo", "curiosidades"]
    category = entry.get("category", "curiosidades")
    if category not in valid_categories:
        category = "curiosidades"

    if collection == "til":
        frontmatter = f"""---
title: "{entry['title']}"
publishDate: {date_str}
tags: [{tags_formatted}]
snippet: "{entry.get('snippet', '')}"
---"""
    elif collection == "blog":
        frontmatter = f"""---
title: "{entry['title']}"
description: "{entry.get('snippet', '')}"
publishDate: {date_str}
tags: [{tags_formatted}]
topic: "{topic}"
draft: false
---"""
    elif collection == "lab":
        frontmatter = f"""---
title: "{entry['title']}"
description: "{entry.get('snippet', '')}"
status: "wip"
stack: [{tags_formatted}]
updatedDate: {date_str}
---"""
    else:  # hobbies
        frontmatter = f"""---
title: "{entry['title']}"
category: "{category}"
date: {date_str}
tags: [{tags_formatted}]
---"""

    full_markdown = f"{frontmatter}\n\n{entry['content'].strip()}\n"
    file_path.write_text(full_markdown, encoding="utf-8")

    # Git commit y push
    try:
        subprocess.run(["git", "add", str(file_path)], cwd=BASE_DIR, check=True)
        commit_msg = f"feat({collection}): {entry['title']}"
        subprocess.run(["git", "commit", "-m", commit_msg], cwd=BASE_DIR, check=True)
        subprocess.run(["git", "push", "origin", "main"], cwd=BASE_DIR, check=True)
        git_status = "Publicado en local y subido a GitHub (main) 🚀"
    except Exception as ge:
        git_status = f"Guardado en local (Git push pendiente o manual: {ge})"

    return str(file_path.name), git_status

def handle_update(update: dict):
    message = update.get("message")
    if not message:
        return

    chat_id = message["chat"]["id"]

    # Caso 1: Nota de voz o audio
    if "voice" in message or "audio" in message:
        voice = message.get("voice") or message.get("audio")
        file_id = voice["file_id"]
        send_telegram_message(chat_id, "🎧 _Escuchando tu nota de voz y redactando entrada con Gemini..._")

        try:
            with httpx.Client(timeout=30.0) as client:
                # Obtener ruta de descarga del archivo en Telegram
                file_info = client.get(f"{TELEGRAM_API}/getFile?file_id={file_id}").json()
                file_path = file_info["result"]["file_path"]
                download_url = f"https://api.telegram.org/file/bot{TELEGRAM_BOT_TOKEN}/{file_path}"
                audio_bytes = client.get(download_url).content

            # Procesar con Gemini
            entry = process_with_gemini(audio_bytes=audio_bytes)
            filename, git_status = save_and_commit(entry)

            tags_str = " ".join([f"#{t}" for t in entry.get("tags", [])])
            reply = (
                f"✅ *Entrada publicada en el jardín digital*\n\n"
                f"📌 *Título:* {entry['title']}\n"
                f"📁 *Colección:* `~/{entry.get('collection', 'til')}`\n"
                f"🏷️ *Tags:* {tags_str}\n\n"
                f"📄 *Archivo:* `{filename}`\n"
                f"🌐 *Estado:* {git_status}"
            )
            send_telegram_message(chat_id, reply)

        except Exception as e:
            send_telegram_message(chat_id, f"❌ Error procesando el audio: {e}")

    # Caso 2: Mensaje de texto
    elif "text" in message:
        text = message["text"]
        if text.startswith("/start"):
            send_telegram_message(
                chat_id,
                "👋 *¡Hola VitoNez! Soy el bot de tu bitácora técnica.*\n\n"
                "🎙️ *Envíame una nota de voz* contándome lo que aprendiste hoy y la transcribiré, formatearé y publicaré automáticamente en tu jardín digital."
            )
            return

        send_telegram_message(chat_id, "✍️ _Procesando nota de texto con Gemini..._")
        try:
            entry = process_with_gemini(text_content=text)
            filename, git_status = save_and_commit(entry)
            tags_str = " ".join([f"#{t}" for t in entry.get("tags", [])])
            reply = (
                f"✅ *Entrada creada*\n\n"
                f"📌 *Título:* {entry['title']}\n"
                f"📁 *Colección:* `~/{entry.get('collection', 'til')}`\n"
                f"🏷️ *Tags:* {tags_str}\n\n"
                f"📄 *Archivo:* `{filename}`\n"
                f"🌐 *Estado:* {git_status}"
            )
            send_telegram_message(chat_id, reply)
        except Exception as e:
            send_telegram_message(chat_id, f"❌ Error procesando el texto: {e}")

def run_bot():
    print(f"[*] Iniciando escucha para @BlogVitobot...")
    offset = 0
    with httpx.Client(timeout=35.0) as client:
        while True:
            try:
                response = client.get(f"{TELEGRAM_API}/getUpdates?offset={offset}&timeout=20")
                if response.status_code == 200:
                    data = response.json()
                    for update in data.get("result", []):
                        offset = update["update_id"] + 1
                        handle_update(update)
                else:
                    time.sleep(2)
            except (httpx.ReadTimeout, httpx.ConnectTimeout):
                continue
            except Exception as e:
                print(f"[!] Error en polling: {e}")
                time.sleep(3)

if __name__ == "__main__":
    run_bot()

