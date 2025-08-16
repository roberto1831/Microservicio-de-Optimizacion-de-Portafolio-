from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path

from .models import PeticionOptimizar, RespuestaOptimizar
from .optimizer import knapsack_01, validar_items_crudos, KnapsackItem

app = FastAPI(
    title="Microservicio de Optimización de Portafolio",
    version="1.0.0",
    description="Endpoint /optimizar que resuelve un problema de mochila 0/1 con Programación Dinámica"
)

# CORS (permitimos todo para facilitar pruebas con el frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# === Servir el frontend como estático en /ui ===
# Estructura esperada: C:\examen_final\{backend, frontend}
FRONTEND_DIR = Path(__file__).resolve().parents[2] / "frontend"
app.mount("/ui", StaticFiles(directory=str(FRONTEND_DIR), html=True), name="ui")

@app.post("/optimizar", response_model=RespuestaOptimizar, tags=["Optimización"])
def optimizar(payload: PeticionOptimizar):
    try:
        items = validar_items_crudos([o.dict() for o in payload.objetos])
        seleccionados, ganancia_total, peso_total = knapsack_01(payload.capacidad, items)
        return RespuestaOptimizar(
            seleccionados=seleccionados,
            ganancia_total=int(ganancia_total),
            peso_total=int(peso_total)
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error interno: " + str(e))

@app.get("/", tags=["Salud"])
def saludo():
    return {"status": "ok", "mensaje": "Microservicio activo. Visita /docs para Swagger UI."}
