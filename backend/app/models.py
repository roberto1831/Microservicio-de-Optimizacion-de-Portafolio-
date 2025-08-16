# backend/app/models.py  (Pydantic v2)
from typing import List
from pydantic import BaseModel, Field, field_validator

class ObjetoEntrada(BaseModel):
    nombre: str = Field(..., description="Nombre del proyecto/inversión")
    peso: int = Field(..., gt=0, description="Costo requerido (entero positivo)")
    ganancia: int = Field(..., ge=0, description="Beneficio esperado (entero, puede ser 0 o positivo)")

    @field_validator("nombre")
    @classmethod
    def nombre_no_vacio(cls, v: str):
        v = v.strip()
        if not v:
            raise ValueError("El nombre no puede estar vacío")
        return v

class PeticionOptimizar(BaseModel):
    capacidad: int = Field(..., ge=0, description="Límite presupuestario total")
    objetos: List[ObjetoEntrada]

class RespuestaOptimizar(BaseModel):
    seleccionados: List[str]
    ganancia_total: int
    peso_total: int
