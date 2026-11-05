import { html } from "../lib.js";

export function PageHeader({ titulo, subtitulo, children }) {
  return html`
    <header className="page-header">
      <div>
        <h1>${titulo}</h1>
        ${subtitulo && html`<p className="muted">${subtitulo}</p>`}
      </div>
      <div className="actions">${children}</div>
    </header>
  `;
}

export function Estado({ cargando, error, vacio, onRetry, children }) {
  if (cargando) return html`<div className="empty"><div className="spinner"></div>Cargando…</div>`;
  if (error)
    return html`
      <div className="empty error">
        <p>${error}</p>
        <button className="btn ghost" onClick=${onRetry}>Reintentar</button>
      </div>
    `;
  if (vacio) return html`<div className="empty">${vacio}</div>`;
  return children;
}

export function Field({ label, error, children, hint }) {
  return html`
    <label className=${`field ${error ? "has-error" : ""}`}>
      <span className="field-label">${label}</span>
      ${children}
      ${hint && !error && html`<small className="muted">${hint}</small>`}
    </label>
  `;
}
