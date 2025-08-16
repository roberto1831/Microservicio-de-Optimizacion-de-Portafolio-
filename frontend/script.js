// Detecta si el frontend está sirviéndose desde el mismo backend (puerto 8000)
const sameBackend =
  location.origin.startsWith("http://127.0.0.1:8000") ||
  location.origin.startsWith("http://localhost:8000");

// Si está en el mismo host:puerto (ej. montado en /ui), usa ruta relativa.
// Si está en otro (ej. http.server en 5500), apúntalo al backend local en 8000.
const API_URL = sameBackend ? "/optimizar" : "http://127.0.0.1:8000/optimizar";

const body = document.getElementById("proyectos-body");
const addBtn = document.getElementById("add-row");
const limpiarBtn = document.getElementById("limpiar");
const calcularBtn = document.getElementById("calcular");
const resultadoCard = document.getElementById("resultado-card");
const resultadosDiv = document.getElementById("resultados");
const errorCard = document.getElementById("error-card");
const errorText = document.getElementById("error-text");

function addRow(nombre = "", peso = "", ganancia = "") {
  const tr = document.createElement("tr");
  tr.innerHTML = `
    <td><input type="text" placeholder="ID/Nombre" value="${nombre}"></td>
    <td><input type="number" min="1" step="1" placeholder="Costo" value="${peso}"></td>
    <td><input type="number" step="1" placeholder="Ganancia" value="${ganancia}"></td>
    <td><button class="remove">✕</button></td>
  `;
  tr.querySelector(".remove").addEventListener("click", () => tr.remove());
  body.appendChild(tr);
}

function collectPayload() {
  const capacidad = Number(document.getElementById("capacidad").value);
  const rows = [...body.querySelectorAll("tr")];

  const objetos = rows.map((r, idx) => {
    const [nombre, peso, ganancia] = [...r.querySelectorAll("input")].map(i => i.value);
    return {
      nombre: String(nombre || "").trim(),
      peso: Number(peso),
      ganancia: Number(ganancia)
    };
  });

  return { capacidad, objetos };
}

function validarPayload(payload) {
  if (!Number.isFinite(payload.capacidad) || payload.capacidad < 0) {
    throw new Error("La 'capacidad' debe ser un número ≥ 0.");
  }
  if (!Array.isArray(payload.objetos) || payload.objetos.length === 0) {
    throw new Error("Debes ingresar al menos un proyecto.");
  }
  for (let i = 0; i < payload.objetos.length; i++) {
    const o = payload.objetos[i];
    if (!o.nombre) throw new Error(`El proyecto #${i + 1} debe tener 'nombre'.`);
    if (!Number.isFinite(o.peso) || o.peso <= 0) throw new Error(`El 'peso' del proyecto #${i + 1} debe ser > 0.`);
    if (!Number.isFinite(o.ganancia) || o.ganancia < 0) throw new Error(`La 'ganancia' del proyecto #${i + 1} debe ser ≥ 0.`);
  }
}

async function calcular() {
  try {
    errorCard.hidden = true;
    resultadosDiv.innerHTML = "";
    resultadoCard.hidden = true;

    const payload = collectPayload();
    validarPayload(payload);

    const res = await fetch(API_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });

    let data;
    try {
      data = await res.json();
    } catch {
      throw new Error(`Respuesta inválida del servidor (HTTP ${res.status}).`);
    }

    if (!res.ok) {
      throw new Error(data.detail || `Error del servidor (HTTP ${res.status}).`);
    }

    // Pintar resultados
    resultadoCard.hidden = false;
    const table = document.createElement("table");
    table.className = "result-table";
    table.innerHTML = `
      <thead>
        <tr><th>Seleccionados</th><th>Ganancia total</th><th>Peso total</th></tr>
      </thead>
      <tbody>
        <tr>
          <td>${(data.seleccionados && data.seleccionados.join(", ")) || "-"}</td>
          <td><span class="badge">$ ${data.ganancia_total}</span></td>
          <td><span class="badge">${data.peso_total}</span></td>
        </tr>
      </tbody>
    `;
    resultadosDiv.appendChild(table);
  } catch (err) {
    errorText.textContent = err.message || "Error desconocido";
    errorCard.hidden = false;
  }
}

addBtn.addEventListener("click", () => addRow());
limpiarBtn.addEventListener("click", () => {
  body.innerHTML = "";
  document.getElementById("capacidad").value = 0;
});
calcularBtn.addEventListener("click", calcular);

// Cargamos filas de ejemplo
[
  ["Fondo_A", 2000, 1500],
  ["Fondo_B", 4000, 3500],
  ["Fondo_C", 5000, 4000],

].forEach(([n,p,g]) => addRow(n,p,g));
