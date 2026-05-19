import { useEffect, useState } from 'react'
import { fetchAlerts } from '../api'

export function StockAlerts() {
  const [alerts, setAlerts] = useState([])
  const [error, setError] = useState(null)

  useEffect(() => {
    fetchAlerts()
      .then(setAlerts)
      .catch((err) => setError(err.message))
  }, [])

  return (
    <div className="stock-alerts">
      <h2>Stock Alerts</h2>
      {error && <p className="error">{error}</p>}
      {alerts.length === 0 && !error && (
        <p className="empty-msg">No alerts yet</p>
      )}
      <ul className="alert-list">
        {alerts.map((alert) => (
          <li
            key={alert.id}
            className={`alert-item ${alert.in_stock ? 'in-stock' : 'out-of-stock'}`}
          >
            <span className="alert-status">
              {alert.in_stock ? '● In Stock' : '○ Out of Stock'}
            </span>
            <span className="alert-retailer">{alert.retailer}</span>
            <span className="alert-time">
              {new Date(alert.detected_at).toLocaleString()}
            </span>
            {alert.url && (
              <a href={alert.url} target="_blank" rel="noreferrer" className="alert-link">
                View →
              </a>
            )}
          </li>
        ))}
      </ul>
    </div>
  )
}
