// src/services/api.js
import axios from 'axios'
import { mockRecipes } from '@/services/mockData.js'

const isMock = import.meta.env.VITE_MOCK_API === 'true'

const api = axios.create({
  baseURL: isMock ? '' : '/api',
  timeout: 10000,
  withCredentials: true
})

api.interceptors.request.use(config => {
  const token = localStorage.getItem('authToken')
  if (token) config.headers.Authorization = `Bearer ${token}`
  return config
})

api.interceptors.response.use(
  res => res,
  async err => {
    if (isMock) {
      await new Promise(r => setTimeout(r, 300 + Math.random() * 700))
      if (Math.random() < 0.05) return Promise.reject({ response: { status: 500 } })
      const data = mockHandler(err.config)
      return data.error ? Promise.reject({ response: { status: 404, data } }) : Promise.resolve({ data })
    }
    return Promise.reject(err)
  }
)

function mockHandler(config) {
  const { method, url, data } = config
  const params = new URLSearchParams(url.split('?')[1] || '')

  if (url === '/auth/login' && method === 'post') return { user: { id: 1, username: data.username }, token: 'fake-jwt' }
  if (url === '/auth/register' && method === 'post') return { user: { id: 1, username: data.username } }

  if (url.startsWith('/recipes') && method === 'get') {
    let results = [...mockRecipes]
    if (params.get('ingredient')) {
      const term = params.get('ingredient').toLowerCase()
      results = results.filter(r => r.title.toLowerCase().includes(term) || r.ingredients.some(i => i.name.toLowerCase().includes(term)))
    }
    if (params.get('cuisine')) results = results.filter(r => r.cuisine === params.get('cuisine'))
    if (params.get('maxTime')) results = results.filter(r => r.cookTime <= parseInt(params.get('maxTime')))
    const page = parseInt(params.get('page') || 1), limit = parseInt(params.get('limit') || 20)
    const start = (page - 1) * limit
    return { recipes: results.slice(start, start + limit), total: results.length }
  }

  if (url.match(/\/recipes\/\d+/) && method === 'get') {
    const id = parseInt(url.split('/').pop())
    return mockRecipes.find(r => r.id === id) || { error: 'Not found' }
  }

  return { data: {} }
}

export default api