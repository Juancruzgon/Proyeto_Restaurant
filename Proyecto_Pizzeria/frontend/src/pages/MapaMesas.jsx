import { useState, useEffect } from 'react'
import { getMesas } from '../services/api'
import { useNavigate } from 'react-router-dom'
import { useSearchParams } from 'react-router-dom'


function MapaMesas() {
  const [searchParams] = useSearchParams()
  const modoNuevo = searchParams.get('modo') === 'nuevo'
  const [mesas, setMesas] = useState([])
  const navigate = useNavigate()

  useEffect(() => {
    getMesas().then(data => setMesas(data))

    const ws = new WebSocket('ws://localhost:8000/ws')
    ws.onmessage = () => {
      getMesas().then(data => setMesas(data))
    }

    return () => ws.close()
  }, [])

  return (
    <div>
      <h1>Mapa de Mesas</h1>
      <div>
        {mesas.map(mesa => (
          <div
            key={mesa.id}
            onClick={() => {
              if (modoNuevo && mesa.estado_id !== 1) {
                alert('Mesa ocupada - elegí otra mesa')
              } else {
                navigate(`/pedido/${mesa.id}`)
  }
}}
            style={{
              background: mesa.estado_id === 1 ? 'green' : 'red',
              color: 'white',
              padding: '20px',
              margin: '10px',
              display: 'inline-block',
              cursor: 'pointer'
            }}
          >
            Mesa {mesa.id}
          </div>
        ))}
      </div>
    </div>
  )
}

export default MapaMesas