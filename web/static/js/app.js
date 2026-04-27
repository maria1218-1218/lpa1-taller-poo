/* ── State ── */
let currentMuebles  = [];
let currentComedores = [];
let sellTargetId    = null;

/* ── Type icons ── */
const ICONS = {
  Silla: '🪑', Sillon: '🛋️', Sofa: '🛋️', Cama: '🛏️',
  SofaCama: '🛏️', Mesa: '🪞', Escritorio: '💻', Armario: '🗄️', Cajonera: '📦',
};

/* ── Color-dot helper ── */
function colorDot(name) {
  const map = {
    negro:'#1a1a1a', blanco:'#f0f0f0', gris:'#888', cafe:'#8B5E3C',
    caoba:'#6B2D1F', roble:'#9E6B3A', marron:'#7B4F2E', nogal:'#5C3317',
    azul:'#3498db', verde:'#27ae60', rojo:'#e74c3c', beige:'#d4b896',
    transparente:'#d0ecf7', gris_oscuro:'#555',
  };
  const key = (name || '').toLowerCase()
    .normalize('NFD').replace(/[̀-ͯ]/g, '').replace(/\s+/g, '_');
  return map[key] || '#c0b090';
}

/* ── Number formatter ── */
const fmt = n => Number(n).toLocaleString('es-CO');

/* ── Debounce ── */
function debounce(fn, ms) {
  let t;
  return function(...a) { clearTimeout(t); t = setTimeout(() => fn.apply(this, a), ms); };
}

/* ═══════════════════════════════════════════
   TAB NAVIGATION
═══════════════════════════════════════════ */
document.querySelectorAll('.nav-tab').forEach(tab => {
  tab.addEventListener('click', () => {
    document.querySelectorAll('.nav-tab').forEach(t => t.classList.remove('active'));
    document.querySelectorAll('.tab-pane').forEach(p => p.classList.remove('active'));
    tab.classList.add('active');
    const name = tab.dataset.tab;
    document.getElementById(`tab-${name}`).classList.add('active');
    ({ catalogo: loadInventario, comedores: loadComedores,
       estadisticas: loadEstadisticas, ventas: loadVentas })[name]?.();
  });
});

/* ── Global search ── */
document.getElementById('global-search').addEventListener('input', debounce(function () {
  if (document.querySelector('.nav-tab.active')?.dataset.tab !== 'catalogo') return;
  const q = this.value.trim();
  if (q) {
    fetch(`/api/buscar?q=${encodeURIComponent(q)}`)
      .then(r => r.json()).then(renderFurnitureGrid);
  } else {
    loadInventario();
  }
}, 280));

/* ═══════════════════════════════════════════
   CATÁLOGO
═══════════════════════════════════════════ */
async function loadInventario() {
  const grid = document.getElementById('furniture-grid');
  grid.innerHTML = '<div class="loading">Cargando muebles...</div>';
  try {
    const data = await fetch('/api/inventario').then(r => r.json());
    currentMuebles = data;
    renderFurnitureGrid(data);
    document.getElementById('catalogo-count').textContent =
      `${data.length} mueble${data.length !== 1 ? 's' : ''} en inventario`;
  } catch {
    grid.innerHTML = '<div class="loading">Error al cargar el inventario.</div>';
  }
}

function renderFurnitureGrid(list) {
  const grid = document.getElementById('furniture-grid');
  if (!list.length) {
    grid.innerHTML = `<div class="empty-state">
      <div class="empty-icon">📭</div><p>No se encontraron muebles</p></div>`;
    return;
  }
  grid.innerHTML = list.map(m => `
    <div class="furniture-card">
      <div class="card-header">
        <div class="card-type-icon">${ICONS[m.tipo] || '🪑'}</div>
        <div>
          <div class="card-type-name">${m.tipo}</div>
          <div class="card-title">${m.nombre}</div>
        </div>
      </div>
      <div class="card-body">
        <div class="card-props">
          <div class="prop-row">
            <span class="prop-label">Material</span>
            <span class="prop-value">${m.material}</span>
          </div>
          <div class="prop-row">
            <span class="prop-label">Color</span>
            <span class="prop-value">
              <span class="color-dot" style="background:${colorDot(m.color)}"></span>${m.color}
            </span>
          </div>
          <div class="prop-row">
            <span class="prop-label">Precio base</span>
            <span class="prop-value">$${fmt(m.precio_base)}</span>
          </div>
        </div>
        <div class="price-badge">$${fmt(m.precio_final)}
          ${m.precio_final !== m.precio_base
            ? `<small>(base $${fmt(m.precio_base)})</small>` : ''}
        </div>
      </div>
      <div class="card-footer">
        <button class="btn btn-outline" onclick="openDetail(${m.id})">Ver</button>
        <button class="btn btn-primary" onclick="openSell(${m.id})">Vender</button>
        <button class="btn btn-danger"  onclick="deleteMueble(${m.id})">✕</button>
      </div>
    </div>`).join('');
}

