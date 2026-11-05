# ADR-0003: Frontend React sin compilación

- **Estado:** Aceptada
- **Fecha:** 2026-11-05

## Contexto
Se necesita un frontend en `frontend/` con las secciones **Clientes** y **Facturas** (listado + CRUD), construido con React y **sin paso de build** (editar y recargar).

## Decisión
- **React 18 + `htm`** cargados como ES modules desde `esm.sh` mediante un `importmap` en `index.html`. `htm` sustituye a JSX con tagged templates, por lo que no se necesita Babel ni bundler.
- Sin dependencias npm ni `node_modules`. Routing por hash (`#/clientes`, `#/facturas`).
- Servido por un servidor estático propio (`frontend/serve.py`, stdlib de Python) en el **puerto fijo 9988**. Fuerza `text/javascript` para `.js` (en Windows el registro puede devolver `text/plain` y romper los módulos) y `Cache-Control: no-store`.
- La API sigue en el 9989, por lo que se habilita **CORS** en FastAPI (`CORS_ORIGINS`, por defecto `http://127.0.0.1:9988,http://localhost:9988`).
- Diseño minimalista con paleta verde (CSS propio con variables, sin framework CSS).

## Alternativas descartadas
- Vite/CRA: requieren build/dev server de Node.
- React UMD + Babel standalone: transpila en el navegador (lento, desaconsejado).
- Servir el frontend desde FastAPI (`StaticFiles`): se descartó porque se pidió un servidor de frontend en un puerto propio (9988).

## Consecuencias
- Requiere conexión a Internet para cargar React desde la CDN (o vendorizar los módulos en el futuro).
- Cualquier cambio en `frontend/` se ve al recargar el navegador.
