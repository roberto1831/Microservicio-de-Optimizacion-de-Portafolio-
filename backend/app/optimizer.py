from typing import List, Dict, Tuple

class KnapsackItem:
    def __init__(self, nombre: str, peso: int, ganancia: int):
        self.nombre = nombre
        self.peso = int(peso)
        self.ganancia = int(ganancia)

def knapsack_01(capacidad: int, items: List[KnapsackItem]) -> Tuple[List[str], int, int]:
    """
    Classic 0/1 knapsack solved with Dynamic Programming.
    Returns (selected_names, total_gain, total_weight).
    """
    n = len(items)
    if capacidad < 0:
        raise ValueError("La capacidad no puede ser negativa")
    # DP matrix: (n+1) x (capacidad+1) of max gain
    dp = [[0]*(capacidad+1) for _ in range(n+1)]
    # Build DP table
    for i in range(1, n+1):
        w = items[i-1].peso
        v = items[i-1].ganancia
        for c in range(capacidad+1):
            dp[i][c] = dp[i-1][c]
            if w <= c:
                cand = dp[i-1][c-w] + v
                if cand > dp[i][c]:
                    dp[i][c] = cand

    # Reconstruct selection
    c = capacidad
    seleccionados: List[str] = []
    peso_total = 0
    for i in range(n, 0, -1):
        if dp[i][c] != dp[i-1][c]:
            item = items[i-1]
            seleccionados.append(item.nombre)
            c -= item.peso
            peso_total += item.peso

    seleccionados.reverse()
    ganancia_total = dp[n][capacidad]
    return seleccionados, ganancia_total, peso_total

def validar_items_crudos(objetos: List[Dict]) -> List[KnapsackItem]:
    if not isinstance(objetos, list) or len(objetos) == 0:
        raise ValueError("La lista 'objetos' debe contener al menos un elemento")
    parsed: List[KnapsackItem] = []
    for idx, obj in enumerate(objetos, start=1):
        if not isinstance(obj, dict):
            raise ValueError(f"Objeto en posición {idx} no es un diccionario")
        for key in ("nombre", "peso", "ganancia"):
            if key not in obj:
                raise ValueError(f"Falta el campo requerido '{key}' en el objeto {idx}")
        try:
            peso = int(obj["peso"])
            ganancia = int(obj["ganancia"])
        except Exception:
            raise ValueError(f"'peso' y 'ganancia' deben ser enteros en el objeto {idx}")
        if peso <= 0:
            raise ValueError(f"'peso' debe ser > 0 en el objeto {idx}")
        if ganancia < 0:
            raise ValueError(f"'ganancia' no puede ser negativa en el objeto {idx}")
        nombre = str(obj["nombre"]).strip()
        if not nombre:
            raise ValueError(f"'nombre' no puede ser vacío en el objeto {idx}")
        parsed.append(KnapsackItem(nombre=nombre, peso=peso, ganancia=ganancia))
    return parsed