// src/stores/auth.js
import { defineStore } from 'pinia'
import api from '@/services/api'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,
    token: null
  }),
  actions: {
    async login(credentials) {
      const res = await api.post('/auth/login', credentials)
      this.user = res.data.user
      this.token = res.data.token
      localStorage.setItem('token', this.token)
    },
    async register(data) {
      const res = await api.post('/auth/register', data)
      this.user = res.data.user
    },
    logout() {
      this.user = null
      this.token = null
      localStorage.removeItem('token')
    }
  }
})