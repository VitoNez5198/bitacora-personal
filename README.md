# Bitácora Personal & Jardín Digital 🌿

Un jardín digital y bitácora personal modular con estética de terminal sobria, minimalismo funcional y enfoque en **divulgación, curiosidades, ciencia, historia y pasatiempos**. 

Cero clichés visuales de IA, 0 KB de JavaScript innecesario y contenido 100% en texto plano versionado en Git.

---

## 🏛️ Estructura de Secciones

```
proyecto_blog/
├── frontend/
│   ├── src/
│   │   ├── content/
│   │   │   ├── notas/          # [~/notas] (/) Apuntes rápidos, trucos, ideas y TILs
│   │   │   ├── historias/      # [~/historias] (/historias) Crónicas y relatos en profundidad
│   │   │   ├── curiosidades/   # [~/curiosidades] (/curiosidades) Hechos insólitos, dinosaurios y ciencia
│   │   │   └── rincon/         # [~/rincon] (/rincon) Pokémon TCG, pasatiempos y scripts personales
│   │   ├── layouts/
│   │   │   └── BaseLayout.astro # Shell con terminal prompt header y responsive móvil
│   │   └── styles/
│   │       └── global.css      # Paleta carbón (#0a0c10), acentos consola y tipografía
│   └── astro.config.mjs
│
├── backend/
│   ├── app/
│   │   ├── telegram_bot.py     # Bot @BlogVitobot con Gemini multimodal (audio & texto)
│   │   ├── api/ingest.py       # API REST de ingesta
│   │   └── main.py             # Servidor FastAPI
│   └── requirements.txt
└── README.md
```

---

## 🎙️ Ingesta por Voz desde el Móvil (Telegram Bot)

El repositorio incluye un bot privado en Telegram (**`@BlogVitobot`**) conectado a la API de **Gemini**:
1. Envías una nota de voz o texto al bot con cualquier idea, anécdota o hecho curioso.
2. Gemini escucha el audio, complementa los datos históricos/científicos faltantes (fact-checking), y redacta la entrada en Markdown limpio.
3. El bot guarda automáticamente el archivo en la colección que corresponde y ejecuta `git commit & push` a GitHub `main`.

---

## 🚀 Puesta en Marcha en Local

### 1. Frontend (Astro)
```powershell
cd frontend
npm run dev -- --host 0.0.0.0
```
> En tu PC: `http://localhost:4321`  
> En tu móvil (mismo Wi-Fi): `http://192.168.4.42:4321`

### 2. Bot de Telegram & Backend (FastAPI)
```powershell
cd backend
.\venv\Scripts\python.exe -u app\telegram_bot.py
```
