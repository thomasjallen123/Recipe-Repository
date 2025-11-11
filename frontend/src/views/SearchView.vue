<template>
  <div class="min-h-screen container mx-auto px-6 py-12">
    <h1 class="text-5xl font-bold text-center text-indigo-700 mb-10">Search Recipes</h1>

    <div class="bg-white/80 backdrop-blur-sm rounded-2xl shadow-2xl p-8 max-w-5xl mx-auto">
      <div class="grid grid-cols-1 md:grid-cols-4 gap-6">
        <input
          v-model="filters.ingredient"
          @keyup.enter="search"
          placeholder="Search by ingredient (e.g. chicken)"
          class="px-6 py-4 border-2 border-gray-300 rounded-xl text-lg focus:border-indigo-600 focus:outline-none"
        />
        <select v-model="filters.cuisine" class="px-6 py-4 border-2 border-gray-300 rounded-xl text-lg">
          <option value="">All Cuisines</option>
          <option>Italian</option>
          <option>Mexican</option>
          <option>Indian</option>
          <option>Thai</option>
          <option>American</option>
        </select>
        <input
          v-model.number="filters.maxTime"
          type="number"
          placeholder="Max minutes"
          class="px-6 py-4 border-2 border-gray-300 rounded-xl text-lg"
        />
        <button
          @click="search"
          class="bg-indigo-600 hover:bg-indigo-700 text-white font-bold text-xl px-10 py-4 rounded-xl shadow-lg transform hover:scale-105 transition"
        >
          SEARCH
        </button>
      </div>
    </div>

    <div class="mt-12 grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-8 max-w-7xl mx-auto">
      <RecipeCard
        v-for="recipe in recipeStore.recipes"
        :key="recipe.id"
        :recipe="recipe"
        @view="$router.push('/recipe/' + recipe.id)"
        @toggle-save="recipeStore.toggleSave(recipe)"
      />
    </div>

    <div v-if="recipeStore.loading" class="text-center py-20">
      <div class="inline-block animate-spin rounded-full h-16 w-16 border-8 border-indigo-600 border-t-transparent"></div>
    </div>

    <div v-if="!recipeStore.loading && recipeStore.recipes.length === 0" class="text-center py-20 text-2xl text-gray-600">
      No recipes found. Try "chicken", "pasta", or "beef"!
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRecipeStore } from '@/stores/recipes'
import RecipeCard from '@/components/RecipeCard.vue'

const recipeStore = useRecipeStore()

const filters = ref({
  ingredient: 'chicken',
  cuisine: '',
  maxTime: null
})

const search = () => {
  recipeStore.search(filters.value)
}

onMounted(() => {
  search()
})
</script>

