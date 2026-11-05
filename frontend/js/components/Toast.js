import React from "react";
import { html, useState, useCallback } from "../lib.js";

const ToastContext = React.createContext(() => {});
export const useToast = () => React.useContext(ToastContext);

export function ToastProvider({ children }) {
  const [toasts, setToasts] = useState([]);

  const notify = useCallback((mensaje, tipo = "ok") => {
    const id = Date.now() + Math.random();
    setToasts((t) => [...t, { id, mensaje, tipo }]);
    setTimeout(() => setToasts((t) => t.filter((x) => x.id !== id)), 3500);
  }, []);

  return html`
    <${ToastContext.Provider} value=${notify}>
      ${children}
      <div className="toasts">
        ${toasts.map((t) => html`<div key=${t.id} className=${`toast ${t.tipo}`}>${t.mensaje}</div>`)}
      </div>
    <//>
  `;
}
