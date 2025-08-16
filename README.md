# Microservicio de Optimización de Portafolio (Knapsack 0/1)

Implementacion el enunciado del **Examen Final - Arquitectura de Software**: microservicio con endpoint `POST /optimizar` que, dado un presupuesto (`capacidad`) y una lista de proyectos (peso/costo y ganancia), devuelve la combinación óptima que **maximiza la ganancia sin exceder el presupuesto**.

## 📁 Estructura
```
portfolio-optimizer/
├─ backend/
│  ├─ app/
│  │  ├─ main.py            # FastAPI + CORS + endpoint /optimizar
│  │  ├─ models.py          # Modelos Pydantic (request/response)
│  │  └─ optimizer.py       # Algoritmo knapsack (programación dinámica) + validaciones
│  ├─ tests/
│  │  ├─ test_api.py
│  │  └─ test_optimizer.py
│  ├─ requirements.txt
│  └─ Dockerfile
├─ frontend/
│  ├─ index.html            # UI en HTML+JS (sin frameworks)
│  ├─ script.js             # Llama al backend y renderiza resultados
│  └─ styles.css
├─ postman/
│  └─ portfolio-optimizer.postman_collection.json
└─ README.md
```

## 🚀 Backend (local)
```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # (Windows) .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```
- Swagger/OpenAPI: http://localhost:8000/docs

### Pruebas
```bash
pytest -q
```

## 🌐 Frontend
Abrimos `frontend/index.html` con un servidor estático (para habilitar `fetch`). Ejemplos:

```bash
# Opción 1 (Python)
cd frontend
python -m http.server 5500
# Abrir http://localhost:5500
```

El frontend llama a `http://localhost:8000/optimizar`. Asegúrnos que el backend corriendo.

## Docker (backend)
```bash
cd backend
docker build -t portfolio-optimizer .
docker run --rm -p 8000:8000 portfolio-optimizer
```

## Ejemplo de petición
```bash
curl -X POST http://localhost:8000/optimizar \
  -H "Content-Type: application/json" \
  -d '{
    "capacidad": 10000,
    "objetos": [
      {"nombre": "Fondo_A", "peso": 2000, "ganancia": 1500},
      {"nombre": "Fondo_B", "peso": 4000, "ganancia": 3500},
      {"nombre": "Fondo_C", "peso": 5000, "ganancia": 4000},
     
    ]
  }'
```

## Casos incluidos en pruebas
- Capacidad 10,000 → **B + C + E** (ganancia 9,300; peso 10,000)
- Capacidad 8,000 → **Acción_Y + Acción_Z + Bono_Q** (ganancia 6,200; peso 7,000)

## Validaciones y errores
- `capacidad` no puede ser negativa.
- `peso` debe ser entero **> 0**.
- `ganancia` debe ser entero **≥ 0**.
- `nombre` obligatorio y no vacío.
- Respuestas de error con HTTP 400 (detalle legible).

## ✨ Notas
- El algoritmo usa **programación dinámica** (óptimo exacto).
- La UI incluye botones *Agregar*, *Limpiar* y *Calcular*, y muestra los **seleccionados**, **ganancia_total** y **peso_total** en una tarjeta de resultados.