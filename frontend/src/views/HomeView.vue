<template>
  <div class="min-h-screen flex items-center justify-center bg-gradient-to-br from-indigo-50 via-white to-pink-50 px-4">
    <div class="text-center max-w-2xl">
      <h1 class="text-5xl md:text-6xl font-bold text-indigo-600 mb-4">
        Recipe Repository
      </h1>
      <p class="text-xl text-gray-700 mb-2">Welcome, Thomas!</p>
      <p class="text-lg text-gray-600 mb-10">
        Discover, save, and scale recipes from AllRecipes & Food Network
      </p>

      <div class="flex flex-col sm:flex-row gap-4 justify-center">
        <router-link
          to="/search"
          class="px-8 py-3 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition text-lg font-medium"
        >
          Explore Recipes
        </router-link>
        <router-link
          to="/login"
          class="px-8 py-3 border-2 border-indigo-600 text-indigo-600 rounded-lg hover:bg-indigo-50 transition text-lg font-medium"
        >
          Login
        </router-link>
      </div>
    </div>
  </div>
</template>