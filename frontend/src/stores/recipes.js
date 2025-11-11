// src/stores/recipes.js
import { defineStore } from 'pinia'
import { mockRecipes } from '@/services/mockData.js'

export const useRecipeStore = defineStore('recipes', {
  state: () => ({
    recipes: [],
    loading: false,
    error: null,
    savedRecipeIds: [] // <-- tracks saved IDs
  }),

  actions: {
    // Load saved state from localStorage
    initSavedState() {
      const saved = localStorage.getItem('savedRecipeIds')
      if (saved) {
        this.savedRecipeIds = JSON.parse(saved)
        mockRecipes.forEach(r => {
          r.isSaved = this.savedRecipeIds.includes(r.id)
        })
      }
    },

    // Toggle save
    toggleSave(recipe) {
      const idx = this.savedRecipeIds.indexOf(recipe.id)
      if (idx > -1) {
        this.savedRecipeIds.splice(idx, 1)
        recipe.isSaved = false
      } else {
        this.savedRecipeIds.push(recipe.id)
        recipe.isSaved = true
      }
      localStorage.setItem('savedRecipeIds', JSON.stringify(this.savedRecipeIds))
    },

    // Search
    async search(filters = {}) {
      this.loading = true
      this.error = null

      if (this.savedRecipeIds.length === 0) this.initSavedState()

      try {
        let results = [...mockRecipes]

        if (filters.ingredient) {
          const term = filters.ingredient.toLowerCase()
          results = results.filter(
            r =>
              r.title.toLowerCase().includes(term) ||
              r.ingredients.some(i => i.name.toLowerCase().includes(term))
          )
        }
        if (filters.cuisine) {
          results = results.filter(r => r.cuisine === filters.cuisine)
        }
        if (filters.maxTime) {
          results = results.filter(r => r.cookTime <= filters.maxTime)
        }

        await new Promise(r => setTimeout(r, 600))
        this.recipes = results
      } catch (err) {
        this.error = 'Search failed'
        console.error(err)
      } finally {
        this.loading = false
      }
    }
  },

  onStoreSetup() {
    this.initSavedState()
    this.search({ ingredient: 'chicken' })
  }
})