import { html, useState, useEffect, useMemo, useCallback, formatEur, formatFecha, hoyISO } from "../lib.js";
import { clientesApi, facturasApi } from "../api.js";
import { Modal, ConfirmDialog } from "../components/Modal.js";
import { PageHeader, Estado, Field } from "../components/ui.js";
import { useToast } from "../components/Toast.js";

const TIPOS_IVA = [21, 10, 4, 0];
const dec = (v) => (Math.round(Number(v || 0) * 100) / 100).toFixed(2);

function FacturaForm({ factura, clientes, onClose, onSaved }) {
  const notify = useToast();
  const editando = Boolean(factura);
  const [form, setForm] = useState(
    editando
      ? { fecha: factura.fecha, base: String(Number(factura.base)), iva: String(Number(factura.iva)), cliente_id: String(factura.cliente_id) }
      : { fecha: hoyISO(), base: "", iva: "", cliente_id: clientes[0] ? String(clientes[0].id) : "" }
  );
  const [guardando, setGuardando] = useState(false);
  const [error, setError] = useState("");

  const set = (campo) => (e) => setForm((f) => ({ ...f, [campo]: e.target.value }));
  const aplicarTipo = (tipo) => setForm((f) => ({ ...f, iva: dec((Number(f.base || 0) * tipo) / 100) }));
  const total = Number(form.base || 0) + Number(form.iva || 0);

  const submit = async (e) => {
    e.preventDefault();
    setError("");
    const payload = {
      fecha: form.fecha,
      base: dec(form.base),
      iva: dec(form.iva),
      cliente_id: Number(form.cliente_id),
    };
    setGuardando(true);
    try {
      if (editando) await facturasApi.update(factura.id, payload);
      else await facturasApi.create(payload);
      notify(editando ? "Factura actualizada" : "Factura creada");
      onSaved();
    } catch (err) {
      setError(err.message);
    } finally {
      setGuardando(false);
    }
  };

  return html`
    <${Modal}
      titulo=${editando ? `Editar factura #${factura.id}` : "Nueva factura"}
      onClose=${onClose}
      footer=${html`
        <button type="button" className="btn ghost" onClick=${onClose}>Cancelar</button>
        <button type="submit" form="factura-form" className="btn primary" disabled=${guardando || !clientes.length}>
          ${guardando ? "Guardando…" : "Guardar"}
        </button>
      `}
    >
      <form id="factura-form" className="form" onSubmit=${submit}>
        ${error && html`<div className="alert">${error}</div>`}
        ${!clientes.length && html`<div className="alert">Primero debes crear algún cliente.</div>`}
        <${Field} label="Cliente">
          <select value=${form.cliente_id} onChange=${set("cliente_id")} required>
            ${clientes.map((c) => html`<option key=${c.id} value=${c.id}>${c.nombre} · ${c.email}</option>`)}
          </select>
        <//>
        <${Field} label="Fecha">
          <input type="date" value=${form.fecha} onInput=${set("fecha")} required />
        <//>
        <div className="grid-2">
          <${Field} label="Base imponible (€)">
            <input type="number" min="0" step="0.01" value=${form.base} onInput=${set("base")} required />
          <//>
          <${Field} label="IVA (€)">
            <input type="number" min="0" step="0.01" value=${form.iva} onInput=${set("iva")} required />
          <//>
        </div>
        <div className="chips">
          <span className="muted small">Calcular IVA:</span>
          ${TIPOS_IVA.map(
            (t) => html`<button type="button" key=${t} className="chip" onClick=${() => aplicarTipo(t)}>${t}%</button>`
          )}
        </div>
        <div className="total-box">
          <span>Total</span>
          <strong>${formatEur(total)}</strong>
        </div>
      </form>
    <//>
  `;
}

export function FacturasPage() {
  const notify = useToast();
  const [facturas, setFacturas] = useState([]);
  const [clientes, setClientes] = useState([]);
  const [cargando, setCargando] = useState(true);
  const [error, setError] = useState("");
  const [filtroCliente, setFiltroCliente] = useState("");
  const [editando, setEditando] = useState(null);
  const [borrando, setBorrando] = useState(null);
  const [eliminando, setEliminando] = useState(false);

  const cargar = useCallback(async () => {
    setCargando(true);
    setError("");
    try {
      const [fs, cs] = await Promise.all([
        facturasApi.list({ cliente_id: filtroCliente }),
        clientesApi.list(),
      ]);
      setFacturas(fs);
      setClientes(cs);
    } catch (err) {
      setError(err.message);
    } finally {
      setCargando(false);
    }
  }, [filtroCliente]);

  useEffect(() => { cargar(); }, [cargar]);

  const nombreCliente = useMemo(() => {
    const m = new Map(clientes.map((c) => [c.id, c.nombre]));
    return (id) => m.get(id) || `Cliente #${id} (eliminado)`;
  }, [clientes]);

  const resumen = useMemo(
    () =>
      facturas.reduce(
        (acc, f) => ({ base: acc.base + Number(f.base), iva: acc.iva + Number(f.iva), total: acc.total + Number(f.total) }),
        { base: 0, iva: 0, total: 0 }
      ),
    [facturas]
  );

  const eliminar = async () => {
    setEliminando(true);
    try {
      await facturasApi.remove(borrando.id);
      notify("Factura eliminada");
      setBorrando(null);
      cargar();
    } catch (err) {
      notify(err.message, "error");
    } finally {
      setEliminando(false);
    }
  };

  return html`
    <section>
      <${PageHeader} titulo="Facturas" subtitulo=${`${facturas.length} registros`}>
        <select className="search" value=${filtroCliente} onChange=${(e) => setFiltroCliente(e.target.value)}>
          <option value="">Todos los clientes</option>
          ${clientes.map((c) => html`<option key=${c.id} value=${c.id}>${c.nombre}</option>`)}
        </select>
        <button className="btn primary" onClick=${() => setEditando("nueva")}>+ Nueva factura</button>
      <//>

      <div className="stats">
        <div className="stat"><span>Base</span><strong>${formatEur(resumen.base)}</strong></div>
        <div className="stat"><span>IVA</span><strong>${formatEur(resumen.iva)}</strong></div>
        <div className="stat accent"><span>Total facturado</span><strong>${formatEur(resumen.total)}</strong></div>
      </div>

      <div className="card">
        <${Estado}
          cargando=${cargando}
          error=${error}
          onRetry=${cargar}
          vacio=${!facturas.length && "No hay facturas"}
        >
          <table className="table">
            <thead>
              <tr>
                <th>#</th><th>Fecha</th><th>Cliente</th>
                <th className="num">Base</th><th className="num">IVA</th><th className="num">Total</th><th></th>
              </tr>
            </thead>
            <tbody>
              ${facturas.map(
                (f) => html`
                  <tr key=${f.id}>
                    <td className="muted">${f.id}</td>
                    <td>${formatFecha(f.fecha)}</td>
                    <td>${nombreCliente(f.cliente_id)}</td>
                    <td className="num">${formatEur(f.base)}</td>
                    <td className="num">${formatEur(f.iva)}</td>
                    <td className="num"><span className="badge">${formatEur(f.total)}</span></td>
                    <td className="row-actions">
                      <button className="btn ghost sm" onClick=${() => setEditando(f)}>Editar</button>
                      <button className="btn ghost sm danger-text" onClick=${() => setBorrando(f)}>Eliminar</button>
                    </td>
                  </tr>
                `
              )}
            </tbody>
          </table>
        <//>
      </div>

      ${editando &&
      html`<${FacturaForm}
        factura=${editando === "nueva" ? null : editando}
        clientes=${clientes}
        onClose=${() => setEditando(null)}
        onSaved=${() => { setEditando(null); cargar(); }}
      />`}

      ${borrando &&
      html`<${ConfirmDialog}
        titulo="Eliminar factura"
        mensaje=${`¿Seguro que quieres eliminar la factura #${borrando.id} (${formatEur(borrando.total)})?`}
        cargando=${eliminando}
        onConfirm=${eliminar}
        onClose=${() => setBorrando(null)}
      />`}
    </section>
  `;
}
