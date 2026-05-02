import pydantic
from typing import Optional
from decimal import Decimal

class MesaCreate(pydantic.BaseModel):
    nro_id: int
    capacidad: int

class MesaModify(pydantic.BaseModel):
    numero: Optional[int] = None
    capacidad: Optional[int] = None
    estado_id: Optional[int] = None