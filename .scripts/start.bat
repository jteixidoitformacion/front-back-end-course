@echo off
setlocal

set "PORT=9989"
set "FRONTEND_PORT=9988"
set "HOST=127.0.0.1"
set "BACKEND_DIR=%~dp0..\backend"
set "FRONTEND_DIR=%~dp0..\frontend"

cd /d "%BACKEND_DIR%" || (
    echo [ERROR] No se encuentra la carpeta backend: %BACKEND_DIR%
    exit /b 1
)

if not exist ".venv\Scripts\python.exe" (
    echo [INFO] Creando entorno virtual...
    python -m venv .venv || exit /b 1
    ".venv\Scripts\python.exe" -m pip install -r requirements.txt || exit /b 1
)

set "PYTHON=%CD%\.venv\Scripts\python.exe"

if exist "%FRONTEND_DIR%\serve.py" (
    echo [INFO] Iniciando frontend en http://%HOST%:%FRONTEND_PORT%  ^(ventana aparte^)
    start "Frontend :%FRONTEND_PORT%" /D "%FRONTEND_DIR%" cmd /k ""%PYTHON%" serve.py"
) else (
    echo [WARN] No se encuentra %FRONTEND_DIR%\serve.py; no se arranca el frontend.
)

set "ENV_ARG="
if exist ".env" set "ENV_ARG=--env-file .env"

echo [INFO] Iniciando FastAPI en http://%HOST%:%PORT%  (Swagger: http://%HOST%:%PORT%/docs)
"%PYTHON%" -m uvicorn app.main:app --host %HOST% --port %PORT% --reload %ENV_ARG%

endlocal
