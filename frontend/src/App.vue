<!-- src/App.vue — FINAL: LIGHT BROWN BACKGROUND — SAME ON ALL PAGES -->
<template>
  <div class="min-h-screen relative">
    <!-- FORCED BACKGROUND — COVERS EVERYTHING -->
    <div 
      class="fixed inset-0 -z-50 bg-gradient-to-br from-amber-50 via-orange-50 to-yellow-50"
      style="background: linear-gradient(to bottom right, #fffbeb, #fff7ed, #fffde7) !important;"
    ></div>

    <!-- MAIN CONTENT — ABOVE BACKGROUND -->
    <router-view class="relative z-10" />
  </div>
</template>

<script setup>
// NO DARK MODE. NO TOGGLE. NO LOCALSTORAGE.
</script>

<style scoped>
/* INTER FONT */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@100..900&display=swap');
* {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

/* KILL ALL LINK STYLES */
a, a:hover, a:visited, a:active {
  color: inherit !important;
  text-decoration: none !important;
}

/* SMOOTH SCROLL */
html {
  scroll-behavior: smooth;
}
</style>