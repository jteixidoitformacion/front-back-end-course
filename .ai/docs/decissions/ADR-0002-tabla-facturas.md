# ADR-0002: Tabla `facturas`

- **Estado:** Aceptada
- **Fecha:** 2026-11-05

## Contexto
Se necesita registrar facturas (id, fecha, base, iva, total, cliente_id, auditoría) asociadas a clientes.

## Decisión
- Modelo `Factura` en `app/models/factura.py`, reutilizando `AuditMixin` (incluye soft delete).
- Importes como `NUMERIC(12,2)` mapeados a `Decimal` (evita errores de coma flotante en Python).
- `iva` almacena el **importe** del IVA, no el porcentaje.
- `CHECK` de integridad: `base >= 0`, `iva >= 0` y `total ≈ base + iva`. Como SQLite guarda NUMERIC con afinidad REAL, la igualdad se valida con tolerancia `< 0.005`.
- `cliente_id` es FK a `clientes.id` con `ON DELETE RESTRICT` e índice. Los clientes se borran lógicamente, por lo que la restricción solo protege frente a borrados físicos.
- Se activa `PRAGMA foreign_keys=ON` en cada conexión SQLite (`app/db/database.py`); sin ello SQLite ignora las FKs.
- La tabla se crea con `create_all` (las tablas nuevas se crean en BDs existentes; Alembic sigue pendiente).

## Consecuencias
- Integridad referencial real en SQLite.
- API `/api/v1/facturas`: el **total se calcula en el servidor** (`base + iva`) al crear y actualizar; el campo `total` enviado por el cliente se ignora. Una factura solo puede asociarse a un cliente activo (si no, 422).
- Los importes se serializan en JSON como cadenas decimales (`"121.12"`), comportamiento estándar de Pydantic v2 para `Decimal`, para no perder precisión.
