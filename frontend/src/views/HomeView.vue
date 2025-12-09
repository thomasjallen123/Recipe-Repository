<!-- src/views/HomeView.vue -->
<template>
  <div class="min-h-screen bg-gradient-to-br from-teal-50 to-lime-50 flex items-center justify-center p-8">
    <div class="text-center max-w-2xl">
      <h1 class="text-6xl font-black text-teal-700 mb-6">Recipe Repository</h1>
      <p class="text-xl text-gray-700 mb-12">Search, save, and scale your favorite recipes.</p>

      <!-- Login & Register -->
      <div class="flex justify-center gap-6 mb-8">
        <router-link 
          to="/login" 
          class="px-8 py-4 bg-teal-600 text-white rounded-xl font-bold hover:bg-teal-700 transition text-lg"
        >
          Login
        </router-link>
        <router-link 
          to="/register" 
          class="px-8 py-4 bg-teal-600 text-white rounded-xl font-bold hover:bg-teal-700 transition text-lg"
        >
          Register
        </router-link>
      </div>

      <!-- NEW: Explore Recipes Button -->
      <router-link 
        to="/search" 
        class="inline-block px-12 py-5 bg-gradient-to-r from-indigo-600 to-purple-600 text-white text-xl font-black rounded-3xl shadow-2xl hover:shadow-indigo-500/50 transform hover:scale-105 transition-all duration-300"
      >
        Explore Recipes
      </router-link>
    </div>
  </div>
</template>
