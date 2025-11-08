import axios from 'axios'
import { mockRecipes } from './mockData.js'  // ← THIS LINE WAS MISSING

const isMock = import.meta.env.VITE_MOCK_API === 'true'

const api = axios.create({
  baseURL: isMock ? '' : '/api',
  withCredentials: true
})

if (isMock) {
  api.interceptors.response.use(config => {
    return new Promise(resolve => 
      setTimeout(() => resolve({ data: mockHandler(config) }), 600)
    )
  })
}

function mockHandler(config) {
  const { method, url } = config
  let params = {}
  if (config.params) params = config.params
  if (url.includes('?')) {
    new URLSearchParams(url.split('?')[1]).forEach((v, k) => params[k] = v)
  }

  if (url.startsWith('/recipes') && method === 'get') {
    let results = [...mockRecipes]

    if (params.ingredient) {
      results = results.filter(r => 
        r.ingredients.some(i => i.name.toLowerCase().includes(params.ingredient.toLowerCase()))
      )
    }
    if (params.cuisine) results = results.filter(r => r.cuisine === params.cuisine)
    if (params.maxTime) results = results.filter(r => r.cookTime <= parseInt(params.maxTime))

    return { recipes: results, total: results.length }
  }

  if (url.match(/\/recipes\/\d+/) && method === 'get') {
    const id = parseInt(url.split('/').pop())
    return mockRecipes.find(r => r.id === id)
  }

  if (url === '/auth/login' && method === 'post') {
    return { user: { id: 1, username: 'thomas' }, token: 'mock-jwt' }
  }

  if (url === '/collections' && method === 'get') {
    return { recipes: mockRecipes.filter(r => r.isSaved) }
  }

  return { data: {} }
}

export default api