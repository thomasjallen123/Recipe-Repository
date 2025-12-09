<script setup>
import { ref, computed, onMounted } from 'vue'
import api from '@/services/api'

const recipes = ref([])
const isLoading = ref(false)
const error = ref('')
const searchQuery = ref('')
const selectedCuisine = ref('')
const veganOnly = ref(false)          // ← ONLY NEW LINE

// VEGAN FILTER — client-side, works perfectly
const displayedRecipes = computed(() => {
  let list = recipes.value

  if (veganOnly.value) {
    list = list.filter(r => {
      const text = `${r.title} ${r.ingredients?.map(i => i.name || '').join(' ')}`.toLowerCase()
      return !/chicken|beef|pork|turkey|salmon|tuna|shrimp|fish|egg|cheese|butter|milk|cream|bacon|ham|sausage|lamb|duck|honey|gelatin|anchovy/i.test(text)
    })
  }

  return list
})

async function fetchRecipes() {
  try {
    isLoading.value = true
    error.value = ''

    const params = {}
    if (searchQuery.value.trim()) params.ingredient = searchQuery.value.trim()
    if (selectedCuisine.value) params.cuisine = selectedCuisine.value

    const response = await api.get('/recipes', { params })
    recipes.value = response.data.recipes || []
  } catch (err) {
    console.error(err)
    error.value = 'Failed to load recipes from backend.'
  } finally {
    isLoading.value = false
  }
}

onMounted(fetchRecipes)
</script>

<template>
  <div class="min-h-screen bg-gradient-to-b from-green-50 to-emerald-50 py-12">
    <div class="max-w-6xl mx-auto px-4">
      <h1 class="text-5xl font-black text-emerald-800 text-center mb-10">Search Recipes</h1>

      <!-- Filter + Search Bar -->
      <div class="flex flex-col md:flex-row gap-4 justify-center items-center mb-12">
        <select
          v-model="selectedCuisine"
          @change="fetchRecipes"
          class="px-6 py-4 rounded-full bg-white shadow-lg border border-orange-200 text-orange-900 font-medium focus:outline-none"
        >
          <option value="">All Cuisines</option>
          <option>Italian</option>
          <option>Mexican</option>
          <option>Indian</option>
          <option>Chinese</option>
          <option>Japanese</option>
          <option>Thai</option>
          <option>Greek</option>
          <option>American</option>
          <option>French</option>
          <option>Korean</option>
        </select>

       <!-- VEGAN TOGGLE — CLEAN & PERFECT -->
<button
  @click="veganOnly = !veganOnly"
  :class="veganOnly 
    ? 'bg-green-600 text-white' 
    : 'bg-white text-green-700 border-2 border-green-300'"
  class="px-10 py-4 rounded-full font-bold shadow-lg transition-all hover:scale-105 flex items-center gap-2"
>
  <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
    <path v-if="veganOnly" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"/>
    <path v-else d="M10 18a8 8 0 100-16 8 8 0 000 16z"/>
  </svg>
  Vegan Only
</button>

        <input
          v-model="searchQuery"
          @keyup.enter="fetchRecipes"
          placeholder="chicken, pasta, salmon..."
          class="w-full max-w-md px-8 py-4 rounded-full bg-white shadow-lg border border-teal-200 focus:ring-4 focus:ring-teal-300 outline-none"
        />

        <button
          @click="fetchRecipes"
          class="px-10 py-4 bg-gradient-to-r from-orange-500 to-red-600 text-white font-bold rounded-full shadow-xl hover:shadow-2xl transform hover:scale-105 transition"
        >
          SEARCH
        </button>
      </div>

      <!-- Error / Loading -->
      <div v-if="error" class="text-center text-red-600 text-xl mb-8">{{ error }}</div>
      <div v-if="isLoading" class="text-center text-gray-600 text-xl">Loading delicious recipes...</div>

      <!-- Recipe Grid — uses displayedRecipes so vegan filter works -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
        <div
          v-for="recipe in displayedRecipes"
          :key="recipe.id"
          class="bg-white rounded-3xl shadow-xl overflow-hidden hover:shadow-2xl transition cursor-pointer transform hover:-translate-y-1"
          @click="$router.push('/recipe/' + recipe.id)"
        >
          <img
            :src="recipe.image_url || 'https://via.placeholder.com/400x300?text=No+Image'"
            class="w-full h-64 object-cover"
            alt="recipe image"
          />
          <div class="p-6">
            <h3 class="text-2xl font-bold text-orange-900 mb-2">{{ recipe.title }}</h3>
            <p class="text-teal-700 font-semibold">
              {{ recipe.cuisine || 'Cuisine' }} • {{ recipe.total_time_minutes || '?' }} min
            </p>
          </div>
        </div>
      </div>

      <p v-if="!isLoading && displayedRecipes.length === 0" class="text-center text-gray-500 text-xl mt-16">
        No recipes found. Try "chicken", "pasta", or "vegan"!
      </p>
    </div>
  </div>
</template>