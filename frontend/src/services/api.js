import axios from 'axios'

const isMock = import.meta.env.VITE_MOCK_API === 'true'

const api = axios.create({
  baseURL: isMock ? '' : '/api',
  withCredentials: true
})

if (isMock) {
  api.interceptors.response.use(config => {
    return new Promise(resolve => 
      setTimeout(() => resolve({ data: mockHandler(config) }), 500)
    )
  })
}

function mockHandler(config) {
  const { method, url, data } = config

  // LOGIN
  if (url === '/auth/login' && method === 'post') {
    return { user: { id: 1, username: data.username }, token: 'fake-jwt-123' }
  }

  // REGISTER
  if (url === '/auth/register' && method === 'post') {
    return { user: { id: 1, username: data.username } }
  }

  // RECIPES
  if (url.startsWith('/recipes') && method === 'get') {
    const params = new URLSearchParams(config.url.split('?')[1])
    let results = [...mockRecipes]

    if (params.get('ingredient')) {
      results = results.filter(r => 
        r.ingredients.some(i => i.name.toLowerCase().includes(params.get('ingredient').toLowerCase()))
      )
    }
    if (params.get('cuisine')) {
      results = results.filter(r => r.cuisine === params.get('cuisine'))
    }
    if (params.get('maxTime')) {
      results = results.filter(r => r.cookTime <= parseInt(params.get('maxTime')))
    }

    return { recipes: results.slice(0, 20), total: results.length }
  }

  // RECIPE BY ID
  if (url.match(/\/recipes\/\d+/) && method === 'get') {
    const id = parseInt(url.split('/').pop())
    return mockRecipes.find(r => r.id === id) || { error: 'Not found' }
  }

  // COLLECTIONS
  if (url === '/collections' && method === 'get') {
    return { recipes: mockRecipes.filter(r => r.isSaved) }
  }

  return { data: {} }
}

export default api