# ADR-0001: Stack del backend (FastAPI + SQLAlchemy 2 + SQLite)

- **Estado:** Aceptada
- **Fecha:** 2026-11-05

## Contexto
Se necesita una API para gestionar clientes (nombre, email, password, teléfono y campos de auditoría) sobre SQLite, ubicada en `backend/`.

## Decisión
- **FastAPI** como framework HTTP (validación con Pydantic v2, OpenAPI automático).
- **SQLAlchemy 2.0** (ORM tipado `Mapped`) para abstraer SQLite y facilitar migrar a otro motor cambiando `DATABASE_URL`.
- **Arquitectura por capas:** `api/routes` → `crud` → `models`, con `schemas` (Pydantic) como contrato de entrada/salida.
- **Hash de contraseñas con PBKDF2-SHA256 (stdlib `hashlib`, 600.000 iteraciones, salt aleatoria)**: sin dependencias nativas (bcrypt/passlib dan problemas con Python 3.14) y alineado con OWASP.
- **Auditoría mediante `AuditMixin`**: `created_at/by`, `updated_at/by`, `deleted_at/by`. El usuario se toma de la cabecera `X-User` (por defecto `system`) hasta que exista autenticación.
- **Borrado lógico (soft delete)**: `DELETE` rellena `deleted_at/by`; los listados excluyen borrados. Email único solo entre clientes activos (índice parcial SQLite) y normalizado a minúsculas.
- **Creación de tablas con `Base.metadata.create_all`** al arrancar (lifespan). Alembic queda pendiente para cuando el esquema evolucione.

## Consecuencias
- Cero configuración para desarrollo local; la BD `clientes.db` se crea sola.
- La cabecera `X-User` no es segura: debe sustituirse por el usuario autenticado (JWT) en una fase futura.
