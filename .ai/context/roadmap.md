# Hoja de Ruta (Roadmap)

## Fase 1: Inicialización y Definición
- [x] Definir requerimientos y alcance (API FastAPI de clientes sobre SQLite en `backend/`).
- [x] Configurar entorno base (venv, requirements, .gitignore).
- [ ] Inicializar control de versiones (git).

## Fase 2: Desarrollo Central
- [x] Modelo `Cliente` con campos de auditoría y soft delete.
- [x] CRUD REST `/api/v1/clientes`.
- [x] Hash seguro de contraseñas.
- [x] Modelo `Factura` (tabla `facturas`) con auditoría y FK a clientes.
- [x] Schemas, CRUD y endpoints `/api/v1/facturas`.
- [ ] Autenticación (login + JWT) y usar el usuario autenticado en la auditoría.
- [ ] Migraciones con Alembic.
- [x] Frontend. Crear un frontend React sobre la carpeta "frontend/" (sin build, puerto 9988).
- [x] Secciones Clientes y Facturas con listado y CRUD.
- [x] CORS en la API y arranque del frontend desde `start.bat`.

## Fase 3: Pruebas y Despliegue
- [x] Pruebas de integración de la API (pytest).
- [ ] Empaquetado y distribución (Docker).
