<template>
  <div class="container mx-auto px-4 py-8 max-w-7xl">
    <h1 class="text-4xl font-bold text-indigo-600 mb-8">Search Recipes</h1>

    <div class="bg-white p-6 rounded-xl shadow-lg mb-8">
      <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
        <input
          v-model="filters.ingredient"
          @keyup.enter="search"
          placeholder="Ingredient (e.g. chicken)"
          class="px-4 py-3 border rounded-lg focus:ring-2 focus:ring-indigo-500"
        />
        <select v-model="filters.cuisine" class="px-4 py-3 border rounded-lg">
          <option value="">All Cuisines</option>
          <option>Italian</option>
          <option>Mexican</option>
          <option>Indian</option>
          <option>Thai</option>
        </select>
        <input
          v-model.number="filters.maxTime"
          type="number"
          placeholder="Max minutes"
          class="px-4 py-3 border rounded-lg"
        />
        <button
          @click="search"
          class="bg-indigo-600 text-white px-8 py-3 rounded-lg hover:bg-indigo-700 font-medium"
        >
          SEARCH
        </button>
      </div>
    </div>

    <!-- LOADING SPINNER -->
    <div v-if="recipeStore.loading" class="text-center py-20">
      <div class="inline-block animate-spin rounded-full h-16 w-16 border-8 border-indigo-600 border-t-transparent"></div>
    </div>

    <!-- NO RESULTS -->
    <div v-else-if="recipeStore.recipes.length === 0" class="text-center py-20 text-gray-500 text-xl">
      No recipes found. Try "chicken", "pasta", "beef", or "rice"!
    </div>

    <!-- RECIPE GRID -->
    <div v-else class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-8">
      <RecipeCard
        v-for="recipe in recipeStore.recipes"
        :key="recipe.id"
        :recipe="recipe"
        @view="$router.push('/recipe/' + recipe.id)"
        @toggle-save="toggleSave(recipe)"
      />
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

const search = async () => {
  console.log('SEARCHING WITH:', filters.value)  // ← YOU WILL SEE THIS IN CONSOLE
  await recipeStore.search(filters.value)
}

const toggleSave = (recipe) => {
  recipe.isSaved = !recipe.isSaved
}

// AUTO-SEARCH ON LOAD
onMounted(() => {
  search()
})
</script>