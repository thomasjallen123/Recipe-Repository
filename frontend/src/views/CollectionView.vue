<template>
  <div class="min-h-screen bg-gradient-to-br from-amber-50/50 to-yellow-50/50 container mx-auto px-6 py-12 max-w-7xl relative z-10">
    <h1 class="text-6xl font-black text-center text-indigo-700 mb-12 leading-tight animate-fadeIn">
      My Favorites
    </h1>

    <div v-if="favorites.length === 0" class="text-center py-32">
      <p class="text-4xl text-gray-600 mb-8 font-medium">Your collection is empty</p>
      <router-link
        to="/search"
        class="inline-block px-16 py-6 bg-gradient-to-r from-indigo-600 to-purple-600 text-white text-2xl font-black rounded-3xl shadow-2xl hover:shadow-indigo-500/50 transform hover:scale-105 transition-all duration-300"
      >
        Explore Recipes
      </router-link>
    </div>

    <div v-else class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-10">
      <RecipeCard
        v-for="recipe in favorites"
        :key="recipe.id"
        :recipe="recipe"
        @view="$router.push('/recipe/' + recipe.id)"
        @toggle-save="recipeStore.toggleSave(recipe)"
        class="animate-fadeInUp"
      />
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRecipeStore } from '@/stores/recipes'
import RecipeCard from '@/components/RecipeCard.vue'

const recipeStore = useRecipeStore()
const favorites = computed(() => recipeStore.recipes.filter(r => r.isSaved))
</script>

<style scoped>
/* SAME STAGGERED ANIMATION AS SEARCH */
.animate-fadeInUp {
  animation: fadeInUp 0.6s ease-out forwards;
}
@keyframes fadeInUp {
  from { opacity: 0; transform: translateY(30px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>
