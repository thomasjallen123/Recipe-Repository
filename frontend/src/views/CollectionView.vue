<!-- src/views/CollectionView.vue -->
<template>
  <div class="min-h-screen bg-[#FAF0E6] container mx-auto px-6 py-12 max-w-7xl">
    <h1 class="text-5xl font-bold text-center text-indigo-700 mb-12">
      My Favorites
    </h1>

    <div v-if="favorites.length === 0" class="text-center py-32">
      <p class="text-3xl text-gray-600 mb-8">Your collection is empty</p>
      <router-link
        to="/search"
        class="px-12 py-6 bg-gradient-to-r from-indigo-600 to-purple-600 text-white text-2xl font-bold rounded-full shadow-2xl hover:shadow-indigo-500/50 transform hover:scale-105 transition"
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
