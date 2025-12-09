<!-- src/views/LoginView.vue — REAL LOGIN (no more fake) -->
<template>
  <div class="min-h-screen bg-gradient-to-br from-teal-50 to-lime-50 flex items-center justify-center p-8">
    <div class="max-w-md w-full bg-white p-8 rounded-2xl shadow-2xl">
      <h2 class="text-4xl font-black text-center text-teal-700 mb-8">Login</h2>
      
      <form @submit.prevent="login" class="space-y-6">
        <input
          v-model="username"
          type="text"
          placeholder="Username"
          required
          class="w-full px-4 py-3 border-2 border-teal-200 rounded-xl focus:border-teal-500 focus:outline-none transition"
        />
        <input
          v-model="password"
          type="password"
          placeholder="Password"
          required
          class="w-full px-4 py-3 border-2 border-teal-200 rounded-xl focus:border-teal-500 focus:outline-none transition"
        />

        <button
          type="submit"
          :disabled="loading"
          class="w-full py-4 bg-gradient-to-r from-teal-600 to-lime-600 text-white font-bold rounded-xl hover:shadow-lg transform hover:scale-105 transition disabled:opacity-50"
        >
          {{ loading ? 'Logging in...' : 'Sign In' }}
        </button>
      </form>

      <p class="text-center mt-6 text-gray-600">
        No account? <router-link to="/register" class="text-teal-600 font-bold hover:underline">Register here</router-link>
      </p>

      <p v-if="error" class="text-red-600 text-center mt-4 font-semibold">{{ error }}</p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()
const username = ref('')
const password = ref('')
const loading = ref(false)
const error = ref('')

const login = async () => {
  loading.value = true
  error.value = ''
  try {
    await authStore.login({ username: username.value, password: password.value })
  } catch (err) {
    error.value = err.response?.data?.error || 'Invalid username or password'
  } finally {
    loading.value = false
  }
}
</script>
