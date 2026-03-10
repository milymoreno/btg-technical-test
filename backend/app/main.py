from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.infrastructure.api.routes import router as users_router
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(
    title="Prueba Técnica API - Usuarios",
    description="API CRUD de usuarios desarrollada con FastAPI y Arquitectura Hexagonal.",
    version="1.0.0",
)

# Configurar CORS (necesario si el front se comunica desde otro dominio local o en ECS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Update for production security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users_router, prefix="/api")

@app.get("/", tags=["Health"])
def health_check():
    return {"status": "ok", "message": "API running"}
