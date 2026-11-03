---
title: "FastAPI Content Ingestion Agent"
description: "Servicio de automatización ligero para capturar notas de voz y enlaces técnicos, procesarlos con LLMs y commitear archivos Markdown directamente al repo."
status: "wip"
stack: ["Python", "FastAPI", "Pydantic", "GitPython"]
repoUrl: "https://github.com"
updatedDate: 2026-11-03
---

Servicio backend auxiliar diseñado para funcionar en un servidor local o VPS pequeño.
Permite enviar notas rápidas vía Telegram o API REST para que un agente las formatee en Markdown con frontmatter válido y las guarde en `src/content/`.

