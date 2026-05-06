import pydantic
from typing import Optional
from decimal import Decimal

class InsumoCreate(pydantic.BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    precio: int
    stock: int
    
class InsumoModify(pydantic.BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    precio: int
    stock: int
