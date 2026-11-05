# Sesión 2026-11-05 — Inicialización del backend

## Objetivo
Iniciar el proyecto: API FastAPI en `backend/` para gestionar clientes (nombre, email, password, teléfono, auditoría) en SQLite.

## Realizado
- Estructura por capas en `backend/app` (core, db, models, schemas, crud, api).
- `AuditMixin` con `created/updated/deleted _at/_by`; usuario vía cabecera `X-User`.
- CRUD `/api/v1/clientes` con soft delete, email único entre activos y normalizado.
- Contraseñas con PBKDF2-SHA256 (stdlib), nunca expuestas en respuestas.
- Tests de integración (`backend/tests`): 7/7 OK + prueba manual con uvicorn.
- Incidencia: Smart App Control bloqueó DLLs de `pydantic-core 2.50` y `sqlalchemy 2.1`; resuelto fijando `pydantic==2.12.5` y `sqlalchemy<2.1`.
- Documentación: arquitectura, entorno, roadmap, task board, ADR-0001, ejemplos.

## Siguientes pasos
Git, autenticación JWT, Alembic, frontend.
