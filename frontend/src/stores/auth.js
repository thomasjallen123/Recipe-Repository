// src/stores/auth.js
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import api from '@/services/api'
import { useRouter } from 'vue-router'

export const useAuthStore = defineStore('auth', () => {
  const user = ref(null)
  const isLoading = ref(true)
  const router = useRouter()

  const isAuthenticated = computed(() => !!user.value)

  const fetchUser = async () => {
    try {
      const res = await api.get('/auth/me')
      user.value = res.data
    } catch (err) {
      user.value = null
    } finally {
      isLoading.value = false
    }
  }

  const login = async (credentials) => {
    try {
      await api.post('/auth/login', credentials)
      await fetchUser()
      router.push('/search')
    } catch (err) {
      throw err
    }
  }

  const register = async (data) => {
    try {
      await api.post('/auth/register', data)
      router.push('/login')
    } catch (err) {
      throw err
    }
  }

  const logout = async () => {
    try {
      await api.post('/auth/logout')
    } catch (err) {
      console.error('Logout failed', err)
    } finally {
      user.value = null
      router.push('/')
    }
  }

  // Auto-check session on app start
  fetchUser()

  return {
    user,
    isAuthenticated,
    isLoading,
    login,
    register,
    logout,
    fetchUser
  }
})