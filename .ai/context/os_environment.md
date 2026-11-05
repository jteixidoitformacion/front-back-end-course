# Entorno de Ejecución y Sistema Operativo (OS & Environment)

## 1. Requisitos de Plataforma
- **Sistemas Operativos compatibles:** Windows / Linux / macOS (desarrollo actual en Windows + PowerShell).
- **Python:** 3.10+ (probado con 3.14.2).
- **Dependencias** (`backend/requirements.txt`): fastapi, uvicorn[standard], sqlalchemy 2.0.x (<2.1), pydantic[email] 2.12.5, pytest, httpx.
- **Base de datos:** SQLite (fichero `backend/clientes.db`, ignorado en git).
- ⚠️ **Windows Smart App Control (modo enforce)** bloquea DLLs de wheels publicadas muy recientemente (`ImportError: DLL load failed ... Una directiva de Control de aplicaciones bloqueó este archivo`). Detectado con `pydantic-core 2.50.x` y `sqlalchemy 2.1.x`; por eso se acotan versiones. Si vuelve a ocurrir tras actualizar, bajar a la versión estable anterior.

## 2. Variables de Entorno y Configuración
| Variable | Por defecto | Descripción |
|---|---|---|
| `APP_NAME` | `API Gestión de Clientes` | Título de la API |
| `DATABASE_URL` | `sqlite:///./clientes.db` | Cadena de conexión SQLAlchemy |
| `DEFAULT_AUDIT_USER` | `system` | Usuario de auditoría si no llega cabecera `X-User` |
| `CORS_ORIGINS` | `http://127.0.0.1:9988,http://localhost:9988` | Orígenes permitidos (separados por comas) |
| `FRONTEND_PORT` | `9988` | Puerto de `frontend/serve.py` (lo fija `start.bat`) |

## Frontend
- Sin Node ni build: React 18 + htm se cargan desde `https://esm.sh` (requiere Internet y navegador moderno con soporte de `importmap`).
- Se sirve con el Python del venv del backend: `backend\.venv\Scripts\python frontend\serve.py` → http://127.0.0.1:9988.

## 3. Comandos (PowerShell, desde `backend/`)
```powershell
python -m venv .venv
.\.venv\Scripts\python -m pip install -r requirements.txt
.\.venv\Scripts\python -m uvicorn app.main:app --reload --env-file .env   # http://127.0.0.1:8000/docs
.\.venv\Scripts\python -m pytest -q
```

## 4. Scripts de arranque (`.scripts/`)
- `.scripts\start.bat`: arranca el **frontend** en **http://127.0.0.1:9988** (ventana aparte, `frontend\serve.py`) y FastAPI (uvicorn `--reload`) siempre en **http://127.0.0.1:9989** (`/docs` para Swagger). Crea `.venv` e instala dependencias si no existe y carga `backend\.env` si está presente. Se puede lanzar desde cualquier directorio.