/* ── Filters ── */
function applyFilters() {
  const p = new URLSearchParams();
  const tipo     = document.getElementById('filter-tipo').value;
  const material = document.getElementById('filter-material').value;
  const min      = document.getElementById('filter-min').value;
  const max      = document.getElementById('filter-max').value;
  if (tipo)     p.set('tipo', tipo);
  if (material) p.set('material', material);
  if (min)      p.set('min_precio', min);
  if (max)      p.set('max_precio', max);
  fetch(`/api/buscar?${p}`).then(r => r.json()).then(renderFurnitureGrid);
}

function clearFilters() {
  ['filter-tipo','filter-material','filter-min','filter-max']
    .forEach(id => { document.getElementById(id).value = ''; });
  loadInventario();
}

/* ═══════════════════════════════════════════
   COMEDORES
═══════════════════════════════════════════ */
async function loadComedores() {
  const grid = document.getElementById('comedores-grid');
  grid.innerHTML = '<div class="loading">Cargando comedores...</div>';
  try {
    const data = await fetch('/api/comedores').then(r => r.json());
    currentComedores = data;
    document.getElementById('comedores-count').textContent =
      `${data.length} set${data.length !== 1 ? 's' : ''} disponible${data.length !== 1 ? 's' : ''}`;
    if (!data.length) {
      grid.innerHTML = `<div class="empty-state">
        <div class="empty-icon">🍽️</div><p>No hay comedores disponibles</p></div>`;
      return;
    }
    grid.innerHTML = data.map(c => `
      <div class="comedor-card">
        <div class="comedor-header">
          <div class="comedor-icon">🍽️</div>
          <div class="comedor-name">${c.nombre}</div>
          <div class="comedor-sub">${c.numero_sillas} sillas · Mesa incluida</div>
        </div>
        <div class="comedor-body">
          <div class="comedor-price">$${fmt(c.precio_total)}</div>
          ${c.tiene_descuento
            ? '<span class="discount-badge">✓ 5% desc. por set completo</span>' : ''}
          <div class="card-props" style="margin-top:10px">
            <div class="prop-row">
              <span class="prop-label">Mesa</span>
              <span class="prop-value">$${fmt(c.precio_mesa)}</span>
            </div>
            <div class="prop-row">
              <span class="prop-label">Sillas (total)</span>
              <span class="prop-value">$${fmt(c.precio_sillas)}</span>
            </div>
          </div>
          <button class="btn btn-outline comedor-detail-btn"
            onclick="openComedorDetail(${c.id})">Ver detalles</button>
        </div>
      </div>`).join('');
  } catch {
    grid.innerHTML = '<div class="loading">Error al cargar comedores.</div>';
  }
}

