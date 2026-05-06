import pydantic
from typing import Optional
from decimal import Decimal

class MesaCreate(pydantic.BaseModel):
    nro_id: int
    capacidad: int
    salon_id: Optional[int] = None

class MesaModify(pydantic.BaseModel):
    nro_id: Optional[int] = None
    capacidad: Optional[int] = None
    estado_id: Optional[int] = None
    salon_id: Optional[int] = None