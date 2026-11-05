# Directivas del Agente (Agent Instructions)

Este archivo define las instrucciones maestras de gobernanza para cualquier agente o modelo de lenguaje que intervenga en este repositorio.

## 1. Alimentación de Contexto Obligatoria
Antes de iniciar cualquier tarea, planificación o modificación en el código:
- Consultar README.md para comprender la definición funcional del proyecto y sus requisitos.
- Leer .ai/context/app_architecture.md para conocer la arquitectura de la aplicación, módulos y flujos técnicos.
- Leer .ai/context/os_environment.md para conocer requisitos del sistema operativo, compatibilidad y entorno de ejecución.
- Revisar .ai/context/roadmap.md y .ai/context/task_board.md para identificar tareas pendientes, estado de ejecución y dependencias.
- Consultar los flujos de trabajo de IA en .ai/workflows/.
- Consultar la documentación histórica en el directorio de documentación:
  - Decisiones de arquitectura y técnicas en .ai/docs/decissions/.
  - Resumen o bitácora de sesiones pasadas en .ai/docs/sessions/.
  - Casos de uso o implementaciones de referencia en .ai/docs/examples/.

## 2. Documentación y Sincronización Obligatoria en .ai/
El agente **NO debe considerar finalizada ninguna solicitud** sin haber actualizado la documentación correspondiente en cada paso:
- **Arquitectura y diseño:** En cuanto definas o modifiques componentes, archivos, dependencias o flujos, regístralos inmediatamente en .ai/context/app_architecture.md y .ai/context/os_environment.md.
- **Gestión de tareas y avance:** Adapta las fases a la petición actual y marca en tiempo real las tareas completadas ([x]) en .ai/context/roadmap.md y .ai/context/task_board.md.
- **Registro de decisiones (ADR):** Si eliges una librería, estructura o patrón de diseño, documenta el motivo en .ai/docs/decissions/.
- **Bitácora y ejemplos:** Documenta resúmenes de sesión en .ai/docs/sessions/ y ejemplos de uso en .ai/docs/examples/ cuando aplique.

## 3. Principios de Operación
- Trabajar de forma iterativa y verificar cambios tras cada modificación.
- Proponer un mensaje de commit en español siguiendo el formato Conventional Commits al finalizar.

## 4. Comunicación con el Usuario
- El usuario se llama **Jordi**; dirígete a él por su nombre.
- Responde **siempre en castellano**, incluidos los mensajes de progreso y los resúmenes.
