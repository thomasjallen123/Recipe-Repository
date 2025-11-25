<template>
  <div class="max-w-md mx-auto bg-white p-8 rounded-2xl shadow-xl">
    <h2 class="text-3xl font-bold text-center text-lime-700 mb-6">Register</h2>
    <form @submit.prevent="register" class="space-y-4">
      <input
        v-model="username"
        type="text"
        placeholder="Username"
        class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-lime-500"
        required
      />
      <input
        v-model="email"
        type="email"
        placeholder="Email"
        class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-lime-500"
        required
      />
      <input
        v-model="password"
        type="password"
        placeholder="Password"
        class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-lime-500"
        required
      />
      <button
        type="submit"
        class="w-full bg-lime-600 text-white py-3 rounded-xl font-bold hover:bg-lime-700 transition"
      >
        Create Account
      </button>
    </form>
    <p class="text-center mt-4 text-sm">
      Have an account?
      <router-link to="/login" class="text-lime-600 font-bold">Login</router-link>
    </p>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const username = ref('')
const email = ref('')
const password = ref('')
const router = useRouter()

const register = () => {
  // Mock register – go to login
  router.push('/login')
}
</script>

