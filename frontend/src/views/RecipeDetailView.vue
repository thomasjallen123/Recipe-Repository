<!-- src/views/RecipeDetailView.vue -->
<template>
  <div class="container mx-auto px-4 py-8 max-w-4xl">
    <button @click="$router.back()" class="mb-6 text-indigo-600 font-medium text-lg hover:underline">
      ← Back to Search
    </button>

    <div v-if="!recipe" class="text-center py-32 text-3xl text-gray-500">
      Recipe not found
    </div>

    <div v-else class="bg-white rounded-3xl shadow-2xl overflow-hidden">
      <img :src="recipe.image" class="w-full h-96 object-cover" alt="Recipe" />
      
      <div class="p-10">
        <div class="flex justify-between items-start mb-8">
          <div>
            <h1 class="text-5xl font-bold text-gray-800 mb-3">{{ recipe.title }}</h1>
            <p class="text-2xl text-gray-600">
              {{ recipe.cuisine }} • {{ recipe.cookTime }} min • Serves {{ servings }}
            </p>
          </div>
          <button @click="toggleSave" class="text-5xl hover:scale-110 transition">
            {{ recipe.isSaved ? '♥' : '♡' }}
          </button>
        </div>

        <!-- SERVING SCALER -->
        <div class="mb-10 p-6 bg-indigo-50 rounded-2xl inline-block">
          <ServingScaler v-model:servings="servings" :original-servings="originalServings" />
        </div>

        <h2 class="text-3xl font-bold mb-6 text-gray-800">Ingredients</h2>
        <ul class="space-y-4 text-lg bg-gray-50 p-6 rounded-2xl">
          <li v-for="ing in scaledIngredients" class="flex items-center">
            <span class="font-bold text-indigo-600 w-32">
              {{ ing.scaled }} {{ ing.unit || '' }}
            </span>
            <span class="text-gray-700">{{ ing.name }}</span>
          </li>
        </ul>

        <h2 class="text-3xl font-bold mt-12 mb-6 text-gray-800">Instructions</h2>
        <p class="text-lg text-gray-700 leading-relaxed whitespace-pre-line bg-gray-50 p-6 rounded-2xl">
          {{ recipe.instructions }}
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { mockRecipes } from '@/services/mockData.js'  // ← THIS LINE WAS MISSING
import ServingScaler from '@/components/ServingScaler.vue'

const route = useRoute()
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
    recipe.value.isSaved = !recipe.value.isSaved
  }
}
</script>