from datetime import date, time, datetime
from sqlmodel import SQLModel, Field
from typing import Optional
from decimal import Decimal

class EstadoPedido(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str = Field(unique=True) # "Abierto", "Cerrado", "Cancelado"
    descripcion: Optional[str] = None

class EstadoMesa(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str = Field(unique=True) # "Libre", "Ocupada", etc.
    descripcion: Optional[str] = None

class Mesa(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nro_id: int = Field(unique=True, index=True)
    estado_id: int = Field(foreign_key="estadomesa.id")
    capacidad: int

class Pedido(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nro_pedido: int = Field(index=True)
    tipo_pedido: str # Ejemplo: "Salón", "Mostrador", "Delivery"
    estado_id: int = Field(foreign_key="estadopedido.id")
    mesa_id: Optional[int] = Field(default=None, foreign_key="mesa.id")
    usuario_id: Optional[int] = Field(default=None, foreign_key="usuario.id")
    total: Decimal = Field(default=0, max_digits=10, decimal_places=2)
    fecha: date = Field(default_factory=date.today)
    hora: time = Field(default_factory=lambda: datetime.now().time())
    activo: bool = Field(default=True)

class DetallePedido(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    pedido_id: int = Field(foreign_key="pedido.id")
    producto_id: int = Field(foreign_key="producto.id")
    cantidad: int
    precio_unitario: Decimal = Field(max_digits=10, decimal_places=2)
    subtotal: Decimal = Field(max_digits=10, decimal_places=2)

class Insumo(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nro_insumo :int = Field(index=True)
    nombre: str = Field(unique=True, index=True)
    descripcion: Optional[str] = None
    precio: Decimal = Field(max_digits=10, decimal_places=2)


class MovimientoStock(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nro_id: int = Field(index=True)
    id_insumo:int = Field(foreign_key="insumo.id")
    cantidad: int
    fecha: date = Field(default_factory=date.today)
    tipo: str  # "entrada" | "salida"

class CategoriaProducto(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str = Field(unique=True)
    descripcion: Optional[str] = None


class Producto(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str = Field(unique=True, index=True)
    descripcion : Optional[str] = None
    precio: Decimal = Field(max_digits=10, decimal_places=2)
    categoria_id: int = Field(foreign_key="categoriaproducto.id")
    activo: bool = Field(default=True)


class Rol(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str = Field(unique=True)
    descripcion: Optional[str] = None

class Usuario(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    apellido: str
    email: str = Field(unique=True)
    password: str
    rol_id: int = Field(foreign_key="rol.id")
    activo: bool = Field(default=True)

class CategoriaGasto(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str = Field(unique=True)
    descripcion: Optional[str] = None


class Gasto(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    descripcion: str
    categoria_id: int = Field(foreign_key="categoriagasto.id")
    monto: Decimal = Field(max_digits=10, decimal_places=2)
    fecha: date = Field(default_factory=date.today)

class GestorNegocio(SQLModel, table=True):
    id: int = Field(default=1, primary_key=True)
    nombre: str
    direccion: str
    telefono: str

class GestorImpresora(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    puerto: int
    ip: str
    tipo: str

#class Proveedor(SQLModel, table=true):

#class Comanda(SQLModel, table=true):

#class GestorImpresion(SQLModel, table=true):

#class ReporteDiario(SQLModel, table=true):
