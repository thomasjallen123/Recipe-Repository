<template>
  <div class="max-w-md mx-auto bg-white p-8 rounded-2xl shadow-xl">
    <h2 class="text-3xl font-bold text-center text-teal-700 mb-6">Login</h2>
    <form @submit.prevent="login" class="space-y-4">
      <input
        v-model="username"
        type="text"
        placeholder="Username"
        class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-teal-500"
        required
      />
      <input
        v-model="password"
        type="password"
        placeholder="Password"
        class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-teal-500"
        required
      />
      <button
        type="submit"
        class="w-full bg-teal-600 text-white py-3 rounded-xl font-bold hover:bg-teal-700 transition"
      >
        Sign In
      </button>
    </form>
    <p class="text-center mt-4 text-sm">
      No account?
      <router-link to="/register" class="text-teal-600 font-bold">Register</router-link>
    </p>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const username = ref('')
const password = ref('')
const router = useRouter()

const login = () => {
  // Mock login success
  router.push('/search')
}
</script>

