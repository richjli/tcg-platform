async function request(url, options) {
  const res = await fetch(url, options)
  if (!res.ok) throw new Error(`Request failed: ${res.status}`)
  return res.json()
}

export const fetchCards = () => request('/cards/')

export const createCard = (data) =>
  request('/cards/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  })

export const fetchPrices = (cardId, limit = 100) =>
  request(`/prices/?card_id=${cardId}&limit=${limit}`)

export const fetchAlerts = () => request('/alerts/')
