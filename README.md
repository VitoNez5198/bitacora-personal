# Bitácora Personal & Jardín Digital

Bitácora técnica modular con estética de terminal y minimalismo funcional. Cero clichés visuales de IA, optimizada para rendimiento extremo (0 KB de JavaScript innecesario) y portabilidad mediante texto plano en Git.

---

## 🏗️ Arquitectura

```
proyecto_blog/
├── frontend/                 # Astro + Tailwind CSS (Generación estática)
│   ├── src/
│   │   ├── content/          # Colecciones tipadas (Markdown + Frontmatter)
│   │   │   ├── til/          # / (Stream de notas rápidas y TIL)
│   │   │   ├── blog/         # /blog (Ensayos largos y reflexiones)
│   │   │   ├── lab/          # /lab (Experimentos, proyectos, scripts)
│   │   │   └── hobbies/      # /hobbies (Gaming, coleccionismo, Pokémon)
│   │   ├── layouts/          # BaseLayout con estilo de prompt shell
│   │   └── styles/           # global.css (paleta carbón, acentos consola)
│   └── astro.config.mjs
│
├── backend/                  # FastAPI (Automatización e ingesta)
│   ├── app/
│   │   ├── api/ingest.py     # Endpoint para guardar notas TIL directamente
│   │   └── main.py           # Servidor API
│   └── requirements.txt
└── README.md
```

---

## 🎨 Filosofía de Diseño

- **Paleta Dark Mode Sobria:** Fondo carbón pizarra (`#0a0c10`), superficies en `#0f1217`, bordes sutiles en `#212631`.
- **Acentos Funcionales:** Verde consola (`#3fb950`) para estado nominal/TIL, ámbar vintage (`#d29922`) para proyectos en desarrollo.
- **Tipografía:** `JetBrains Mono` / `Geist Mono` para metadatos, tags y código; sans-serif limpia y geométrica para lectura de artículos.

---

## 🚀 Puesta en Marcha

### Opción A: Desde WSL (Linux / Ubuntu en Bash)

#### 1. Frontend (Astro)
```bash
cd /mnt/d/Proyectos/proyecto_blog/frontend
npm run dev
```
> Disponible en: `http://localhost:4321`

#### 2. Backend de Ingesta (FastAPI)
```bash
cd /mnt/d/Proyectos/proyecto_blog/backend
source .venv/bin/activate
uvicorn app.main:app --reload --port 8000
```
> Swagger Docs: `http://localhost:8000/docs`
> Endpoint de Ingesta: `POST http://localhost:8000/api/ingest/til`

---

### Opción B: Desde Windows PowerShell

#### 1. Frontend (Astro)
```powershell
cd d:\Proyectos\proyecto_blog\frontend
npm run dev
```

#### 2. Backend (FastAPI)
```powershell
cd d:\Proyectos\proyecto_blog\backend
.\venv\Scripts\activate
uvicorn app.main:app --reload --port 8000
```
