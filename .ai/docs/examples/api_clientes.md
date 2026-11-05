# Ejemplos de uso — API Clientes

Base URL: `http://127.0.0.1:8000/api/v1` · Swagger: `http://127.0.0.1:8000/docs`

```powershell
# Crear
curl -X POST http://127.0.0.1:8000/api/v1/clientes -H "Content-Type: application/json" -H "X-User: admin" `
  -d '{"nombre":"Ana","email":"ana@example.com","password":"secreta123","telefono":"+34 600 000 000"}'

# Listar (paginado)
curl "http://127.0.0.1:8000/api/v1/clientes?skip=0&limit=50"

# Obtener
curl http://127.0.0.1:8000/api/v1/clientes/1

# Actualizar parcialmente
curl -X PATCH http://127.0.0.1:8000/api/v1/clientes/1 -H "Content-Type: application/json" -H "X-User: editor" -d '{"telefono":"611111111"}'

# Borrado lógico
curl -X DELETE http://127.0.0.1:8000/api/v1/clientes/1 -H "X-User: admin"
```

Respuesta tipo (`ClienteRead`, nunca incluye la contraseña):
```json
{"id":1,"nombre":"Ana","email":"ana@example.com","telefono":"+34 600 000 000",
 "created_at":"2026-11-05T10:00:00","created_by":"admin","updated_at":"2026-11-05T10:00:00","updated_by":"admin"}
```

Códigos: `201` creado · `204` borrado · `404` no existe · `409` email duplicado · `422` validación.
