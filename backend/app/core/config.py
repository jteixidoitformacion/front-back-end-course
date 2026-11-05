import os

APP_NAME = os.getenv("APP_NAME", "API Gestión de Clientes")
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./clientes.db")
DEFAULT_AUDIT_USER = os.getenv("DEFAULT_AUDIT_USER", "system")
