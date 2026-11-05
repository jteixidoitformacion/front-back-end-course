import { API_URL, AUDIT_USER } from "./config.js";

function mensajeError(status, body) {
  const detail = body?.detail;
  if (Array.isArray(detail)) {
    return detail
      .map((d) => `${(d.loc || []).filter((p) => p !== "body").join(".")}: ${d.msg}`)
      .join(" · ");
  }
  if (typeof detail === "string") return detail;
  return `Error ${status}`;
}

async function request(path, { method = "GET", body, params } = {}) {
  const url = new URL(`${API_URL}${path}`, window.location.origin);
  Object.entries(params || {}).forEach(([k, v]) => {
    if (v !== undefined && v !== null && v !== "") url.searchParams.set(k, v);
  });

  let res;
  try {
    res = await fetch(url, {
      method,
      headers: { "Content-Type": "application/json", "X-User": AUDIT_USER },
      body: body ? JSON.stringify(body) : undefined,
    });
  } catch {
    throw new Error("No se pudo conectar con la API");
  }

  if (res.status === 204) return null;
  const data = await res.json().catch(() => null);
  if (!res.ok) throw new Error(mensajeError(res.status, data));
  return data;
}

function recurso(nombre) {
  return {
    list: (params) => request(`/${nombre}`, { params: { limit: 500, ...params } }),
    get: (id) => request(`/${nombre}/${id}`),
    create: (data) => request(`/${nombre}`, { method: "POST", body: data }),
    update: (id, data) => request(`/${nombre}/${id}`, { method: "PATCH", body: data }),
    remove: (id) => request(`/${nombre}/${id}`, { method: "DELETE" }),
  };
}

export const clientesApi = recurso("clientes");
export const facturasApi = recurso("facturas");
