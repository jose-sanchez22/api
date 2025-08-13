async function cargar() {
  const resp = await fetch('/api/traps');
  const data = await resp.json();
  const tbody = document.querySelector('#tabla-traps tbody');
  tbody.innerHTML = '';
  data.forEach((t, i) => {
    for (const [oid, val] of Object.entries(t)) {
      const tr = document.createElement('tr');
      tr.innerHTML = `<td>${i}</td><td>${oid}</td><td>${val}</td>
        <td><button class="btn btn-danger btn-sm" onclick="borrar(${i})">Borrar</button></td>`;
      tbody.appendChild(tr);
    }
  });
}
async function borrar(idx) {
  await fetch(`/api/traps/${idx}`, { method: 'DELETE' });
  cargar();
}
window.onload = cargar;
