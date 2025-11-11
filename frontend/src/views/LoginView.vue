<template>
  <div class="min-h-screen flex items-center justify-center px-4">
    <div class="w-full max-w-md">
      <div class="bg-white/90 p-8 rounded-xl shadow-lg backdrop-blur-sm">
        <h2 class="text-3xl font-bold text-center text-indigo-600 mb-6">Login</h2>
        <form @submit.prevent="login" class="space-y-4">
          <input
            v-model="username"
            type="text"
            placeholder="Username"
            required
            class="w-full px-4 py-3 border rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
          />
          <input
            v-model="password"
            type="password"
            placeholder="Password"
            required
            class="w-full px-4 py-3 border rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
          />
          <button
            type="submit"
            class="w-full py-3 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition font-medium"
          >
            Login
          </button>
        </form>
        <p class="mt-4 text-center text-sm text-gray-600">
          Don't have an account?
          <router-link to="/register" class="text-indigo-600 hover:underline">Register</router-link>
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const username = ref('')
const password = ref('')
const router = useRouter()

const login = () => {
  alert(`Logging in: ${username.value}`)
  router.push('/search')
}
</script>

