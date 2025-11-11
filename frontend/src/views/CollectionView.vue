<template>
  <div class="min-h-screen bg-gradient-to-br from-orange-400/20 via-red-400/20 to-yellow-500/20 container mx-auto px-6 py-12 max-w-7xl relative z-10 animate-pageIn">
    <h1 class="text-6xl font-black text-center bg-gradient-to-r from-red-600 to-yellow-600 bg-clip-text text-transparent mb-12 leading-tight typewriter">
      My Favorites
    </h1>

    <div v-if="favorites.length === 0" class="text-center py-32">
      <p class="text-4xl text-orange-800 mb-8 font-semibold animate-slideIn">Your collection is empty</p>
      <router-link
        to="/search"
        class="inline-block px-16 py-6 bg-gradient-to-r from-teal-500 to-lime-500 text-white text-2xl font-black rounded-3xl shadow-2xl hover:shadow-teal-500/50 transform hover:scale-105 transition-all duration-300 bounce-hover"
      >
        Explore Recipes
      </router-link>
    </div>

    <div v-else class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-10">
      <RecipeCard
        v-for="(recipe, index) in favorites"
        :key="recipe.id"
        :recipe="recipe"
        :index="index"
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
