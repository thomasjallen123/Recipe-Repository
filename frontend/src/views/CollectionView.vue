<!-- src/views/CollectionView.vue — FINAL WITH BACK BUTTON -->
<script setup>
import { ref, onMounted, watch } from 'vue'
import { useRecipeStore } from '@/stores/recipes'
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'
import api from '@/services/api'
import RecipeCard from '@/components/RecipeCard.vue'

const recipeStore = useRecipeStore()
const authStore = useAuthStore()
const router = useRouter()

const savedRecipes = ref([])
const loading = ref(true)

const loadSavedRecipes = async () => {
  loading.value = true

  if (authStore.isAuthenticated) {
    try {
      const res = await api.get('/api/collections')
      savedRecipes.value = res.data.recipes || []
    } catch {
      savedRecipes.value = []
    }
  } else {
    if (recipeStore.savedRecipeIds.length === 0) {
      savedRecipes.value = []
    } else {
      const results = await Promise.allSettled(
        recipeStore.savedRecipeIds.map(id => api.get(`/recipes/${id}`))
      )
      savedRecipes.value = results
        .filter(r => r.status === 'fulfilled')
        .map(r => r.value.data)
    }
  }
  loading.value = false
}

onMounted(loadSavedRecipes)
watch(() => recipeStore.savedRecipeIds, loadSavedRecipes, { deep: true })
watch(() => authStore.isAuthenticated, loadSavedRecipes)
</script>

<template>
  <div class="min-h-screen bg-gradient-to-br from-pink-50 to-red-50 py-20">
    <div class="max-w-7xl mx-auto px-8 relative">
      <!-- BACK BUTTON — TOP LEFT -->
      <button
        @click="router.push('/search')"
        class="absolute top-0 left-8 flex items-center gap-2 text-red-700 hover:text-red-800 font-bold text-lg transition transform hover:-translate-x-1"
      >
        <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
        </svg>
        Back to Search
      </button>

      <!-- TITLE -->
      <h1 class="text-6xl font-black text-center text-red-700 mb-16 pt-12">
        {{ authStore.isAuthenticated ? 'My Collection' : 'My Favorites' }}
      </h1>

      <!-- LOADING -->
      <div v-if="loading" class="text-center py-40 text-4xl text-gray-600">
        Loading your saves...
      </div>

      <!-- EMPTY STATE -->
      <div v-else-if="savedRecipes.length === 0" class="text-center py-32 px-8">
        <p class="text-4xl md:text-5xl font-black text-gray-700 mb-8 leading-tight">
          No saved recipes yet
        </p>
        <router-link
          to="/search"
          class="inline-block px-12 py-5 bg-gradient-to-r from-red-600 to-pink-600 text-white text-xl font-bold rounded-full hover:shadow-2xl transform hover:scale-105 transition-all duration-300 shadow-lg"
        >
          Go Find Some Delicious Recipes
        </router-link>
      </div>

      <!-- RECIPE GRID -->
      <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-12 pb-10">
        <RecipeCard
          v-for="recipe in savedRecipes"
          :key="recipe.id"
          :recipe="recipe"
          @toggle-save="recipeStore.toggleSave(recipe)"
        />
      </div>
    </div>
  </div>
</template>