from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field

class FacturaCreate(BaseModel):
    fecha: date
    base: Decimal = Field(ge=0, max_digits=12, decimal_places=2)
    iva: Decimal = Field(ge=0, max_digits=12, decimal_places=2)
    cliente_id: int = Field(gt=0)


class FacturaUpdate(BaseModel):
    fecha: date | None = None
    base: Decimal | None = Field(default=None, ge=0, max_digits=12, decimal_places=2)
    iva: Decimal | None = Field(default=None, ge=0, max_digits=12, decimal_places=2)
    cliente_id: int | None = Field(default=None, gt=0)


class FacturaRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    fecha: date
    base: Decimal
    iva: Decimal
    total: Decimal
    cliente_id: int
    created_at: datetime
    created_by: str
    updated_at: datetime
    updated_by: str
