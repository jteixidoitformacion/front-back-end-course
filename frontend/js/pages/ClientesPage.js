import { html, useState, useEffect, useMemo, useCallback, formatFechaHora } from "../lib.js";
import { clientesApi } from "../api.js";
import { Modal, ConfirmDialog } from "../components/Modal.js";
import { PageHeader, Estado, Field } from "../components/ui.js";
import { useToast } from "../components/Toast.js";

const VACIO = { nombre: "", email: "", telefono: "", password: "" };

function ClienteForm({ cliente, onClose, onSaved }) {
  const notify = useToast();
  const editando = Boolean(cliente);
  const [form, setForm] = useState(
    editando ? { nombre: cliente.nombre, email: cliente.email, telefono: cliente.telefono || "", password: "" } : VACIO
  );
  const [guardando, setGuardando] = useState(false);
  const [error, setError] = useState("");

  const set = (campo) => (e) => setForm((f) => ({ ...f, [campo]: e.target.value }));

  const submit = async (e) => {
    e.preventDefault();
    setError("");
    const payload = {
      nombre: form.nombre.trim(),
      email: form.email.trim(),
      telefono: form.telefono.trim() || null,
    };
    if (form.password) payload.password = form.password;

    setGuardando(true);
    try {
      if (editando) await clientesApi.update(cliente.id, payload);
      else await clientesApi.create(payload);
      notify(editando ? "Cliente actualizado" : "Cliente creado");
      onSaved();
    } catch (err) {
      setError(err.message);
    } finally {
      setGuardando(false);
    }
  };

  return html`
    <${Modal}
      titulo=${editando ? `Editar cliente #${cliente.id}` : "Nuevo cliente"}
      onClose=${onClose}
      footer=${html`
        <button type="button" className="btn ghost" onClick=${onClose}>Cancelar</button>
        <button type="submit" form="cliente-form" className="btn primary" disabled=${guardando}>
          ${guardando ? "Guardando…" : "Guardar"}
        </button>
      `}
    >
      <form id="cliente-form" className="form" onSubmit=${submit}>
        ${error && html`<div className="alert">${error}</div>`}
        <${Field} label="Nombre">
          <input value=${form.nombre} onInput=${set("nombre")} required maxLength=${150} autoFocus />
        <//>
        <${Field} label="Email">
          <input type="email" value=${form.email} onInput=${set("email")} required />
        <//>
        <${Field} label="Teléfono" hint="Opcional. Ej.: +34 600 000 000">
          <input value=${form.telefono} onInput=${set("telefono")} pattern="\\+?[0-9 ()\\-]{6,30}" />
        <//>
        <${Field} label="Contraseña" hint=${editando ? "Déjala vacía para no cambiarla" : "Mínimo 8 caracteres"}>
          <input
            type="password"
            value=${form.password}
            onInput=${set("password")}
            required=${!editando}
            minLength=${8}
            maxLength=${128}
            autoComplete="new-password"
          />
        <//>
      </form>
    <//>
  `;
}

export function ClientesPage() {
  const notify = useToast();
  const [clientes, setClientes] = useState([]);
  const [cargando, setCargando] = useState(true);
  const [error, setError] = useState("");
  const [busqueda, setBusqueda] = useState("");
  const [editando, setEditando] = useState(null); // null | "nuevo" | cliente
  const [borrando, setBorrando] = useState(null);
  const [eliminando, setEliminando] = useState(false);

  const cargar = useCallback(async () => {
    setCargando(true);
    setError("");
    try {
      setClientes(await clientesApi.list());
    } catch (err) {
      setError(err.message);
    } finally {
      setCargando(false);
    }
  }, []);

  useEffect(() => { cargar(); }, [cargar]);

  const filtrados = useMemo(() => {
    const q = busqueda.trim().toLowerCase();
    if (!q) return clientes;
    return clientes.filter((c) =>
      [c.nombre, c.email, c.telefono].some((v) => (v || "").toLowerCase().includes(q))
    );
  }, [clientes, busqueda]);

  const eliminar = async () => {
    setEliminando(true);
    try {
      await clientesApi.remove(borrando.id);
      notify("Cliente eliminado");
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
      <${PageHeader} titulo="Clientes" subtitulo=${`${clientes.length} registros`}>
        <input
          className="search"
          type="search"
          placeholder="Buscar por nombre, email o teléfono…"
          value=${busqueda}
          onInput=${(e) => setBusqueda(e.target.value)}
        />
        <button className="btn primary" onClick=${() => setEditando("nuevo")}>+ Nuevo cliente</button>
      <//>

      <div className="card">
        <${Estado}
          cargando=${cargando}
          error=${error}
          onRetry=${cargar}
          vacio=${!filtrados.length && (busqueda ? "Sin resultados para la búsqueda" : "Aún no hay clientes")}
        >
          <table className="table">
            <thead>
              <tr>
                <th>#</th><th>Nombre</th><th>Email</th><th>Teléfono</th><th>Actualizado</th><th></th>
              </tr>
            </thead>
            <tbody>
              ${filtrados.map(
                (c) => html`
                  <tr key=${c.id}>
                    <td className="muted">${c.id}</td>
                    <td>
                      <div className="cell-main">
                        <span className="avatar">${c.nombre.charAt(0).toUpperCase()}</span>${c.nombre}
                      </div>
                    </td>
                    <td>${c.email}</td>
                    <td>${c.telefono || html`<span className="muted">—</span>`}</td>
                    <td className="muted small" title=${`por ${c.updated_by}`}>${formatFechaHora(c.updated_at)}</td>
                    <td className="row-actions">
                      <button className="btn ghost sm" onClick=${() => setEditando(c)}>Editar</button>
                      <button className="btn ghost sm danger-text" onClick=${() => setBorrando(c)}>Eliminar</button>
                    </td>
                  </tr>
                `
              )}
            </tbody>
          </table>
        <//>
      </div>

      ${editando &&
      html`<${ClienteForm}
        cliente=${editando === "nuevo" ? null : editando}
        onClose=${() => setEditando(null)}
        onSaved=${() => { setEditando(null); cargar(); }}
      />`}

      ${borrando &&
      html`<${ConfirmDialog}
        titulo="Eliminar cliente"
        mensaje=${`¿Seguro que quieres eliminar a "${borrando.nombre}"?`}
        cargando=${eliminando}
        onConfirm=${eliminar}
        onClose=${() => setBorrando(null)}
      />`}
    </section>
  `;
}
