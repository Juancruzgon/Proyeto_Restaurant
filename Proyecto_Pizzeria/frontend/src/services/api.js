import axios from 'axios'

const api = axios.create({
  baseURL: 'http://localhost:8000'
})
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

export default api

export const login = async (email, password) => {
  const formData = new FormData()
  formData.append('username', email)
  formData.append('password', password)
  
  const response = await api.post('/login', formData)
  return response.data
}

export const getMesas = async (salonId = null) => {
  const url = salonId ? `/mesas/?salon_id=${salonId}` : '/mesas/'
  const response = await api.get(url)
  return response.data
 
}

api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token')
      window.location.href = '/'
    }
    return Promise.reject(error)
  }
)

export const getPedidosPorMesa = async (mesaId) => {
  const response = await api.get(`/pedidos/?mesa_id=${mesaId}`)
  return response.data
}

export const getDetallePedido = async (pedidoId) => {
  const response = await api.get(`/pedidos/${pedidoId}/detalle`)
  return response.data
}

export const getProductos = async (categoriaId = null) => {
  const url = categoriaId ? `/productos/?categoria_id=${categoriaId}` : '/productos/'
  const response = await api.get(url)
  return response.data
}

export const getProductoPorId = async (productoId) => {
  const response = await api.get(`/productos/${productoId}`)
  return response.data
}

export const modificarProducto = async (productoId, data) => {
  const response = await api.put(`/productos/${productoId}`, data)
  return response.data
  
}

export const crearProducto = async (nombre, precio, descripcion, categoriaId) => {
  const response = await api.post('/productos/', {
    nombre,
    precio: parseFloat(precio),
    descripcion,
    categoria_id: parseInt(categoriaId)
  })
  return response.data
}

export const eliminarProducto = async (productoId) => {
  const response = await api.delete(`/productos/${productoId}`)
  return response.data
}

export const cambiarEstadoPedido = async (pedidoId) => {
  const response = await api.put(`/pedidos/${pedidoId}/estado`)
  return response.data
}

export const eliminarDetalle = async (pedidoId, detalleId) => {
  const response = await api.delete(`/pedidos/${pedidoId}/detalle/${detalleId}`)
  return response.data
}

export const modificarCantidad = async (pedidoId, detalleId, cantidad) => {
  const response = await api.put(`/pedidos/${pedidoId}/detalle/${detalleId}?cantidad=${cantidad}`)
  return response.data
}

export const agregarDetalle = async (pedidoId, productoId, cantidad) => {
  const response = await api.post(`/pedidos/${pedidoId}/detalle`, {
    producto_id: productoId,
    cantidad: cantidad
  })
  return response.data
}

export const crearPedido = async (mesaId, usuarioId, tipoPedido) => {
  const response = await api.post('/pedidos/', {
    mesa_id: parseInt(mesaId),
    usuario_id: parseInt(usuarioId),
    tipo_pedido: tipoPedido
  })
  return response.data

  
}

export const getPedidos = async () => {
  const response = await api.get('/pedidos/')
  return response.data
}

export const getCategorias = async (parentId = null) => {
  const url = parentId ? `/categorias-productos/?parent_id=${parentId}` : '/categorias-productos/'
  const response = await api.get(url)
  return response.data
}

export const crearCategoria = async (nombre, descripcion, parentId) => {
  const response = await api.post('/categorias-productos/', { nombre, descripcion, parent_id: parentId })
  return response.data
}

export const getSalones = async () => {
  const response = await api.get('/salones/')
  return response.data
}
export const eliminarMesa = async (mesaId) => {
  const response = await api.delete(`/mesas/${mesaId}`)
  return response.data
}

export const getMesaPorId = async (mesaId) => {
  const response = await api.get(`/mesas/${mesaId}`)
  return response.data
}

export const modificarMesa = async (mesaId, data) => {
  const response = await api.put(`/mesas/${mesaId}`, data)
  return response.data
}

export const crearMesa = async (data) => {
  const response = await api.post('/mesas/', data)
  return response.data
}