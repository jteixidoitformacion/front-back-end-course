// El frontend se sirve en el puerto 9988 y la API (FastAPI) en el 9989 del mismo host.
export const API_URL = `${window.location.protocol}//${window.location.hostname}:9989/api/v1`;

// Usuario enviado en la cabecera X-User para los campos de auditoría.
export const AUDIT_USER = "frontend";
