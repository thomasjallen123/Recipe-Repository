<template>
  <div class="min-h-screen flex items-center justify-center px-4 py-12 bg-gradient-to-br from-orange-400/20 via-red-400/20 to-yellow-500/20 animate-pageIn">
    <div class="w-full max-w-md">
      <div class="bg-gradient-to-br from-yellow-50/90 to-orange-50/90 p-10 rounded-3xl shadow-2xl backdrop-blur-md border border-teal-200/50 animate-pulse-slow">
        <h2 class="text-4xl font-black text-center bg-gradient-to-r from-teal-600 to-lime-600 bg-clip-text text-transparent mb-8 leading-tight typewriter">Welcome Back</h2>
        <form @submit.prevent="login" class="space-y-6">
          <div>
            <input
              v-model="username"
              type="text"
              placeholder="Username"
              required
              class="w-full px-5 py-4 border-2 border-teal-200 rounded-2xl focus:ring-4 focus:ring-teal-200/50 focus:border-teal-500 focus:outline-none transition-all text-lg placeholder-orange-400 bg-white/50 animate-slideIn"
            />
          </div>
          <div class="animate-slideIn delay-1">
            <input
              v-model="password"
              type="password"
              placeholder="Password"
              required
              class="w-full px-5 py-4 border-2 border-teal-200 rounded-2xl focus:ring-4 focus:ring-teal-200/50 focus:border-teal-500 focus:outline-none transition-all text-lg placeholder-orange-400 bg-white/50"
            />
          </div>
          <button
            type="submit"
            class="w-full py-4 bg-gradient-to-r from-teal-500 to-lime-500 text-white rounded-2xl hover:from-teal-600 hover:to-lime-600 transition-all font-black text-lg shadow-lg hover:shadow-teal-500/50 transform hover:scale-105 bounce-hover"
          >
            Sign In
          </button>
        </form>
        <p class="mt-6 text-center text-sm text-orange-800 font-semibold animate-slideIn delay-2">
          Don't have an account?
          <router-link to="/register" class="bg-gradient-to-r from-teal-600 to-lime-600 bg-clip-text text-transparent font-bold transition-all hover:from-red-600 hover:to-yellow-600">Create one</router-link>
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

<style scoped>
.animate-pulse-slow {
  animation: pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}
.delay-1 { animation-delay: 0.2s; }
.delay-2 { animation-delay: 0.4s; }
</style>

