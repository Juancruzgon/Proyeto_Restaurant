import { Routes, Route } from 'react-router-dom'
import Login from './pages/Login'
import MapaMesas from './pages/MapaMesas'
import Pedido from './pages/Pedido'
import Dashboard from './pages/Dashboard'
import Pedidos from './pages/Pedidos'
import NuevoPedido from './pages/NuevoPedido'
import Productos from './pages/Productos'
import CategoriaProductos from './pages/CategoriaProductos'
import ModificarProducto from './pages/ModificarProducto'
import EditarMesa from './pages/EditarMesa'
import CrearMesa from './pages/CrearMesa'



function App() {
  return (
    <Routes>
      <Route path="/" element={<Login />} />
      <Route path="/mesas" element={<MapaMesas />} />
      <Route path="/pedido/:mesaId" element={<Pedido />} />
      <Route path="/dashboard" element={<Dashboard />} />
      <Route path="/pedidos" element={<Pedidos />} />
      <Route path="/nuevo-pedido" element={<NuevoPedido />} />
      <Route path="/productos" element={<Productos />} />
      <Route path="/productos/:categoriaId" element={<CategoriaProductos />} />
      <Route path="/productos/:categoriaId/:productoId" element={<ModificarProducto />} />
      <Route path="/mesas/:mesaId/editar" element={<EditarMesa />} />
      <Route path="/mesas/nueva" element={<CrearMesa />} />
    </Routes>
  )
}

export default App