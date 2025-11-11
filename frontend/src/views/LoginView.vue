<template>
  <div class="min-h-screen flex items-center justify-center px-4 py-12 bg-gradient-to-br from-amber-50/50 to-yellow-50/50">
    <div class="w-full max-w-md">
      <div class="bg-white/95 p-10 rounded-3xl shadow-2xl backdrop-blur-md border border-gray-100/50">
        <h2 class="text-4xl font-black text-center text-indigo-600 mb-8 leading-tight">Welcome Back</h2>
        <form @submit.prevent="login" class="space-y-6">
          <div>
            <input
              v-model="username"
              type="text"
              placeholder="Username"
              required
              class="w-full px-5 py-4 border-2 border-gray-200 rounded-2xl focus:ring-4 focus:ring-indigo-200/50 focus:border-indigo-500 focus:outline-none transition-all text-lg placeholder-gray-400"
            />
          </div>
          <div>
            <input
              v-model="password"
              type="password"
              placeholder="Password"
              required
              class="w-full px-5 py-4 border-2 border-gray-200 rounded-2xl focus:ring-4 focus:ring-indigo-200/50 focus:border-indigo-500 focus:outline-none transition-all text-lg placeholder-gray-400"
            />
          </div>
          <button
            type="submit"
            class="w-full py-4 bg-gradient-to-r from-indigo-600 to-purple-600 text-white rounded-2xl hover:from-indigo-700 hover:to-purple-700 transition-all font-black text-lg shadow-lg hover:shadow-indigo-500/50 transform hover:scale-105"
          >
            Sign In
          </button>
        </form>
        <p class="mt-6 text-center text-sm text-gray-600 font-medium">
          Don't have an account?
          <router-link to="/register" class="text-indigo-600 hover:text-purple-600 font-bold transition-colors">Create one</router-link>
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