/* ═══════════════════════════════════════════
   ESTADÍSTICAS
═══════════════════════════════════════════ */
async function loadEstadisticas() {
  try {
    const d = await fetch('/api/estadisticas').then(r => r.json());

    document.getElementById('stats-grid').innerHTML = `
      <div class="stat-card">
        <div class="stat-icon blue">📦</div>
        <div><div class="stat-value">${d.total_muebles}</div>
             <div class="stat-label">Total Muebles</div></div>
      </div>
      <div class="stat-card">
        <div class="stat-icon green">💰</div>
        <div><div class="stat-value">$${fmt(Math.round(d.valor_inventario))}</div>
             <div class="stat-label">Valor Inventario</div></div>
      </div>
      <div class="stat-card">
        <div class="stat-icon orange">🛍️</div>
        <div><div class="stat-value">${d.ventas_realizadas}</div>
             <div class="stat-label">Ventas Realizadas</div></div>
      </div>
      <div class="stat-card">
        <div class="stat-icon purple">🍽️</div>
        <div><div class="stat-value">${d.total_comedores}</div>
             <div class="stat-label">Sets de Comedor</div></div>
      </div>`;

    const tipos  = d.tipos_muebles || {};
    const maxVal = Math.max(...Object.values(tipos), 1);
    document.getElementById('chart-tipos').innerHTML =
      Object.entries(tipos).sort((a,b) => b[1]-a[1]).map(([tipo, cnt]) => `
        <div class="bar-item">
          <div class="bar-label">
            <span>${ICONS[tipo] || ''} ${tipo}</span>
            <span class="bar-count">${cnt}</span>
          </div>
          <div class="bar-track">
            <div class="bar-fill" style="width:${(cnt/maxVal)*100}%"></div>
          </div>
        </div>`).join('') || '<p style="color:var(--text-light);font-size:13px">Sin datos</p>';

    document.getElementById('store-summary').innerHTML = `
      <div class="summary-row">
        <span class="summary-label">Precio promedio</span>
        <span class="summary-value">$${fmt(d.precio_promedio || 0)}</span>
      </div>
      <div class="summary-row">
        <span class="summary-label">Mueble más caro</span>
        <span class="summary-value">${d.mueble_mas_caro || 'N/A'}</span>
      </div>
      <div class="summary-row">
        <span class="summary-label">Mueble más barato</span>
        <span class="summary-value">${d.mueble_mas_barato || 'N/A'}</span>
      </div>
      <div class="summary-row">
        <span class="summary-label">Ingresos por ventas</span>
        <span class="summary-value">$${fmt(d.ingresos_totales || 0)}</span>
      </div>
      <div class="summary-row">
        <span class="summary-label">Descuentos activos</span>
        <span class="summary-value">${d.descuentos_activos || 0}</span>
      </div>`;
  } catch (e) { console.error(e); }
}

/* ═══════════════════════════════════════════
   VENTAS
═══════════════════════════════════════════ */
async function loadVentas() {
  try {
    const data   = await fetch('/api/ventas').then(r => r.json());
    const ventas = data.ventas || [];

    document.getElementById('ventas-count').textContent =
      `${ventas.length} venta${ventas.length !== 1 ? 's' : ''} registrada${ventas.length !== 1 ? 's' : ''}`;

    document.getElementById('ventas-summary').innerHTML = `
      <div class="ventas-stat">
        <div class="ventas-stat-label">Total ventas</div>
        <div class="ventas-stat-value">${ventas.length}</div>
      </div>
      <div class="ventas-stat">
        <div class="ventas-stat-label">Ingresos totales</div>
        <div class="ventas-stat-value">$${fmt(data.total || 0)}</div>
      </div>`;

    if (!ventas.length) {
      document.getElementById('ventas-table-container').innerHTML =
        `<div class="empty-state"><div class="empty-icon">🛒</div>
         <p>Aún no se han registrado ventas</p></div>`;
      return;
    }

    document.getElementById('ventas-table-container').innerHTML = `
      <div class="table-wrapper">
        <table>
          <thead><tr>
            <th>#</th><th>Mueble</th><th>Tipo</th><th>Cliente</th>
            <th>P. Original</th><th>Descuento</th><th>P. Final</th>
          </tr></thead>
          <tbody>
            ${ventas.map((v,i) => `<tr>
              <td>${i+1}</td>
              <td><strong>${v.mueble}</strong></td>
              <td><span class="badge badge-success">${v.tipo}</span></td>
              <td>${v.cliente}</td>
              <td>$${fmt(v.precio_original)}</td>
              <td>${v.descuento > 0
                ? `<span class="badge badge-warning">${v.descuento.toFixed(1)}%</span>`
                : '—'}</td>
              <td><strong>$${fmt(v.precio_final)}</strong></td>
            </tr>`).join('')}
          </tbody>
        </table>
      </div>`;
  } catch (e) { console.error(e); }
}

