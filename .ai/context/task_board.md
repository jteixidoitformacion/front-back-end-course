# Tablero de Tareas (Task Board)

## Pendientes (Backlog / To-Do)
- [ ] Inicializar repositorio git y primer commit.
- [ ] Autenticación JWT (sustituir cabecera `X-User`).
- [ ] Migraciones Alembic.
- [ ] Búsqueda/filtrado de clientes en servidor (hoy el frontend filtra en local).
- [ ] Paginación en el frontend (hoy carga hasta 500 registros).
- [ ] Vendorizar React/htm para funcionar sin Internet.

## En Progreso (In Progress)
- (ninguna)

## Completado (Done)
- [x] Inicialización del andamiaje de gobernanza IA.
- [x] Estructura FastAPI en `backend/` (core, db, models, schemas, crud, api).
- [x] Modelo `Cliente` + `AuditMixin` (created/updated/deleted _at/_by).
- [x] Endpoints CRUD con soft delete y email único entre activos.
- [x] Hash PBKDF2-SHA256 de contraseñas.
- [x] Tests de integración con pytest.
- [x] Documentación `.ai/` (arquitectura, entorno, ADR-0001, ejemplos, sesión).
- [x] Script `.scripts/start.bat` para arrancar FastAPI en el puerto fijo 9989.
- [x] Tabla `facturas` (id, fecha, base, iva, total, cliente_id + auditoría) y activación de FKs en SQLite.
- [x] Tests del modelo `Factura` (`tests/test_facturas.py`).
- [x] Endpoints CRUD `/api/v1/facturas` (total calculado en servidor, filtro por cliente, soft delete) + tests de API.
- [x] Frontend React sin build (`frontend/`): Clientes y Facturas con listado y CRUD, tema verde (ADR-0003).
- [x] Servidor estático del frontend en el puerto fijo 9988 (`frontend/serve.py`) y arranque en `start.bat`.
- [x] CORS en FastAPI (`CORS_ORIGINS`).
