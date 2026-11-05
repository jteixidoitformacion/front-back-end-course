from datetime import date
from decimal import Decimal

from sqlalchemy import CheckConstraint, Date, ForeignKey, Integer, Numeric
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base
from app.models.audit import AuditMixin


class Factura(AuditMixin, Base):
    __tablename__ = "facturas"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    fecha: Mapped[date] = mapped_column(Date, nullable=False)
    base: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    iva: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    total: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    cliente_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("clientes.id", ondelete="RESTRICT"), nullable=False, index=True
    )

    __table_args__ = (
        CheckConstraint("base >= 0", name="ck_facturas_base_no_negativa"),
        CheckConstraint("iva >= 0", name="ck_facturas_iva_no_negativo"),
        # SQLite guarda NUMERIC como REAL: se compara con tolerancia de medio céntimo.
        CheckConstraint("abs(total - (base + iva)) < 0.005", name="ck_facturas_total"),
    )
