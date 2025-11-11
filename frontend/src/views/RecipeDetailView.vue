<template>
  <div class="min-h-screen container mx-auto px-4 py-8">
    <button @click="$router.back()" class="mb-6 text-indigo-600 font-medium text-lg hover:underline">
      Back to Search
    </button>

    <div v-if="!recipe" class="text-center py-32 text-3xl text-gray-500">
      Recipe not found
    </div>

    <div v-else class="bg-white/90 backdrop-blur-sm rounded-3xl shadow-2xl overflow-hidden">
      <img :src="recipe.image" class="w-full h-96 object-cover" alt="Recipe" />

      <div class="p-10">
        <div class="flex justify-between items-start mb-8">
          <div>
            <h1 class="text-5xl font-bold text-gray-800 mb-3">{{ recipe.title }}</h1>
            <p class="text-2xl text-gray-600">
              {{ recipe.cuisine }} • {{ recipe.cookTime }} min • Serves {{ servings }}
            </p>
          </div>

          <button @click="toggleSave" class="hover:scale-110 transition">
            <svg v-if="recipe.isSaved" style="width: 48px; height: 48px;" class="text-red-600" fill="currentColor" viewBox="0 0 24 24">
              <path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z"/>
            </svg>
            <svg v-else style="width: 48px; height: 48px;" class="text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"/>
            </svg>
          </button>
        </div>

        <div class="mb-10 p-6 bg-indigo-50/80 rounded-2xl inline-block">
          <ServingScaler v-model:servings="servings" :original-servings="originalServings" />
        </div>

        <h2 class="text-3xl font-bold mb-6 text-gray-800">Ingredients</h2>
        <ul class="space-y-4 text-lg bg-indigo-50/50 p-6 rounded-2xl">
          <li v-for="ing in scaledIngredients" class="flex items-center">
            <span class="font-bold text-indigo-600 w-32">{{ ing.scaled }} {{ ing.unit || '' }}</span>
            <span class="text-gray-700">{{ ing.name }}</span>
          </li>
        </ul>

        <h2 class="text-3xl font-bold mt-12 mb-6 text-gray-800">Instructions</h2>
        <p class="text-lg text-gray-700 leading-relaxed whitespace-pre-line bg-indigo-50/50 p-6 rounded-2xl">
          {{ recipe.instructions }}
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { mockRecipes } from '@/services/mockData.js'
import { useRecipeStore } from '@/stores/recipes'
import ServingScaler from '@/components/ServingScaler.vue'

const route = useRoute()
const recipeStore = useRecipeStore()
const recipe = ref(null)
const servings = ref(4)
const originalServings = ref(4)

onMounted(() => {
  const id = parseInt(route.params.id)
  recipe.value = mockRecipes.find(r => r.id === id)
  if (recipe.value) {
    originalServings.value = recipe.value.servings || 4
    servings.value = originalServings.value
  }
})

const scaledIngredients = computed(() => {
  if (!recipe.value) return []
  const scale = servings.value / originalServings.value
  return recipe.value.ingredients.map(i => ({
    ...i,
    scaled: (i.quantity * scale).toFixed(1).replace(/\.0$/, '')
  }))
})

const toggleSave = () => {
  if (recipe.value) {
    recipeStore.toggleSave(recipe.value)
  }
}
</script>

