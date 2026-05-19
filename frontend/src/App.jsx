import { useState } from 'react'
import { CardSearch } from './components/CardSearch'
import { PriceChart } from './components/PriceChart'
import { StockAlerts } from './components/StockAlerts'

export default function App() {
  const [selectedCard, setSelectedCard] = useState(null)

  return (
    <div className="app">
      <header className="app-header">
        <h1>TCG Platform</h1>
      </header>
      <div className="app-body">
        <aside className="sidebar">
          <CardSearch onSelect={setSelectedCard} selectedCard={selectedCard} />
        </aside>
        <main className="main-content">
          <PriceChart card={selectedCard} />
          <StockAlerts />
        </main>
      </div>
    </div>
  )
}
