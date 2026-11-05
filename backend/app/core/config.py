import os

APP_NAME = os.getenv("APP_NAME", "API Gestión de Clientes")
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./clientes.db")
DEFAULT_AUDIT_USER = os.getenv("DEFAULT_AUDIT_USER", "system")
CORS_ORIGINS = [
    o.strip()
    for o in os.getenv("CORS_ORIGINS", "http://127.0.0.1:9988,http://localhost:9988").split(",")
    if o.strip()
]
