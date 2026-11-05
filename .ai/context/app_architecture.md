# Arquitectura de la Aplicación (Application Architecture)

## 1. Visión General
API REST en **FastAPI** ubicada en `backend/` para gestionar clientes sobre **SQLite** mediante **SQLAlchemy 2.0**. Arquitectura por capas (ver [ADR-0001](../docs/decissions/ADR-0001-stack-backend.md)).

```
backend/
├── app/
│   ├── main.py              # App FastAPI, lifespan (create_all), /health, router /api/v1
│   ├── core/
│   │   ├── config.py        # Configuración vía variables de entorno
│   │   └── security.py      # hash_password / verify_password (PBKDF2-SHA256)
│   ├── db/database.py       # engine (PRAGMA foreign_keys=ON en SQLite), SessionLocal, Base, get_db
│   ├── models/
│   │   ├── audit.py         # AuditMixin (created/updated/deleted _at/_by)
│   │   ├── cliente.py       # Modelo Cliente (tabla clientes)
│   │   └── factura.py       # Modelo Factura (tabla facturas, FK a clientes)
│   ├── schemas/             # cliente.py, factura.py (Create / Update / Read)
│   ├── crud/                # cliente.py (email único, soft delete), factura.py (total en servidor)
│   └── api/
│       ├── deps.py          # DbSession, UsuarioAuditoria (cabecera X-User)
│       └── routes/          # clientes.py, facturas.py
├── tests/                   # pytest + TestClient (BD test_clientes.db)
├── requirements.txt
├── pytest.ini
└── .env.example
```

## 2. Módulos y Componentes
- **API (`api/routes`)**: endpoints HTTP, traducción de errores de dominio a códigos HTTP (404, 409).
- **Schemas (`schemas`)**: validación de entrada (email válido, password 8-128, teléfono con patrón) y serialización de salida (sin password).
- **CRUD (`crud`)**: lógica de persistencia; normaliza email a minúsculas, hashea password, rellena auditoría, aplica soft delete.
- **Modelos (`models`)**: ORM. `AuditMixin` reutilizable por futuras entidades.
- **Core**: configuración y seguridad.

### Entidad `clientes`
| Campo | Tipo | Notas |
|---|---|---|
| id | INTEGER PK | autoincremental |
| nombre | VARCHAR(150) | obligatorio |
| email | VARCHAR(255) | obligatorio, minúsculas, único entre activos (índice parcial `uq_clientes_email_activo`) |
| password_hash | VARCHAR(255) | `pbkdf2_sha256$iter$salt$hash` |
| telefono | VARCHAR(30) | opcional |
| created_at / created_by | DATETIME / VARCHAR(100) | auditoría alta |
| updated_at / updated_by | DATETIME / VARCHAR(100) | auditoría modificación |
| deleted_at / deleted_by | DATETIME / VARCHAR(100) | borrado lógico (NULL = activo) |

### Entidad `facturas`
Ver [ADR-0002](../docs/decissions/ADR-0002-tabla-facturas.md). Expuesta en `/api/v1/facturas` (schemas en `schemas/factura.py`, CRUD en `crud/factura.py`, router en `api/routes/facturas.py`). El **total lo calcula el servidor** (`base + iva`); si el cliente lo envía, se ignora.

| Campo | Tipo | Notas |
|---|---|---|
| id | INTEGER PK | autoincremental |
| fecha | DATE | obligatorio |
| base | NUMERIC(12,2) | obligatorio, `>= 0` (`ck_facturas_base_no_negativa`) |
| iva | NUMERIC(12,2) | importe del IVA, obligatorio, `>= 0` (`ck_facturas_iva_no_negativo`) |
| total | NUMERIC(12,2) | obligatorio, `total = base + iva` con tolerancia 0,005 (`ck_facturas_total`) |
| cliente_id | INTEGER FK → `clientes.id` | obligatorio, indexado, `ON DELETE RESTRICT` |
| created_at/by, updated_at/by, deleted_at/by | — | auditoría vía `AuditMixin` (soft delete) |

### Endpoints (`/api/v1`)
| Método | Ruta | Descripción |
|---|---|---|
| GET | `/health` (sin prefijo) | Estado del servicio |
| GET | `/clientes?skip&limit` | Listar activos |
| GET | `/clientes/{id}` | Obtener |
| POST | `/clientes` | Crear (201, 409 si email existe) |
| PATCH | `/clientes/{id}` | Actualización parcial |
| DELETE | `/clientes/{id}` | Borrado lógico (204) |
| GET | `/facturas?skip&limit&cliente_id` | Listar activas (filtro opcional por cliente) |
| GET | `/facturas/{id}` | Obtener |
| POST | `/facturas` | Crear (201; 422 si el cliente no existe o está borrado) |
| PATCH | `/facturas/{id}` | Actualización parcial (recalcula total) |
| DELETE | `/facturas/{id}` | Borrado lógico (204) |

La API habilita **CORS** (`CORSMiddleware` en `main.py`) para los orígenes de `CORS_ORIGINS` (por defecto el frontend en `:9988`).

## 3. Flujo de Datos y Negocio
`Request → Router (valida con Schema, inyecta Session + usuario X-User) → CRUD (reglas + auditoría) → SQLAlchemy → SQLite → Modelo → ClienteRead → Response`

## 4. Frontend (`frontend/`)
SPA en **React 18 + htm** sin compilación (ES modules desde `esm.sh` vía `importmap`). Ver [ADR-0003](../docs/decissions/ADR-0003-frontend-react-sin-build.md). Servida en **http://127.0.0.1:9988** por `serve.py`; consume la API en `http://<host>:9989/api/v1`.

```
frontend/
├── index.html               # importmap (react, react-dom/client, htm) + carga js/main.js
├── serve.py                 # Servidor estático stdlib, puerto 9988 (FRONTEND_PORT), MIME .js correcto, no-store
├── css/styles.css           # Tema minimalista verde (variables CSS), responsive
└── js/
    ├── config.js            # API_URL (host actual :9989), AUDIT_USER (cabecera X-User)
    ├── api.js               # fetch genérico + clientesApi / facturasApi (list/get/create/update/remove)
    ├── lib.js               # html (htm+React), hooks, formateadores (EUR, fechas)
    ├── main.js / App.js     # Montaje, layout con sidebar, routing por hash (#/clientes, #/facturas)
    ├── components/          # Modal + ConfirmDialog, Toast (contexto), ui (PageHeader, Estado, Field)
    └── pages/
        ├── ClientesPage.js  # Listado + búsqueda local, alta/edición (password opcional al editar), borrado
        └── FacturasPage.js  # Listado + filtro por cliente, totales, alta/edición con cálculo IVA (21/10/4/0 %), borrado
```

Flujo: `Página → api.js (fetch + X-User) → FastAPI /api/v1 → respuesta JSON → estado React`. Los errores de la API (`detail`) se muestran en el formulario o como toast. Importes se envían como string con 2 decimales.
