import pydantic
from typing import Optional
from decimal import Decimal


class Login(pydantic.BaseModel):
    email: str
    password: str


#Productos

class ProductoCreate(pydantic.BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    precio: Decimal
    categoria_id: int

class ProductoModify(pydantic.BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    precio: Optional[Decimal] = None
    categoria_id: Optional[int] = None


#Pedidos

class PedidoCreate(pydantic.BaseModel):
    tipo_pedido: str
    mesa_id: Optional[int] = None
    usuario_id: Optional[int] = None

class PedidoModify(pydantic.BaseModel):
    tipo_pedido: Optional[str] = None
    mesa_id: Optional[int] = None
    usuario_id: Optional[int] = None

#Usuarios

class UsuarioCreate(pydantic.BaseModel):
    email: str
    password: str
    nombre: str
    apellido: str
    rol_id: int

class UsuarioModify(pydantic.BaseModel):
    email: Optional[str] = None
    password: Optional[str] = None
    nombre: Optional[str] = None
    apellido: Optional[str] = None
    rol_id: Optional[int] = None

#Roles

class RolCreate(pydantic.BaseModel):
    nombre: str
    descripcion: Optional[str] = None

class RolModify(pydantic.BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None

#Mesas

class MesaCreate(pydantic.BaseModel):
    nro_id: int
    capacidad: int

class MesaModify(pydantic.BaseModel):
    numero: Optional[int] = None
    capacidad: Optional[int] = None
    estado_id: Optional[int] = None

#Categoria_Productos

class CategoriaProductoCreate(pydantic.BaseModel):
    nombre: str
    descripcion: Optional[str] = None

class CategoriaProductoModify(pydantic.BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None

#Categorias_Gastos

class CategoriaGastoCreate(pydantic.BaseModel):
    nombre: str
    descripcion: Optional[str] = None

class CategoriaGastoModify(pydantic.BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None

#Gastos

class GastoCreate(pydantic.BaseModel):
    nombre: str
    descripcion: str
    monto: Decimal
    categoria_id: int

class GastoModify(pydantic.BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    monto: Optional[Decimal] = None
    categoria_id: Optional[int] = None


#Insumos

class InsumoCreate(pydantic.BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    precio: int

class InsumoModify(pydantic.BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    precio: int




