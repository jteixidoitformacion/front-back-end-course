# Sesión 2026-11-05: Frontend React (clientes y facturas)

## Petición
Crear un frontend en `frontend/` con React, sin compilación, secciones Clientes y Facturas con listado y CRUD, diseño moderno minimalista en verdes. Seguimiento: servir el frontend siempre en el puerto 9988 y arrancarlo desde `start.bat`.

## Cambios
- `frontend/` (nuevo): `index.html` (importmap React 18 + htm), `serve.py` (servidor estático :9988), `css/styles.css`, `js/` (`config.js`, `api.js`, `lib.js`, `main.js`, `App.js`, `components/`, `pages/`).
- `backend/app/core/config.py`: `CORS_ORIGINS`.
- `backend/app/main.py`: `CORSMiddleware`.
- `.scripts/start.bat`: arranca el frontend (:9988, ventana aparte) y la API (:9989).
- Documentación: arquitectura, entorno, roadmap, task board, ADR-0003, README.

## Verificación
- `pytest -q` → 16 passed.
- `serve.py` sirve `.js` como `text/javascript`.
- Preflight CORS desde `http://127.0.0.1:9988` OK (PATCH/DELETE + `X-User`).
- Render headless (Edge) de `#/clientes` y `#/facturas` con datos reales de la API.
- Ciclo CRUD (crear cliente → crear/editar/borrar factura → borrar cliente) OK; total recalculado.

## Commit propuesto
`feat(frontend): añadir frontend React sin build para clientes y facturas en el puerto 9988`
