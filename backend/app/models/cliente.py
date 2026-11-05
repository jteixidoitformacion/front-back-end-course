from sqlalchemy import Index, Integer, String, text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base
from app.models.audit import AuditMixin


class Cliente(AuditMixin, Base):
    __tablename__ = "clientes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nombre: Mapped[str] = mapped_column(String(150), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    telefono: Mapped[str | None] = mapped_column(String(30), nullable=True)

    # Email único solo entre clientes no borrados (soft delete).
    __table_args__ = (
        Index(
            "uq_clientes_email_activo",
            "email",
            unique=True,
            sqlite_where=text("deleted_at IS NULL"),
        ),
    )
