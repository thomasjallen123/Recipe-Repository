<!-- src/views/RecipeDetailView.vue — FINAL FIX: Uses Pinia, not localStorage -->
<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useRecipeStore } from '@/stores/recipes'
import api from '@/services/api'

const route = useRoute()
const recipeStore = useRecipeStore()

const recipe = ref(null)
const baseServings = ref(1)
const servings = ref(1)
const isLoading = ref(true)
const error = ref('')

// Use Pinia store instead of localStorage
const isSaved = computed(() => {
  if (!recipe.value) return false
  return recipeStore.savedRecipeIds.includes(recipe.value.id)
})

const toggleSave = () => {
  if (!recipe.value) return
  recipeStore.toggleSave(recipe.value)
}

// Capitalized cuisine
const displayCuisine = computed(() => {
  if (!recipe.value?.cuisine) return 'Cuisine'
  return recipe.value.cuisine
    .split(' ')
    .map(word => word.charAt(0).toUpperCase() + word.slice(1).toLowerCase())
    .join(' ')
})

// Smart difficulty
const displayDifficulty = computed(() => {
  const d = recipe.value?.difficulty
  if (!d || d === 'N/A') {
    const time = recipe.value?.total_time_minutes || 0
    if (time < 30) return 'Easy'
    if (time < 90) return 'Medium'
    return 'Hard'
  }
  return d.charAt(0).toUpperCase() + d.slice(1).toLowerCase()
})

// Scale ingredients
const scaledIngredients = computed(() => {
  if (!recipe.value) return []
  const base = baseServings.value || recipe.value.servings || 1
  return (recipe.value.ingredients || []).map(ing => {
    let qty = ing.quantity
    const num = parseFloat(qty)
    if (!isNaN(num)) {
      const scaled = (num * servings.value) / base
      qty = Number.isInteger(scaled) ? scaled.toString() : scaled.toFixed(2)
    }
    return { ...ing, scaledQuantity: qty }
  })
})

async function loadRecipe() {
  try {
    isLoading.value = true
    error.value = ''

    const id = route.params.id
    const resp = await api.get(`/recipes/${id}`)
    
    recipe.value = resp.data
    baseServings.value = resp.data.servings || 1
    servings.value = baseServings.value
  } catch (err) {
    console.error(err)
    error.value = 'Failed to load recipe.'
  } finally {
    isLoading.value = false
  }
}

onMounted(loadRecipe)
</script>

<template>
  <div class="min-h-screen bg-gradient-to-b from-green-50 to-emerald-50 pb-16">
    <div class="max-w-4xl mx-auto px-4 pt-10">
      <router-link to="/search" class="text-sm text-teal-600 hover:underline">
        ← Back to search
      </router-link>

      <div v-if="isLoading" class="mt-8 text-center text-gray-600">Loading recipe...</div>
      <div v-else-if="error" class="mt-8 text-center text-red-600">{{ error }}</div>

      <div v-else-if="recipe" class="mt-8 bg-white rounded-2xl shadow-md p-6 md:p-8">
        <!-- Title + Heart -->
        <div class="flex justify-between items-start mb-6">
          <h1 class="text-3xl font-bold text-emerald-800">{{ recipe.title }}</h1>

          <!-- HEART ON DETAIL PAGE — NOW WORKS WITH PINIA -->
          <button
            @click="toggleSave"
            class="bg-white/90 p-4 rounded-full shadow-xl hover:scale-110 transition backdrop-blur border border-red-200"
          >
            <svg v-if="isSaved" class="w-8 h-8 text-red-500 animate-pulse" fill="currentColor" viewBox="0 0 24 24">
              <path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z"/>
            </svg>
            <svg v-else class="w-8 h-8 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"/>
            </svg>
          </button>
        </div>

        <p class="text-gray-600 mb-2"><strong>Cuisine:</strong> {{ displayCuisine }}</p>
        <p class="text-gray-600 mb-2"><strong>Total time:</strong> {{ recipe.total_time_minutes || '?' }} min</p>
        <p class="text-gray-600 mb-4"><strong>Difficulty:</strong> {{ displayDifficulty }}</p>

        <div class="mb-6 flex items-center gap-3">
          <label class="font-semibold text-gray-700">Servings:</label>
          <input type="number" v-model.number="servings" min="1" class="w-20 px-2 py-1 border rounded-md text-center" />
          <span class="text-sm text-gray-500">(original: {{ baseServings }})</span>
        </div>

        <div class="grid md:grid-cols-2 gap-8">
          <div>
            <h2 class="text-xl font-semibold text-emerald-700 mb-3">Ingredients</h2>
            <ul class="list-disc list-inside space-y-1 text-gray-700">
              <li v-for="ing in scaledIngredients" :key="ing.id">
                <span class="font-medium">
                  {{ ing.scaledQuantity || ing.quantity }}
                  <span v-if="ing.unit"> {{ ing.unit }}</span>
                </span>
                {{ ' ' + ing.name }}
              </li>
            </ul>
          </div>

          <div>
            <h2 class="text-xl font-semibold text-emerald-700 mb-3">Instructions</h2>
            <ol class="list-decimal list-inside space-y-2 text-gray-700">
              <li v-for="step in recipe.instructions" :key="step.step_number">
                {{ step.step_text }}
              </li>
            </ol>
          </div>
        </div>

        <div v-if="recipe.source_url" class="mt-6">
          <a :href="recipe.source_url" target="_blank" class="text-sm text-teal-600 hover:underline">
            Original source →
          </a>
        </div>
      </div>
    </div>
  </div>
</template>
