<template>
  <div class="min-h-screen flex flex-col items-center justify-center px-4 sm:px-6 lg:px-8 py-12 relative overflow-hidden animate-pageIn" style="direction: ltr;">
    <!-- LOGIN BUTTON — TOP RIGHT FIXED (HARD OVERRIDE) -->
    <router-link
      to="/login"
      class="fixed top-4 right-4 left-auto text-2xl font-bold text-orange-800 relative after:absolute after:bottom-0 after:left-0 after:w-0 after:h-1 after:bg-gradient-to-r after:from-teal-500 after:to-lime-500 after:transition-all after:duration-500 hover:after:w-full px-6 py-3 rounded-xl bg-yellow-100/80 backdrop-blur-sm hover:bg-red-100/80 transition-all bounce-hover z-50 md:text-xl md:px-4 md:py-2" style="left: auto !important; right: 1rem !important; transform: translateX(0) !important;"
    >
      Login
    </router-link>

    <!-- ENHANCED FLOATING ELEMENTS -->
    <div class="absolute inset-0 pointer-events-none">
      <div class="absolute top-10 left-20 w-32 h-32 bg-red-400/10 rounded-full blur-xl animate-float fast"></div>
      <div class="absolute bottom-32 right-32 w-40 h-40 bg-yellow-400/10 rounded-full blur-xl animate-float medium"></div>
    </div>
    
    <div class="w-full max-w-7xl mx-auto text-center z-10 flex flex-col items-center justify-center">
      <h1 class="block text-7xl md:text-9xl font-black tracking-tight bg-gradient-to-r from-teal-500 via-lime-500 to-red-500 bg-clip-text text-transparent drop-shadow-2xl mb-12 typewriter" style="margin-left: auto; margin-right: auto; width: fit-content; line-height: 1.1;">
        Recipe Repository
      </h1>

      <p class="mt-12 text-xl md:text-2xl font-medium text-orange-800 max-w-6xl px-8 animate-slideIn delay-1" style="margin-left: auto; margin-right: auto; width: fit-content; line-height: 1.8; max-width: 80%;">
        Our platform empowers users to seamlessly explore a wide variety of recipes sourced directly from trusted sites like AllRecipes and Food Network. 
        Whether you're searching for everyday meals or trying something completely new, you can easily save your favorite dishes, organize them for later, and personalize serving sizes using our built-in recipe scaling tools.
      </p>

      <div class="mt-20 flex flex-col sm:flex-row gap-8 justify-center items-center">
        <router-link
          to="/search"
          class="group relative px-12 py-6 bg-gradient-to-r from-teal-500/20 to-lime-500/20 backdrop-blur-xl border-2 border-teal-300/50 rounded-3xl shadow-2xl hover:shadow-teal-500/50 transition-all duration-500 hover:scale-105 overflow-hidden bounce-hover"
        >
          <span class="text-2xl font-bold bg-gradient-to-r from-teal-600 to-lime-600 bg-clip-text text-transparent relative z-10 group-hover:from-red-600 group-hover:to-yellow-600 transition-colors">
            Explore Recipes
          </span>
          <div class="absolute inset-0 rounded-3xl bg-gradient-to-r from-teal-500/40 to-lime-500/40 blur-xl group-hover:blur-2xl transition-all"></div>
        </router-link>

        <router-link
          to="/collection"
          class="group relative px-12 py-6 bg-gradient-to-r from-red-500/20 to-yellow-500/20 backdrop-blur-xl border-2 border-red-300/50 rounded-3xl shadow-2xl hover:shadow-red-500/50 transition-all duration-500 hover:scale-105 overflow-hidden bounce-hover"
        >
          <span class="text-2xl font-bold bg-gradient-to-r from-red-600 to-yellow-600 bg-clip-text text-transparent relative z-10 group-hover:from-lime-600 group-hover:to-teal-600 transition-colors">
            My Favorites
          </span>
          <div class="absolute inset-0 rounded-3xl bg-gradient-to-r from-red-500/40 to-yellow-500/40 blur-xl group-hover:blur-2xl transition-all"></div>
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
// UNCHANGED
</script>

<style scoped>
.animate-slideIn {
  opacity: 0;
  transform: translateY(30px);
  animation: slideIn 1s ease-out forwards;
}
@keyframes slideIn {
  to { opacity: 1; transform: translateY(0); }
}
.delay-1 { animation-delay: 0.5s; }
</style>
