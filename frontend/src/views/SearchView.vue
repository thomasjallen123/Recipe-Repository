<!-- src/views/SearchView.vue -->
<template>
  <main class="min-h-screen bg-gradient-to-br from-teal-50 to-lime-50 p-8 relative">
    <div class="max-w-6xl mx-auto">
      <h1 class="text-5xl font-black text-center text-teal-700 mb-12">Search Recipes</h1>

      <!-- Search Bar -->
      <form @submit.prevent="search" class="mb-12">
        <div class="flex gap-4 max-w-2xl mx-auto">
          <input
            v-model="query"
            @input="debouncedSearch"
            placeholder="Search recipes (e.g. chicken, pasta)"
            class="flex-1 px-6 py-4 text-lg border-2 border-teal-300 rounded-xl focus:outline-none focus:ring-4 focus:ring-teal-200"
          />
          <button
            type="submit"
            class="px-8 py-4 bg-teal-600 text-white font-bold rounded-xl hover:bg-teal-700 transition"
          >
            Search
          </button>
        </div>
      </form>

      <!-- Loading -->
      <div v-if="loading" class="grid grid-cols-1 md:grid-cols-3 gap-8">
        <div v-for="n in 6" :key="n" class="bg-white/70 backdrop-blur p-6 rounded-2xl shadow animate-pulse">
          <div class="h-6 bg-gray-300 rounded mb-4"></div>
          <div class="h-4 bg-gray-300 rounded w-3/4"></div>
        </div>
      </div>

      <!-- No Results -->
      <div v-else-if="results.length === 0" class="text-center py-20 text-xl text-gray-600">
        No recipes found. Try "chicken" or "beef".
      </div>

      <!-- Results -->
      <div v-else class="grid grid-cols-1 md:grid-cols-3 gap-8">
        <div
          v-for="recipe in results"
          :key="recipe.id"
          class="bg-white p-6 rounded-2xl shadow-lg hover:shadow-xl transition cursor-pointer relative group"
          @click="goToRecipe(recipe.id)"
        >
          <!-- Save Button -->
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
    </div>

    <!-- Floating Collection Button -->
    <router-link
      to="/collection"
      class="fixed bottom-8 right-8 w-16 h-16 bg-red-500 text-white rounded-full shadow-lg flex items-center justify-center hover:scale-110 transition z-50"
    >
      <svg class="w-8 h-8" fill="currentColor" viewBox="0 0 24 24">
        <path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z"/>
      </svg>
    </router-link>
  </main>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { debounce } from 'lodash-es'

// All 3 recipes
const allRecipes = [
  { id: 1, title: "Spicy Chicken Curry", cuisine: "Indian", cookTime: 45, isSaved: false },
  { id: 2, title: "Beef Tacos", cuisine: "Mexican", cookTime: 20, isSaved: false },
  { id: 3, title: "Pasta Carbonara", cuisine: "Italian", cookTime: 25, isSaved: false },
]

const query = ref('')
const results = ref([])
const loading = ref(false)
const router = useRouter()

const search = () => {
  loading.value = true
  setTimeout(() => {
    if (!query.value) {
      results.value = allRecipes
    } else {
      results.value = allRecipes.filter(r =>
        r.title.toLowerCase().includes(query.value.toLowerCase()) ||
        r.cuisine.toLowerCase().includes(query.value.toLowerCase())
      )
    }
    loading.value = false
  }, 300)
}

const debouncedSearch = debounce(search, 400)

const toggleSave = (recipe) => {
  recipe.isSaved = !recipe.isSaved
  // Optional: Save to localStorage
  localStorage.setItem('savedRecipes', JSON.stringify(allRecipes.filter(r => r.isSaved)))
}

const goToRecipe = (id) => {
  router.push({ name: 'RecipeDetail', params: { id } })
}

onMounted(() => {
  search()
  // Load saved state
  const saved = localStorage.getItem('savedRecipes')
  if (saved) {
    const savedIds = JSON.parse(saved).map(r => r.id)
    allRecipes.forEach(r => {
      if (savedIds.includes(r.id)) r.isSaved = true
    })
  }
})
</script>

