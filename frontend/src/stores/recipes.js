// src/stores/recipes.js
import { defineStore } from 'pinia'
import api from '@/services/api'
import { mockRecipes } from '@/services/mockData.js'

export const useRecipeStore = defineStore('recipes', () => {
  const recipes = ref([])
  const currentRecipe = ref(null)
  const savedRecipeIds = ref([])
  const loading = ref(false)
  const searchLoading = ref(false)
  const error = ref(null)
  const total = ref(0)
  const page = ref(1)
  const limit = ref(20)

  const savedRecipes = computed(() => recipes.value.filter(r => savedRecipeIds.value.includes(r.id)))
  const hasMore = computed(() => recipes.value.length < total.value)

  const initSavedState = () => {
    const saved = localStorage.getItem('savedRecipeIds')
    if (saved) savedRecipeIds.value = JSON.parse(saved)
  }

  const search = async (filters = {}, append = false) => {
    searchLoading.value = true
    error.value = null
    try {
      const params = new URLSearchParams()
      Object.keys(filters).forEach(k => filters[k] && params.append(k, filters[k]))
      params.append('page', page.value)
      params.append('limit', limit.value)

      let data
      if (import.meta.env.VITE_MOCK_API === 'true') {
        await new Promise(r => setTimeout(r, 500))
        let results = [...mockRecipes]
        if (filters.ingredient) {
          const term = filters.ingredient.toLowerCase()
          results = results.filter(r =>
            r.title.toLowerCase().includes(term) ||
            r.ingredients.some(i => i.name.toLowerCase().includes(term))
          )
        }
        if (filters.cuisine) results = results.filter(r => r.cuisine === filters.cuisine)
        if (filters.maxTime) results = results.filter(r => r.cookTime <= filters.maxTime)
        const start = (page.value - 1) * limit.value
        data = { recipes: results.slice(start, start + limit.value), total: results.length }
      } else {
        const res = await api.get(`/recipes?${params}`)
        data = res.data
      }

      data.recipes.forEach(r => { r.isSaved = savedRecipeIds.value.includes(r.id) })
      if (append) recipes.value.push(...data.recipes)
      else recipes.value = data.recipes
      total.value = data.total
      page.value = append ? page.value + 1 : 1
    } catch (err) {
      error.value = 'Search failed'
    } finally {
      searchLoading.value = false
    }
  }

  const fetchRecipeById = async (id) => {
    loading.value = true
    try {
      if (import.meta.env.VITE_MOCK_API === 'true') {
        await new Promise(r => setTimeout(r, 300))
        currentRecipe.value = mockRecipes.find(r => r.id === parseInt(id)) || null
      } else {
        const res = await api.get(`/recipes/${id}`)
        currentRecipe.value = res.data
      }
      if (currentRecipe.value) currentRecipe.value.isSaved = savedRecipeIds.value.includes(currentRecipe.value.id)
    } catch (err) {
      error.value = 'Recipe not found'
    } finally {
      loading.value = false
    }
  }

  const toggleSave = (recipe) => {
    const id = recipe.id
    const idx = savedRecipeIds.value.indexOf(id)
    if (idx > -1) {
      savedRecipeIds.value.splice(idx, 1)
      recipe.isSaved = false
    } else {
      savedRecipeIds.value.push(id)
      recipe.isSaved = true
    }
    localStorage.setItem('savedRecipeIds', JSON.stringify(savedRecipeIds.value))
  }

  initSavedState()

  return {
    recipes, currentRecipe, savedRecipes, loading, searchLoading, error, total, hasMore,
    search, fetchRecipeById, toggleSave, loadMore: () => hasMore.value && search({}, true)
  }
})

