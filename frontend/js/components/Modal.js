import { html, useEffect } from "../lib.js";

export function Modal({ titulo, onClose, children, footer, ancho = 520 }) {
  useEffect(() => {
    const onKey = (e) => e.key === "Escape" && onClose();
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [onClose]);

  return html`
    <div className="modal-backdrop" onMouseDown=${(e) => e.target === e.currentTarget && onClose()}>
      <div className="modal" style=${{ maxWidth: `${ancho}px` }} role="dialog" aria-modal="true">
        <div className="modal-header">
          <h3>${titulo}</h3>
          <button className="icon-btn" onClick=${onClose} aria-label="Cerrar">✕</button>
        </div>
        <div className="modal-body">${children}</div>
        ${footer && html`<div className="modal-footer">${footer}</div>`}
      </div>
    </div>
  `;
}

export function ConfirmDialog({ titulo = "Confirmar", mensaje, onConfirm, onClose, cargando }) {
  return html`
    <${Modal}
      titulo=${titulo}
      onClose=${onClose}
      ancho=${420}
      footer=${html`
        <button className="btn ghost" onClick=${onClose} disabled=${cargando}>Cancelar</button>
        <button className="btn danger" onClick=${onConfirm} disabled=${cargando}>
          ${cargando ? "Eliminando…" : "Eliminar"}
        </button>
      `}
    >
      <p className="muted">${mensaje}</p>
    <//>
  `;
}
