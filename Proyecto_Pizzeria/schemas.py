import pydantic
from typing import Optional
from decimal import Decimal


class PedidoCreate(pydantic.BaseModel):
    tipo_pedido: str
    estado_id: int
    mesa_id: Optional[int] = None
    usuario_id: Optional[int] = None

class ProductoCreate(pydantic.BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    precio: Decimal
    categoria_id: int

class Login(pydantic.BaseModel):
    email: str
    password: str

class UsuarioCreate(pydantic.BaseModel):
    email: str
    password: str
    nombre: str
    apellido: str
    rol_id: int

class RolCreate(pydantic.BaseModel):
    nombre: str
    descripcion: Optional[str] = None