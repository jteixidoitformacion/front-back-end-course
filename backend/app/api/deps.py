from typing import Annotated

from fastapi import Depends, Header
from sqlalchemy.orm import Session

from app.core.config import DEFAULT_AUDIT_USER
from app.db.database import get_db

DbSession = Annotated[Session, Depends(get_db)]


def get_usuario_auditoria(
    x_user: Annotated[str | None, Header(max_length=100)] = None,
) -> str:
    """Usuario que realiza la operación (cabecera X-User). Provisional hasta tener autenticación."""
    return x_user or DEFAULT_AUDIT_USER


UsuarioAuditoria = Annotated[str, Depends(get_usuario_auditoria)]
