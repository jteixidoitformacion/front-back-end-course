# Proyecto

<!-- PROTOCOLO DE GOBERNANZA IA (OBLIGATORIO PARA EL MODELO / AGENTE) -->
## 🤖 Directiva Obligatoria para Asistentes y Agentes de IA
> **ATENCIÓN MODELO / AGENTE DE CÓDIGO:**
> Este repositorio opera bajo un sistema estricto de gobernanza y trazabilidad documental ubicado en la carpeta `.ai/`.
> Antes de implementar código o dar por finalizada cualquier tarea solicitada por el usuario:
> 1. **Lectura obligatoria:** Consulta y aplica rigurosamente las reglas en [.ai/agent.md](.ai/agent.md).
> 2. **Sincronización de Arquitectura:** Registra o actualiza los módulos, dependencias y flujos técnicos en [.ai/context/app_architecture.md](.ai/context/app_architecture.md) y [.ai/context/os_environment.md](.ai/context/os_environment.md).
> 3. **Gestión de Tareas y Roadmap:** Desglosa las fases y marca en tiempo real el progreso (`[x]`) en [.ai/context/roadmap.md](.ai/context/roadmap.md) y [.ai/context/task_board.md](.ai/context/task_board.md).
> 4. **Decisiones de Diseño:** Registra cualquier decisión técnica relevante o patrón arquitectónico en [.ai/docs/decissions/](.ai/docs/decissions/).
>
> ⛔ **REGLA DE ORO:** Nunca entregues código sin haber actualizado previamente el estado y la arquitectura en `.ai/`.
<!-- FIN PROTOCOLO DE GOBERNANZA IA -->

---

## Definición del Proyecto
Quiero generar un proyecto fastapi para gestionar una BD SQLite de momento de clientes (nombre, email, password, telefono, CAMPOS DE AUDIT)

## Puesta en marcha (backend)
```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\python -m pip install -r requirements.txt
.\.venv\Scripts\python -m uvicorn app.main:app --reload --env-file .env   # Swagger: http://127.0.0.1:8000/docs
.\.venv\Scripts\python -m pytest -q                       # tests
```

## Frontend
React 18 sin compilación (ES modules + `htm`) en `frontend/`, con secciones **Clientes** y **Facturas** (listado y CRUD). Se sirve siempre en http://127.0.0.1:9988:
```powershell
backend\.venv\Scripts\python frontend\serve.py
```

Atajo en Windows: `.scripts\start.bat` arranca el frontend en http://127.0.0.1:9988 (ventana aparte) y la API en http://127.0.0.1:9989 (Swagger: `/docs`).

