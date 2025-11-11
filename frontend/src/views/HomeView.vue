<template>
  <div class="min-h-screen flex flex-col items-center justify-center px-4 sm:px-6 lg:px-8">
    <div class="w-full max-w-5xl mx-auto text-center z-10">
      <h1 class="block w-full text-7xl md:text-9xl font-black tracking-tight bg-gradient-to-r from-indigo-600 via-purple-600 to-pink-600 bg-clip-text text-transparent drop-shadow-2xl">
        Recipe Repository
      </h1>

      <p class="mt-12 text-xl md:text-2xl font-medium text-gray-700 leading-relaxed max-w-4xl mx-auto">
        Welcome, everyone!<br><br>
        Our platform empowers users to seamlessly explore a wide variety of recipes sourced directly from trusted sites like AllRecipes and Food Network. 
        Whether you’re searching for everyday meals or trying something completely new, you can easily save your favorite dishes, organize them for later, and personalize serving sizes using our built-in recipe scaling tools.
      </p>

      <div class="mt-20 flex flex-col sm:flex-row gap-12 justify-center items-center">
        <router-link
          to="/search"
          class="group relative px-12 py-6 bg-white/10 backdrop-blur-xl border-2 border-white/30 rounded-3xl shadow-2xl hover:shadow-indigo-500/50 transition-all duration-500 hover:scale-105"
        >
          <span class="text-2xl font-bold bg-gradient-to-r from-indigo-600 to-purple-600 bg-clip-text text-transparent group-hover:from-pink-600 group-hover:to-purple-600">
            Explore Recipes
          </span>
          <div class="absolute inset-0 rounded-3xl bg-gradient-to-r from-indigo-600/20 to-purple-600/20 blur-xl group-hover:blur-2xl transition"></div>
        </router-link>

        <router-link
          to="/collection"
          class="group relative px-12 py-6 bg-white/10 backdrop-blur-xl border-2 border-white/30 rounded-3xl shadow-2xl hover:shadow-red-500/50 transition-all duration-500 hover:scale-105"
        >
          <span class="text-2xl font-bold bg-gradient-to-r from-red-600 to-pink-600 bg-clip-text text-transparent group-hover:from-pink-600 group-hover:to-red-600">
            My Favorites
          </span>
          <div class="absolute inset-0 rounded-3xl bg-gradient-to-r from-red-600/20 to-pink-600/20 blur-xl group-hover:blur-2xl transition"></div>
        </router-link>

        <router-link
          to="/login"
          class="text-2xl font-bold text-gray-800 relative after:absolute after:bottom-0 after:left-0 after:w-0 after:h-1 after:bg-gradient-to-r after:from-indigo-600 after:to-purple-600 after:transition-all after:duration-500 hover:after:w-full"
        >
          Login
        </router-link>
      </div>
    </div>
  </div>
</template>
<script setup></script>

