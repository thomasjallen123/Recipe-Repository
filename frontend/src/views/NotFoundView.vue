<!-- src/views/NotFoundView.vue -->
<template>
  <main class="min-h-screen flex flex-col items-center justify-center text-center px-6 py-12 bg-gradient-to-br from-amber-50/50 to-yellow-50/50 animate-pageIn" role="alert" aria-labelledby="not-found-title">
    <h1 id="not-found-title" class="text-8xl sm:text-9xl font-black text-orange-600 drop-shadow-lg" data-testid="404-title">
      404
    </h1>
    <p class="text-2xl sm:text-3xl font-semibold text-orange-800 mt-4" data-testid="404-message">
      Page not found
    </p>
    <p class="text-lg text-gray-600 mt-2 max-w-md">
      The page you're looking for doesn't exist or has been moved.
    </p>
    <router-link :to="{ name: 'Home' }" class="mt-10 inline-block px-8 py-4 bg-gradient-to-r from-teal-500 to-lime-500 text-white text-lg font-bold rounded-2xl shadow-lg hover:shadow-teal-500/50 transform hover:scale-105 transition-all duration-300 focus:outline-none focus:ring-4 focus:ring-teal-300" data-testid="home-button">
      Back to Home
    </router-link>
  </main>
</template>