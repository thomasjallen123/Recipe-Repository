// src/stores/recipes.js
import { defineStore } from 'pinia'
import api from '@/services/api'
import { mockRecipes } from '@/services/mockData.js'

export const useRecipeStore = defineStore('recipes', {
  state: () => ({
    recipes: [],
    loading: false,
    error: null
  }),
  actions: {
    async search(filters = {}) {
      this.loading = true
      this.error = null
      try {
        // MOCK MODE — USE MOCK DATA
        let results = [...mockRecipes]

        if (filters.ingredient) {
          const term = filters.ingredient.toLowerCase()
          results = results.filter(r =>
            r.ingredients.some(i => i.name.toLowerCase().includes(term)) ||
            r.title.toLowerCase().includes(term)
          )
        }
        if (filters.cuisine) {
          results = results.filter(r => r.cuisine === filters.cuisine)
        }
        if (filters.maxTime) {
          results = results.filter(r => r.cookTime <= filters.maxTime)
        }

        // Fake delay
        await new Promise(resolve => setTimeout(resolve, 600))

        this.recipes = results
        console.log('LOADED RECIPES:', this.recipes.length)  // ← CHECK CONSOLE
      } catch (err) {
        this.error = 'Search failed'
        console.error(err)
      } finally {
        this.loading = false
      }
    }
  }
})