/* ═══════════════════════════════════════════
   DETAIL MODAL
═══════════════════════════════════════════ */
function openDetail(id) {
  const m = currentMuebles.find(x => x.id === id);
  if (!m) return;

  document.getElementById('modal-detail-title').textContent =
    `${ICONS[m.tipo] || ''} ${m.nombre}`;
  document.getElementById('modal-detail-body').innerHTML =
    `<pre class="detail-description">${m.descripcion}</pre>`;

  const btnDel  = document.getElementById('modal-detail-delete');
  const btnSell = document.getElementById('modal-detail-sell');
  btnDel.style.display  = '';
  btnSell.style.display = '';
  btnDel.onclick  = () => { closeModal('modal-detail'); deleteMueble(id); };
  btnSell.onclick = () => { closeModal('modal-detail'); openSell(id); };
  openModal('modal-detail');
}

function openComedorDetail(id) {
  const c = currentComedores.find(x => x.id === id);
  if (!c) return;

  document.getElementById('modal-detail-title').textContent = `🍽️ ${c.nombre}`;
  document.getElementById('modal-detail-body').innerHTML =
    `<pre class="detail-description">${c.descripcion}</pre>`;

  document.getElementById('modal-detail-delete').style.display = 'none';
  document.getElementById('modal-detail-sell').style.display   = 'none';
  openModal('modal-detail');
}

/* ═══════════════════════════════════════════
   SELL MODAL
═══════════════════════════════════════════ */
function openSell(id) {
  const m = currentMuebles.find(x => x.id === id);
  if (!m) return;
  sellTargetId = id;
  document.getElementById('sell-mueble-info').innerHTML =
    `<strong>${m.nombre}</strong>
     <div class="price">$${fmt(m.precio_final)}</div>`;
  document.getElementById('sell-cliente').value = '';
  openModal('modal-sell');
}

async function confirmSell() {
  const cliente = document.getElementById('sell-cliente').value.trim() || 'Cliente Anónimo';
  try {
    const res = await fetch('/api/ventas', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ indice: sellTargetId, cliente }),
    });
    const data = await res.json();
    if (!res.ok) { showToast('error', data.error || 'Error al vender'); return; }
    showToast('success', `✓ Venta: ${data.mueble} — $${fmt(data.precio_final)}`);
    closeModal('modal-sell');
    loadInventario();
  } catch { showToast('error', 'Error de conexión'); }
}

/* ═══════════════════════════════════════════
   DELETE
═══════════════════════════════════════════ */
async function deleteMueble(id) {
  if (!confirm('¿Eliminar este mueble del inventario?')) return;
  try {
    const res = await fetch(`/api/inventario/${id}`, { method: 'DELETE' });
    const data = await res.json();
    if (!res.ok) { showToast('error', data.error || 'Error'); return; }
    showToast('success', '✓ Mueble eliminado');
    loadInventario();
  } catch { showToast('error', 'Error de conexión'); }
}

/* ═══════════════════════════════════════════
   ADD MUEBLE MODAL
═══════════════════════════════════════════ */
document.getElementById('btn-add').addEventListener('click', () => {
  document.getElementById('form-add-mueble').reset();
  document.getElementById('dynamic-fields').innerHTML = '';
  openModal('modal-add');
});

