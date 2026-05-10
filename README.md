# 💼 Microservicio de Optimización de Portafolio (Knapsack 0/1)

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Pydantic](https://img.shields.io/badge/Pydantic-E92063?style=for-the-badge&logo=pydantic&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Pytest](https://img.shields.io/badge/Pytest-0A9EDC?style=for-the-badge&logo=pytest&logoColor=white)

> Microservicio que resuelve el problema de optimización de portafolio de inversiones usando el algoritmo **Knapsack 0/1 con programación dinámica**. Dado un presupuesto y una lista de proyectos/fondos, devuelve la combinación óptima que maximiza la ganancia sin exceder el presupuesto.

---

## 🧠 Algoritmo

Este microservicio implementa el clásico problema de la **mochila 0/1** aplicado a finanzas:

```
Entrada:  capacidad (presupuesto) + lista de proyectos {nombre, peso/costo, ganancia}
Proceso:  Programación dinámica → solución óptima exacta en O(n × W)
Salida:   Proyectos seleccionados + ganancia_total + peso_total
```

| Propiedad | Detalle |
|---|---|
| Tipo de algoritmo | Programación dinámica (óptimo exacto) |
| Complejidad temporal | O(n × W) |
| Endpoint principal | `POST /optimizar` |
| Documentación | Swagger / OpenAPI en `/docs` |

---

## 📁 Estructura del Proyecto

```
portfolio-optimizer/
├─ backend/
│  ├─ app/
│  │  ├─ main.py            # FastAPI + CORS + endpoint /optimizar
│  │  ├─ models.py          # Modelos Pydantic (request/response)
│  │  └─ optimizer.py       # Algoritmo knapsack + validaciones
│  ├─ tests/
│  │  ├─ test_api.py
│  │  └─ test_optimizer.py
│  ├─ requirements.txt
│  └─ Dockerfile
├─ frontend/
│  ├─ index.html            # UI en HTML + JS (sin frameworks)
│  ├─ script.js             # Llama al backend y renderiza resultados
│  └─ styles.css
├─ postman/
│  └─ portfolio-optimizer.postman_collection.json
└─ README.md
```

---

## 🚀 Ejecución Local

### Backend (FastAPI)

```bash
cd backend
python -m venv .venv

# Linux / Mac
source .venv/bin/activate

# Windows
.venv\Scripts\activate

pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

📄 Swagger UI disponible en: **http://localhost:8000/docs**

### Frontend

```bash
cd frontend
python -m http.server 5500
# Abrir http://localhost:5500
```

> ⚠️ El frontend llama a `http://localhost:8000/optimizar`. Asegúrate de tener el backend corriendo antes de abrir la UI.

### Pruebas

```bash
pytest -q
```

---

## 🐳 Docker

```bash
cd backend
docker build -t portfolio-optimizer .
docker run --rm -p 8000:8000 portfolio-optimizer
```

---

## 📨 Ejemplo de Uso

### Solicitud

```bash
curl -X POST http://localhost:8000/optimizar \
  -H "Content-Type: application/json" \
  -d '{
    "capacidad": 10000,
    "objetos": [
      {"nombre": "Fondo_A", "peso": 2000, "ganancia": 1500},
      {"nombre": "Fondo_B", "peso": 4000, "ganancia": 3500},
      {"nombre": "Fondo_C", "peso": 5000, "ganancia": 4000}
    ]
  }'
```

### Respuesta Esperada

```json
{
  "seleccionados": ["Fondo_B", "Fondo_C"],
  "ganancia_total": 7500,
  "peso_total": 9000
}
```

---

## 🧪 Casos de Prueba Incluidos

| Escenario | Capacidad | Resultado | Ganancia | Peso |
|---|---|---|---|---|
| Caso 1 | 10,000 | B + C + E | 9,300 | 10,000 |
| Caso 2 | 8,000 | Acción_Y + Acción_Z + Bono_Q | 6,200 | 7,000 |

---

## ✅ Validaciones y Errores

| Campo | Regla | Error |
|---|---|---|
| `capacidad` | No puede ser negativa | HTTP 400 |
| `peso` | Entero > 0 | HTTP 400 |
| `ganancia` | Entero ≥ 0 | HTTP 400 |
| `nombre` | Obligatorio y no vacío | HTTP 400 |

Todos los errores retornan **HTTP 400** con detalle legible en el body.

---

## 🖥️ Interfaz de Usuario

La UI incluye:
- ➕ Botón **Agregar** — añade proyectos a la lista
- 🗑️ Botón **Limpiar** — reinicia el formulario
- ⚡ Botón **Calcular** — llama al backend y muestra resultados
- 📊 Tarjeta de resultados con **seleccionados**, **ganancia_total** y **peso_total**

---

## 👤 Autor

**Ing. Roberto Toapanta**  
📍 Quito, Ecuador  
🔗 [GitHub](https://github.com/roberto1831) · [LinkedIn](https://linkedin.com/in/roberto1831)

---

## 📄 Licencia

Uso académico / demostrativo. No apto para producción sin revisión de seguridad.
