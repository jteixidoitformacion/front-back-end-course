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
- [ ] Schemas, CRUD y endpoints `/api/v1/facturas`.
- [ ] Autenticación (login + JWT) y usar el usuario autenticado en la auditoría.
- [ ] Migraciones con Alembic.
- [ ] Frontend. Crear un frontend Rect sobre la carpeta "frontend/"

## Fase 3: Pruebas y Despliegue
- [x] Pruebas de integración de la API (pytest).
- [ ] Empaquetado y distribución (Docker).
