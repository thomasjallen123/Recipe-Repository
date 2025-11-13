<!-- src/views/CollectionView.vue -->
<template>
  <main class="min-h-screen bg-gradient-to-br from-amber-50/50 to-yellow-50/50 container mx-auto px-4 sm:px-6 py-12 max-w-7xl relative z-10">
    <header class="text-center mb-12">
      <h1 class="text-5xl sm:text-6xl font-black text-teal-700 leading-tight animate-fadeIn" aria-label="My Favorite Recipes">
        My Favorites
      </h1>
    </header>

    <div v-if="loading" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-8">
      <div v-for="n in 6" :key="n" class="bg-white/70 p-6 rounded-2xl shadow animate-pulse">
        <div class="h-6 bg-gray-300 rounded mb-4"></div>
        <div class="h-4 bg-gray-300 rounded w-3/4"></div>
      </div>
    </div>

    <div v-else-if="favorites.length === 0" class="text-center py-32">
      <p class="text-3xl sm:text-4xl text-gray-600 mb-8 font-medium">Your collection is empty</p>
      <router-link :to="{ name: 'Search' }" class="inline-block px-12 py-5 bg-gradient-to-r from-teal-600 to-teal-600 text-white text-xl font-black rounded-3xl shadow-2xl hover:shadow-teal-500/50 transform hover:scale-105 transition-all duration-300">
        Explore Recipes
      </router-link>
    </div>

    <div v-else class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-8">
      <div
        v-for="recipe in favorites"
        :key="recipe.id"
        class="bg-white p-6 rounded-2xl shadow-lg hover:shadow-xl transition cursor-pointer relative group"
        @click="goToRecipe(recipe.id)"
      >
        <button
          @click.stop="toggleSave(recipe)"
          class="absolute top-4 right-4 w-10 h-10 bg-white/80 backdrop-blur rounded-full shadow flex items-center justify-center hover:scale-110 transition"
        >
          <svg v-if="recipe.isSaved" class="w-6 h-6 text-red-500" fill="currentColor" viewBox="0 0 24 24">
            <path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z"/>
          </svg>
          <svg v-else class="w-6 h-6 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"/>
          </svg>
        </button>
        <h3 class="text-xl font-bold text-teal-700">{{ recipe.title }}</h3>
        <p class="text-gray-600">{{ recipe.cuisine }} • {{ recipe.cookTime }} min</p>
      </div>
    </div>
  </main>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const favorites = ref([])
const loading = ref(true)

// Mock saved recipes
const mockSaved = [
  { id: 1, title: "Spicy Chicken Curry", cuisine: "Indian", cookTime: 45, isSaved: true },
  { id: 3, title: "Pasta Carbonara", cuisine: "Italian", cookTime: 25, isSaved: true },
]

const toggleSave = (recipe) => {
  recipe.isSaved = !recipe.isSaved
  if (!recipe.isSaved) {
    favorites.value = favorites.value.filter(r => r.id !== recipe.id)
  }
}

const goToRecipe = (id) => {
  router.push({ name: 'RecipeDetail', params: { id } })
}

onMounted(() => {
  setTimeout(() => {
    favorites.value = mockSaved
    loading.value = false
  }, 500)
})
</script>

<style scoped>
.animate-fadeIn { animation: fadeIn 0.8s ease-out; }
@keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
</style>