const DYNAMIC_FIELDS = {
  Silla: `
    <div class="dynamic-section-title">Opciones de Silla</div>
    <div class="form-group">
      <label>Material tapizado</label>
      <input type="text" id="add-material_tapizado" placeholder="tela, cuero...">
    </div>
    <div class="form-check"><label>
      <input type="checkbox" id="add-tiene_respaldo" checked> Con respaldo
    </label></div>
    <div class="form-check"><label>
      <input type="checkbox" id="add-altura_regulable"> Altura regulable
    </label></div>
    <div class="form-check"><label>
      <input type="checkbox" id="add-tiene_ruedas"> Con ruedas
    </label></div>`,

  Sillon: `
    <div class="dynamic-section-title">Opciones de Sillón</div>
    <div class="form-group">
      <label>Material tapizado</label>
      <input type="text" id="add-material_tapizado" placeholder="tela, cuero..." value="tela">
    </div>
    <div class="form-check"><label>
      <input type="checkbox" id="add-tiene_brazos" checked> Con brazos
    </label></div>`,

  Sofa: `
    <div class="dynamic-section-title">Opciones de Sofá</div>
    <div class="form-row">
      <div class="form-group">
        <label>Capacidad (personas)</label>
        <input type="number" id="add-capacidad_personas" min="2" max="8" value="3">
      </div>
      <div class="form-group">
        <label>Material tapizado</label>
        <input type="text" id="add-material_tapizado" value="tela">
      </div>
    </div>
    <div class="form-check"><label>
      <input type="checkbox" id="add-es_modular"> Modular
    </label></div>`,

  Cama: `
    <div class="dynamic-section-title">Opciones de Cama</div>
    <div class="form-group">
      <label>Tamaño</label>
      <select id="add-tamaño">
        <option value="single">Single</option>
        <option value="double">Double</option>
        <option value="queen" selected>Queen</option>
        <option value="king">King</option>
      </select>
    </div>
    <div class="form-check"><label>
      <input type="checkbox" id="add-tiene_almacenamiento"> Con almacenamiento
    </label></div>
    <div class="form-check"><label>
      <input type="checkbox" id="add-es_electrica"> Eléctrica
    </label></div>`,

  SofaCama: `
    <div class="dynamic-section-title">Opciones de Sofá-Cama</div>
    <div class="form-row">
      <div class="form-group">
        <label>Capacidad (sofá)</label>
        <input type="number" id="add-capacidad_personas" min="2" max="6" value="3">
      </div>
      <div class="form-group">
        <label>Tamaño cama</label>
        <select id="add-tamaño_cama">
          <option value="single">Single</option>
          <option value="double">Double</option>
          <option value="queen" selected>Queen</option>
          <option value="king">King</option>
        </select>
      </div>
    </div>
    <div class="form-row">
      <div class="form-group">
        <label>Material tapizado</label>
        <input type="text" id="add-material_tapizado" value="tela">
      </div>
      <div class="form-group">
        <label>Mecanismo</label>
        <select id="add-mecanismo_conversion">
          <option value="plegable">Plegable</option>
          <option value="corredizo">Corredizo</option>
          <option value="electrico">Eléctrico</option>
        </select>
      </div>
    </div>
    <div class="form-check"><label>
      <input type="checkbox" id="add-incluye_colchon" checked> Incluye colchón
    </label></div>`,

  Mesa: `
    <div class="dynamic-section-title">Dimensiones</div>
    <div class="form-row">
      <div class="form-group">
        <label>Largo (cm)</label>
        <input type="number" id="add-largo" min="1" value="120">
      </div>
      <div class="form-group">
        <label>Ancho (cm)</label>
        <input type="number" id="add-ancho" min="1" value="80">
      </div>
    </div>
    <div class="form-row">
      <div class="form-group">
        <label>Alto (cm)</label>
        <input type="number" id="add-alto" min="1" value="75">
      </div>
      <div class="form-group">
        <label>Material superficie</label>
        <input type="text" id="add-material_superficie" value="madera">
      </div>
    </div>`,

  Escritorio: `
    <div class="dynamic-section-title">Dimensiones y opciones</div>
    <div class="form-row">
      <div class="form-group">
        <label>Largo (cm)</label>
        <input type="number" id="add-largo" min="1" value="120">
      </div>
      <div class="form-group">
        <label>Ancho (cm)</label>
        <input type="number" id="add-ancho" min="1" value="60">
      </div>
    </div>
    <div class="form-row">
      <div class="form-group">
        <label>Alto (cm)</label>
        <input type="number" id="add-alto" min="1" value="75">
      </div>
      <div class="form-group">
        <label>Material superficie</label>
        <input type="text" id="add-material_superficie" value="madera">
      </div>
    </div>
    <div class="form-group">
      <label>Número de cajones</label>
      <input type="number" id="add-numero_cajones" min="0" value="2">
    </div>
    <div class="form-check"><label>
      <input type="checkbox" id="add-tiene_cajonera"> Cajonera integrada
    </label></div>
    <div class="form-check"><label>
      <input type="checkbox" id="add-altura_regulable"> Altura regulable
    </label></div>`,

  Armario: `
    <div class="dynamic-section-title">Opciones de Armario</div>
    <div class="form-row">
      <div class="form-group">
        <label>Capacidad (m³)</label>
        <input type="number" id="add-capacidad_volumen" min="0.1" step="0.1" value="2.0">
      </div>
      <div class="form-group">
        <label>Compartimientos</label>
        <input type="number" id="add-numero_compartimientos" min="1" value="3">
      </div>
    </div>
    <div class="form-group">
      <label>Número de puertas</label>
      <input type="number" id="add-numero_puertas" min="1" value="2">
    </div>
    <div class="form-check"><label>
      <input type="checkbox" id="add-tiene_espejo"> Con espejo
    </label></div>`,

  Cajonera: `
    <div class="dynamic-section-title">Opciones de Cajonera</div>
    <div class="form-row">
      <div class="form-group">
        <label>Capacidad (m³)</label>
        <input type="number" id="add-capacidad_volumen" min="0.1" step="0.1" value="1.5">
      </div>
      <div class="form-group">
        <label>Número de cajones</label>
        <input type="number" id="add-numero_compartimientos" min="1" value="3">
      </div>
    </div>
    <div class="form-group">
      <label>Profundidad cajones (cm)</label>
      <input type="number" id="add-profundidad_cajones" min="1" value="45">
    </div>
    <div class="form-check"><label>
      <input type="checkbox" id="add-deslizable" checked> Cajones deslizables
    </label></div>`,
};

