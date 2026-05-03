import { Routes, Route } from 'react-router-dom'
import Login from './pages/Login'
import MapaMesas from './pages/MapaMesas'
import Pedido from './pages/Pedido'
import Dashboard from './pages/Dashboard'
import Pedidos from './pages/Pedidos'
import NuevoPedido from './pages/NuevoPedido'

function App() {
  return (
    <Routes>
      <Route path="/" element={<Login />} />
      <Route path="/mesas" element={<MapaMesas />} />
      <Route path="/pedido/:mesaId" element={<Pedido />} />
      <Route path="/dashboard" element={<Dashboard />} />
      <Route path="/pedidos" element={<Pedidos />} />
      <Route path="/nuevo-pedido" element={<NuevoPedido />} />
    </Routes>
  )
}

export default App