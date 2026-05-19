import { useEffect, useState } from 'react'
import { createCard, fetchCards } from '../api'

const EMPTY_FORM = { name: '', set_name: '', game: 'pokemon', card_number: '' }

export function CardSearch({ onSelect, selectedCard }) {
  const [cards, setCards] = useState([])
  const [query, setQuery] = useState('')
  const [adding, setAdding] = useState(false)
  const [form, setForm] = useState(EMPTY_FORM)
  const [error, setError] = useState(null)

  useEffect(() => {
    fetchCards()
      .then(setCards)
      .catch((err) => setError(err.message))
  }, [])

  const filtered = cards.filter((c) =>
    c.name.toLowerCase().includes(query.toLowerCase())
  )

  function handleField(field) {
    return (e) => setForm((f) => ({ ...f, [field]: e.target.value }))
  }

  async function handleAdd(e) {
    e.preventDefault()
    setError(null)
    try {
      const payload = { ...form }
      if (!payload.card_number) delete payload.card_number
      const card = await createCard(payload)
      setCards((prev) => [...prev, card])
      setAdding(false)
      setForm(EMPTY_FORM)
    } catch (err) {
      setError(err.message)
    }
  }

  return (
    <div className="card-search">
      <div className="card-search-header">
        <h2>Cards</h2>
        <button className="btn-ghost" onClick={() => setAdding((v) => !v)}>
          {adding ? 'Cancel' : '+ Add'}
        </button>
      </div>

      {adding && (
        <form className="add-card-form" onSubmit={handleAdd}>
          <input
            placeholder="Name"
            value={form.name}
            onChange={handleField('name')}
            required
          />
          <input
            placeholder="Set name"
            value={form.set_name}
            onChange={handleField('set_name')}
            required
          />
          <select value={form.game} onChange={handleField('game')}>
            <option value="pokemon">Pokémon</option>
            <option value="riftbound">Riftbound</option>
          </select>
          <input
            placeholder="Card number (optional)"
            value={form.card_number}
            onChange={handleField('card_number')}
          />
          <button type="submit" className="btn-primary">Add Card</button>
        </form>
      )}

      <input
        className="search-input"
        placeholder="Search cards…"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
      />

      {error && <p className="error">{error}</p>}

      <ul className="card-list">
        {filtered.map((card) => (
          <li
            key={card.id}
            className={`card-item ${selectedCard?.id === card.id ? 'selected' : ''}`}
            onClick={() => onSelect(card)}
          >
            <span className="card-name">{card.name}</span>
            <span className="card-meta">{card.set_name} · {card.game}</span>
          </li>
        ))}
        {filtered.length === 0 && (
          <li className="card-item empty">No cards found</li>
        )}
      </ul>
    </div>
  )
}
