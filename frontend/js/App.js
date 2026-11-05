import { html, useState, useEffect, useCallback } from "./lib.js";
import { ToastProvider } from "./components/Toast.js";
import { ClientesPage } from "./pages/ClientesPage.js";
import { FacturasPage } from "./pages/FacturasPage.js";

const SECCIONES = {
  clientes: { titulo: "Clientes", icono: "👥", Page: ClientesPage },
  facturas: { titulo: "Facturas", icono: "🧾", Page: FacturasPage },
};

function seccionActual() {
  const s = window.location.hash.replace(/^#\/?/, "");
  return SECCIONES[s] ? s : "clientes";
}

export function App() {
  const [seccion, setSeccion] = useState(seccionActual);

  useEffect(() => {
    const onHash = () => setSeccion(seccionActual());
    window.addEventListener("hashchange", onHash);
    return () => window.removeEventListener("hashchange", onHash);
  }, []);

  const ir = useCallback((s) => {
    window.location.hash = `/${s}`;
  }, []);

  const { Page } = SECCIONES[seccion];

  return html`
    <${ToastProvider}>
      <div className="layout">
        <aside className="sidebar">
          <div className="brand">
            <span className="brand-logo">G</span>
            <span>Gestión</span>
          </div>
          <nav>
            ${Object.entries(SECCIONES).map(
              ([key, s]) => html`
                <a
                  key=${key}
                  href=${`#/${key}`}
                  className=${`nav-item ${seccion === key ? "active" : ""}`}
                  onClick=${(e) => { e.preventDefault(); ir(key); }}
                >
                  <span className="nav-icon">${s.icono}</span>${s.titulo}
                </a>
              `
            )}
          </nav>
          <div className="sidebar-footer">API · :9989/api/v1</div>
        </aside>
        <main className="content">
          <${Page} key=${seccion} />
        </main>
      </div>
    <//>
  `;
}
