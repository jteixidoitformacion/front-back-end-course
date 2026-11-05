from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field

TELEFONO_PATTERN = r"^\+?[0-9 ()-]{6,30}$"


class ClienteBase(BaseModel):
    nombre: str = Field(min_length=1, max_length=150)
    email: EmailStr
    telefono: str | None = Field(default=None, pattern=TELEFONO_PATTERN)


class ClienteCreate(ClienteBase):
    password: str = Field(min_length=8, max_length=128)


class ClienteUpdate(BaseModel):
    nombre: str | None = Field(default=None, min_length=1, max_length=150)
    email: EmailStr | None = None
    telefono: str | None = Field(default=None, pattern=TELEFONO_PATTERN)
    password: str | None = Field(default=None, min_length=8, max_length=128)


class ClienteRead(ClienteBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    created_by: str
    updated_at: datetime
    updated_by: str
