<template>
  <div class="min-h-screen container mx-auto px-6 py-12 relative z-10 animate-pageIn">
    <h1 class="text-6xl font-black text-center bg-gradient-to-r from-teal-600 to-lime-600 bg-clip-text text-transparent mb-12 leading-tight typewriter">Search Recipes</h1>

    <div class="bg-gradient-to-r from-yellow-50/90 to-orange-50/90 backdrop-blur-md rounded-3xl shadow-2xl p-10 max-w-6xl mx-auto border border-teal-200/50 animate-slideIn">
      <div class="grid grid-cols-1 md:grid-cols-4 gap-6">
        <input
          v-model="filters.ingredient"
          @keyup.enter="search"
          placeholder="Search by ingredient (e.g. chicken)"
          class="px-6 py-5 border-2 border-teal-200 rounded-2xl text-lg focus:ring-4 focus:ring-teal-200/50 focus:border-teal-500 focus:outline-none placeholder-orange-400 transition-all bg-white/50 animate-slideIn delay-1"
        />
        <select v-model="filters.cuisine" class="px-6 py-5 border-2 border-teal-200 rounded-2xl text-lg focus:ring-4 focus:ring-teal-200/50 focus:border-teal-500 focus:outline-none bg-white/50 animate-slideIn delay-2">
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
          class="px-6 py-5 border-2 border-teal-200 rounded-2xl text-lg focus:ring-4 focus:ring-teal-200/50 focus:border-teal-500 focus:outline-none placeholder-orange-400 transition-all bg-white/50 animate-slideIn delay-3"
        />
        <button
          @click="search"
          class="bg-gradient-to-r from-teal-500 to-lime-500 hover:from-teal-600 hover:to-lime-600 text-white font-black text-xl px-10 py-5 rounded-2xl shadow-lg transform hover:scale-105 transition-all bounce-hover"
        >
          SEARCH
        </button>
      </div>
    </div>

    <div class="mt-16 grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-10 max-w-7xl mx-auto">
      <RecipeCard
        v-for="(recipe, index) in recipeStore.recipes"
        :key="recipe.id"
        :recipe="recipe"
        :index="index"
        @toggle-save="recipeStore.toggleSave(recipe)"
      />
    </div>

    <div v-if="recipeStore.loading" class="text-center py-20">
      <div class="inline-block animate-spin rounded-full h-20 w-20 border-8 border-teal-500 border-t-transparent shadow-lg"></div>
      <p class="mt-4 text-xl text-orange-800 font-semibold typewriter">Finding delicious recipes...</p>
    </div>

    <div v-if="!recipeStore.loading && recipeStore.recipes.length === 0" class="text-center py-20 text-2xl text-orange-800 font-semibold animate-slideIn">
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

<style scoped>
.delay-1 { animation-delay: 0.2s; }
.delay-2 { animation-delay: 0.4s; }
.delay-3 { animation-delay: 0.6s; }
</style>

