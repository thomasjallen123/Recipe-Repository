<!-- src/views/RegisterView.vue -->
<script setup>
import { ref } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'

const authStore = useAuthStore()
const router = useRouter()

const username = ref('')
const email = ref('')
const password = ref('')
const loading = ref(false)
const error = ref('')

const register = async () => {
  loading.value = true
  error.value = ''
  try {
    await authStore.register({
      username: username.value,
      email: email.value,
      password: password.value
    })
    // Success → redirected to /login by store
  } catch (err) {
    error.value = err.response?.data?.error || 'Registration failed'
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="min-h-screen bg-gradient-to-br from-teal-50 to-lime-50 flex items-center justify-center p-8">
    <div class="max-w-md w-full bg-white p-10 rounded-3xl shadow-2xl">
      <h2 class="text-5xl font-black text-center text-teal-700 mb-10">Create Account</h2>

      <form @submit.prevent="register" class="space-y-6">
        <input v-model="username" type="text" placeholder="Username" required
          class="w-full px-6 py-4 text-lg border-2 border-teal-200 rounded-2xl focus:border-lime-500 focus:outline-none transition" />
        <input v-model="email" type="email" placeholder="Email" required
          class="w-full px-6 py-4 text-lg border-2 border-teal-200 rounded-2xl focus:border-lime-500 focus:outline-none transition" />
        <input v-model="password" type="password" placeholder="Password" required
          class="w-full px-6 py-4 text-lg border-2 border-teal-200 rounded-2xl focus:border-lime-500 focus:outline-none transition" />

        <button type="submit" :disabled="loading"
          class="w-full py-5 bg-gradient-to-r from-teal-600 to-lime-600 text-white text-xl font-bold rounded-2xl shadow-xl hover:shadow-2xl transform hover:scale-105 transition disabled:opacity-60">
          {{ loading ? 'Creating Account...' : 'Sign Up' }}
        </button>
      </form>

      <p v-if="error" class="text-red-600 text-center mt-6 font-semibold text-lg">{{ error }}</p>

      <p class="text-center mt-8 text-gray-600 text-lg">
        Already have an account?
        <router-link to="/login" class="text-teal-600 font-bold hover:underline">Log in here</router-link>
      </p>
    </div>
  </div>
</template>

