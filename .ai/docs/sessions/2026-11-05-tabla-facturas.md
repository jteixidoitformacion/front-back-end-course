# Sesión 2026-11-05: Tabla facturas

## Petición
Añadir la tabla `facturas` (id, fecha, base, iva, total, cliente_id, auditoría).

## Cambios
- `backend/app/models/factura.py`: modelo `Factura` + CHECKs + FK a `clientes`.
- `backend/app/models/__init__.py`: registro de `Factura`.
- `backend/app/db/database.py`: `PRAGMA foreign_keys=ON` para SQLite.
- `backend/tests/test_facturas.py`: columnas, alta, FK inválida y total incoherente.
- Documentación: arquitectura, roadmap, task board, ADR-0002.

## Verificación
`.\.venv\Scripts\python -m pytest -q` → 11 passed.

## Commit propuesto
`feat(facturas): añadir modelo y tabla facturas con auditoría y FK a clientes`
