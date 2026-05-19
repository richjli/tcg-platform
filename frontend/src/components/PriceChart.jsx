import { useEffect, useState } from 'react'
import {
  CartesianGrid,
  Line,
  LineChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from 'recharts'
import { fetchPrices } from '../api'

function formatPrice(value) {
  return `$${value.toFixed(2)}`
}

export function PriceChart({ card }) {
  const [prices, setPrices] = useState([])
  const [error, setError] = useState(null)

  useEffect(() => {
    if (!card) {
      setPrices([])
      return
    }
    setError(null)
    fetchPrices(card.id)
      .then((data) =>
        setPrices(
          data.map((p) => ({
            time: new Date(p.recorded_at).toLocaleDateString(),
            price: p.price,
          }))
        )
      )
      .catch((err) => setError(err.message))
  }, [card])

  if (!card) {
    return (
      <div className="price-chart empty">
        <p>Select a card to view price history</p>
      </div>
    )
  }

  return (
    <div className="price-chart">
      <h2>
        {card.name} <span className="card-meta">— Price History</span>
      </h2>
      {error && <p className="error">{error}</p>}
      {prices.length === 0 && !error && (
        <p className="empty-msg">No price data yet</p>
      )}
      {prices.length > 0 && (
        <ResponsiveContainer width="100%" height={300}>
          <LineChart data={prices} margin={{ top: 8, right: 24, bottom: 8, left: 8 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="#2a2a3a" />
            <XAxis dataKey="time" tick={{ fontSize: 11, fill: '#888' }} />
            <YAxis tickFormatter={formatPrice} tick={{ fontSize: 11, fill: '#888' }} />
            <Tooltip formatter={(v) => [formatPrice(v), 'Price']} />
            <Line
              type="monotone"
              dataKey="price"
              stroke="#6366f1"
              strokeWidth={2}
              dot={false}
              activeDot={{ r: 4 }}
            />
          </LineChart>
        </ResponsiveContainer>
      )}
    </div>
  )
}
