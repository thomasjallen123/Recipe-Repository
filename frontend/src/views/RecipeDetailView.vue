<!-- src/views/RecipeDetailView.vue -->
<template>
  <main class="min-h-screen bg-gradient-to-br from-teal-50 to-lime-50 p-6">
    <button @click="$router.back()" class="mb-6 inline-flex items-center gap-2 text-teal-700 font-bold hover:text-teal-900 transition">
      ← Back to Search
    </button>

    <div v-if="loading" class="max-w-4xl mx-auto space-y-6">
      <div class="bg-white/80 backdrop-blur p-8 rounded-2xl shadow animate-pulse">
        <div class="h-10 bg-gray-300 rounded w-3/4 mb-4"></div>
        <div class="h-6 bg-gray-300 rounded w-1/2"></div>
      </div>
    </div>

    <div v-else-if="error" class="text-center py-20">
      <h2 class="text-3xl font-black text-red-600 mb-4">Recipe Not Found</h2>
      <p class="text-lg text-gray-700 mb-6">{{ error }}</p>
      <button @click="fetchRecipe" class="px-8 py-3 bg-red-600 text-white rounded-xl hover:bg-red-700 transition font-bold">
        Try Again
      </button>
    </div>

    <article v-else class="max-w-4xl mx-auto bg-white/90 backdrop-blur-md p-8 rounded-3xl shadow-2xl">
      <header class="mb-8">
        <h1 class="text-5xl font-black text-teal-700 mb-4 leading-tight">{{ recipe.title }}</h1>
        <p class="text-xl text-gray-700">{{ recipe.cuisine }} • {{ recipe.cookTime }} min • Serves {{ servings }}</p>
      </header>

      <!-- Serving Scaler -->
      <div class="mb-12 p-6 bg-teal-50 rounded-2xl border border-teal-200">
        <label class="block font-bold text-teal-700 mb-3">Servings:</label>
        <div class="flex items-center gap-4">
          <button @click="servings--" :disabled="servings <= 1" class="w-10 h-10 bg-teal-600 text-white rounded-full font-bold hover:bg-teal-700 disabled:opacity-50">−</button>
          <input v-model.number="servings" type="number" min="1" max="20" class="w-20 px-3 py-2 text-center text-xl font-bold border-2 border-teal-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-teal-400" />
          <button @click="servings++" class="w-10 h-10 bg-teal-600 text-white rounded-full font-bold hover:bg-teal-700">+</button>
          <span class="ml-4 text-lg font-semibold text-teal-600">({{ scaleFactor.toFixed(1) }}x)</span>
        </div>
      </div>

      <!-- Ingredients -->
      <section class="mb-12">
        <h2 class="text-3xl font-black text-teal-700 mb-6">Ingredients</h2>
        <ul class="space-y-3">
          <li v-for="ing in scaledIngredients" :key="ing.name" class="flex justify-between items-center bg-teal-50/70 p-4 rounded-xl">
            <span class="font-bold text-teal-700">{{ ing.scaled }} {{ ing.unit || '' }}</span>
            <span class="text-gray-800 font-medium">{{ ing.name }}</span>
          </li>
        </ul>
      </section>

      <!-- Instructions -->
      <section>
        <h2 class="text-3xl font-black text-teal-700 mb-6">Instructions</h2>
        <div class="prose prose-lg max-w-none text-gray-800 whitespace-pre-line">
          {{ recipe.instructions }}
        </div>
      </section>
    </article>
  </main>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { formatQuantity } from '@/services/formatQuantity'

const route = useRoute()
const recipe = ref(null)
const servings = ref(4)
const originalServings = ref(4)
const loading = ref(true)
const error = ref(null)

// ALL 3 RECIPES
const mockRecipes = {
  1: {
    id: 1,
    title: "Spicy Chicken Curry",
    cuisine: "Indian",
    cookTime: 45,
    servings: 4,
    ingredients: [
      { name: "chicken", quantity: 500, unit: "g" },
      { name: "curry powder", quantity: 2, unit: "tbsp" },
      { name: "coconut milk", quantity: 400, unit: "ml" },
      { name: "onion", quantity: 1 },
    ],
    instructions: "1. Brown chicken.\n2. Add onion and curry.\n3. Pour in coconut milk.\n4. Simmer 30 min.\n5. Serve with rice."
  },
  2: {
    id: 2,
    title: "Beef Tacos",
    cuisine: "Mexican",
    cookTime: 20,
    servings: 4,
    ingredients: [
      { name: "ground beef", quantity: 400, unit: "g" },
      { name: "taco shells", quantity: 8 },
      { name: "lettuce", quantity: 1, unit: "cup" },
      { name: "cheese", quantity: 100, unit: "g" },
    ],
    instructions: "1. Cook beef with spices.\n2. Warm shells.\n3. Fill with beef, lettuce, cheese.\n4. Add salsa."
  },
  3: {
    id: 3,
    title: "Pasta Carbonara",
    cuisine: "Italian",
    cookTime: 25,
    servings: 4,
    ingredients: [
      { name: "spaghetti", quantity: 400, unit: "g" },
      { name: "eggs", quantity: 4 },
      { name: "pancetta", quantity: 200, unit: "g" },
      { name: "parmesan", quantity: 100, unit: "g" },
    ],
    instructions: "1. Boil pasta.\n2. Fry pancetta.\n3. Mix eggs + cheese.\n4. Toss off heat.\n5. Serve hot."
  }
}

const fetchRecipe = async () => {
  loading.value = true
  error.value = null
  try {
    await new Promise(r => setTimeout(r, 400))
    const id = parseInt(route.params.id)
    const data = mockRecipes[id]
    if (!data) throw new Error("Recipe not found")
    recipe.value = data
    originalServings.value = data.servings
    servings.value = originalServings.value
  } catch (err) {
    error.value = err.message
  } finally {
    loading.value = false
  }
}

const scaleFactor = computed(() => servings.value / originalServings.value)
const scaledIngredients = computed(() => {
  if (!recipe.value) return []
  return recipe.value.ingredients.map(ing => ({
    ...ing,
    scaled: formatQuantity(ing.quantity * scaleFactor.value)
  }))
})

onMounted(fetchRecipe)
</script>

