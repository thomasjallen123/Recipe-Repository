// src/stores/auth.js
import { defineStore } from 'pinia'
import api from '@/services/api'
import { useRouter } from 'vue-router'

export const useAuthStore = defineStore('auth', () => {
  const user = ref(null)
  const token = ref(null)
  const loading = ref(false)
  const error = ref(null)
  const router = useRouter()

  const isAuthenticated = computed(() => !!token.value)

  const init = () => {
    const saved = localStorage.getItem('authToken')
    if (saved) token.value = saved
  }

  const login = async (credentials) => {
    loading.value = true
    error.value = null
    try {
      const res = await api.post('/auth/login', credentials)
      user.value = res.data.user
      token.value = res.data.token
      localStorage.setItem('authToken', token.value)
      const redirect = router.currentRoute.value.query.redirect || '/search'
      router.push(redirect)
    } catch (err) {
      error.value = err.response?.data?.error || 'Login failed'
    } finally {
      loading.value = false
    }
  }

  const register = async (data) => {
    loading.value = true
    error.value = null
    try {
      await api.post('/auth/register', data)
      router.push('/login')
    } catch (err) {
      error.value = err.response?.data?.error || 'Registration failed'
    } finally {
      loading.value = false
    }
  }

  const logout = () => {
    user.value = null
    token.value = null
    localStorage.removeItem('authToken')
    router.push('/')
  }

  init()

  return { user, token, loading, error, isAuthenticated, login, register, logout }
})