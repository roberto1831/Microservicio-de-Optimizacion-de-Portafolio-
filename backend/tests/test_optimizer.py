from app.optimizer import knapsack_01, KnapsackItem

def test_knapsack_basic():
    items = [
        KnapsackItem("A", 2000, 1500),
        KnapsackItem("B", 4000, 3500),
        KnapsackItem("C", 5000, 4000),
        KnapsackItem("D", 3000, 2500),
        KnapsackItem("E", 1500, 1800),
    ]
    seleccionados, ganancia, peso = knapsack_01(10000, items)
    assert ganancia == 9300
    assert peso == 10000
    assert set(seleccionados) == {"B", "C", "E"}