function updateFormFields() {
  const tipo = document.getElementById('add-tipo').value;
  document.getElementById('dynamic-fields').innerHTML = DYNAMIC_FIELDS[tipo] || '';
}

async function submitAddMueble() {
  const tipo      = document.getElementById('add-tipo').value;
  const nombre    = document.getElementById('add-nombre').value.trim();
  const material  = document.getElementById('add-material').value.trim();
  const color     = document.getElementById('add-color').value.trim();
  const precio_base = document.getElementById('add-precio').value;

  if (!tipo || !nombre || !material || !color || !precio_base) {
    showToast('warning', 'Completa todos los campos obligatorios (*)');
    return;
  }

  const data = { tipo, nombre, material, color, precio_base };
  document.querySelectorAll('#dynamic-fields input, #dynamic-fields select')
    .forEach(el => {
      const key = el.id.replace('add-', '');
      data[key] = el.type === 'checkbox' ? el.checked : el.value;
    });

  try {
    const res = await fetch('/api/inventario', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });
    const resp = await res.json();
    if (!res.ok) { showToast('error', resp.error || 'Error al agregar'); return; }
    showToast('success', `✓ ${resp.mueble.nombre} agregado al catálogo`);
    closeModal('modal-add');
    loadInventario();
  } catch { showToast('error', 'Error de conexión'); }
}

/* ═══════════════════════════════════════════
   DISCOUNT MODAL
═══════════════════════════════════════════ */
document.getElementById('btn-descuento').addEventListener('click',
  () => openModal('modal-discount'));

async function applyDiscount() {
  const categoria  = document.getElementById('discount-categoria').value;
  const porcentaje = parseInt(document.getElementById('discount-porcentaje').value);
  if (!porcentaje || porcentaje < 1 || porcentaje > 100) {
    showToast('warning', 'El porcentaje debe ser entre 1 y 100'); return;
  }
  try {
    const res = await fetch('/api/descuentos', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ categoria, porcentaje }),
    });
    const data = await res.json();
    if (!res.ok) { showToast('error', data.error); return; }
    showToast('success', `✓ ${porcentaje}% de descuento aplicado a ${categoria}`);
    closeModal('modal-discount');
  } catch { showToast('error', 'Error de conexión'); }
}

/* ═══════════════════════════════════════════
   MODAL HELPERS
═══════════════════════════════════════════ */
function openModal(id) {
  document.getElementById(id).hidden = false;
  document.body.style.overflow = 'hidden';
}
function closeModal(id) {
  document.getElementById(id).hidden = true;
  document.body.style.overflow = '';
}
document.querySelectorAll('.modal-overlay').forEach(overlay =>
  overlay.addEventListener('click', e => {
    if (e.target === overlay) closeModal(overlay.id);
  })
);
document.addEventListener('keydown', e => {
  if (e.key === 'Escape')
    document.querySelectorAll('.modal-overlay:not([hidden])')
      .forEach(m => closeModal(m.id));
});

/* ═══════════════════════════════════════════
   TOAST
═══════════════════════════════════════════ */
function showToast(type, msg) {
  const el = document.createElement('div');
  el.className = `toast ${type}`;
  el.textContent = msg;
  document.getElementById('toast-container').appendChild(el);
  setTimeout(() => {
    el.style.animation = 'toastOut .3s ease forwards';
    setTimeout(() => el.remove(), 300);
  }, 3500);
}

/* ── Bootstrap on load ── */
loadInventario();
