from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.ingest import router as ingest_router

app = FastAPI(
    title="Logbook Automation Engine",
    description="Backend de ingesta de contenido y redacción automatizada para el jardín digital.",
    version="0.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(ingest_router, prefix="/api/ingest", tags=["Ingest"])

@app.get("/health")
def health_check():
    return {
        "status": "nominal",
        "service": "logbook-backend",
        "version": "0.1.0"
    }

