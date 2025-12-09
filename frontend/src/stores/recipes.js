// src/stores/recipes.js
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import api from '@/services/api'
import { useAuthStore } from '@/stores/auth'

export const useRecipeStore = defineStore('recipes', () => {
  const recipes = ref([])
  const currentRecipe = ref(null)
  const savedRecipeIds = ref([])
  const loading = ref(false)
  const searchLoading = ref(false)
  const error = ref(null)

  const authStore = useAuthStore()

  const savedRecipes = computed(() =>
    recipes.value.filter(r => savedRecipeIds.value.includes(r.id))
  )

  const initSavedState = () => {
    const saved = localStorage.getItem('savedRecipeIds')
    if (saved) savedRecipeIds.value = JSON.parse(saved)
  }

  const search = async (filters = {}, append = false) => {
    searchLoading.value = true
    error.value = null
    try {
      const params = new URLSearchParams()
      Object.entries(filters).forEach(([k, v]) => v && params.append(k, v))

      const res = await api.get(`/recipes?${params}`)
      const newRecipes = res.data.recipes || []

      newRecipes.forEach(r => {
        r.isSaved = savedRecipeIds.value.includes(r.id)
      })

      if (append) {
        recipes.value.push(...newRecipes)
      } else {
        recipes.value = newRecipes
      }
    } catch (err) {
      error.value = 'Failed to load recipes'
    } finally {
      searchLoading.value = false
    }
  }

  const fetchRecipeById = async (id) => {
    loading.value = true
    try {
      const res = await api.get(`/recipes/${id}`)
      currentRecipe.value = res.data
      currentRecipe.value.isSaved = savedRecipeIds.value.includes(currentRecipe.value.id)
    } catch (err) {
      error.value = 'Recipe not found'
    } finally {
      loading.value = false
    }
  }

  const toggleSave = async (recipe) => {
    const id = recipe.id
    const wasSaved = savedRecipeIds.value.includes(id)

    // Optimistic UI update
    if (wasSaved) {
      savedRecipeIds.value = savedRecipeIds.value.filter(x => x !== id)
    } else {
      savedRecipeIds.value.push(id)
    }
    localStorage.setItem('savedRecipeIds', JSON.stringify(savedRecipeIds.value))

    // Update all instances
    const updateIsSaved = (r) => { if (r && r.id === id) r.isSaved = !wasSaved }
    if (currentRecipe.value) updateIsSaved(currentRecipe.value)
    recipes.value.forEach(updateIsSaved)

    // Sync with backend if logged in
    if (authStore.isAuthenticated) {
      try {
        await api.post(`/collections/${id}/toggle`)
      } catch (err) {
        console.error('Failed to sync save state with server')
        // Revert on failure
        toggleSave(recipe) // revert
      }
    }
  }

  initSavedState()

  return {
    recipes,
    currentRecipe,
    savedRecipes,
    savedRecipeIds,
    loading,
    searchLoading,
    error,
    search,
    fetchRecipeById,
    toggleSave
  }
})

