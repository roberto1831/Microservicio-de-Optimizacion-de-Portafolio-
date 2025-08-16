from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_api_optimizar_example():
    payload = {
        "capacidad": 8000,
        "objetos": [
            {"nombre": "Acción_Y", "peso": 2500, "ganancia": 2200},
            {"nombre": "Acción_Z", "peso": 3000, "ganancia": 2800},
            {"nombre": "Bono_Q", "peso": 1500, "ganancia": 1200},
            {"nombre": "Bono_P", "peso": 4000, "ganancia": 3000},
            {"nombre": "Acción_X", "peso": 1000, "ganancia": 800},
        ]
    }
    res = client.post("/optimizar", json=payload)
    assert res.status_code == 200, res.text
    data = res.json()
    assert data["ganancia_total"] == 6200
    assert data["peso_total"] == 7000
    assert set(data["seleccionados"]) == {"Acción_Y", "Acción_Z", "Bono_Q"}