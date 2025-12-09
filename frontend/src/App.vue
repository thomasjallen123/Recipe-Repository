<!-- src/App.vue — FINAL: Floating heart only on Search & Collection -->
<template>
  <div class="min-h-screen bg-gradient-to-br from-teal-50 to-lime-50">
    <router-view />

    <!-- Floating Heart Button — ONLY on /search and /collection -->
    <router-link
      v-if="$route.path === '/search' || $route.path === '/collection'"
      to="/collection"
      class="fixed bottom-8 right-8 z-50 bg-gradient-to-br from-red-500 to-pink-600 text-white p-5 rounded-full shadow-2xl hover:shadow-red-600/60 transform hover:scale-110 transition-all duration-300 flex items-center justify-center"
    >
      <svg class="w-8 h-8" fill="currentColor" viewBox="0 0 24 24">
        <path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z"/>
      </svg>

      <transition name="fade">
        <span 
          v-if="savedCount > 0"
          class="absolute -top-2 -right-2 bg-yellow-400 text-red-800 text-xs font-bold px-2.5 py-1 rounded-full min-w-[28px] shadow-lg animate-bounce"
        >
          {{ savedCount }}
        </span>
      </transition>
    </router-link>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRecipeStore } from '@/stores/recipes'
import { storeToRefs } from 'pinia'

const recipeStore = useRecipeStore()
const { savedRecipeIds } = storeToRefs(recipeStore)
const savedCount = computed(() => savedRecipeIds.value.length)
</script>

<style scoped>
.fade-enter-active, .fade-leave-active {
  transition: all 0.3s ease;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}
</style>