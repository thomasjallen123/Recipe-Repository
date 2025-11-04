<template>
  <div class="container mx-auto px-4 py-8">
    <h1 class="text-3xl font-bold text-indigo-600 mb-6">Search Recipes</h1>

    <div class="bg-white p-6 rounded-lg shadow mb-6">
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
        <input
          v-model="ingredient"
          @keyup.enter="search"
          placeholder="Search by ingredient..."
          class="px-4 py-2 border rounded-lg focus:ring-2 focus:ring-indigo-500"
        />
        <select v-model="cuisine" class="px-4 py-2 border rounded-lg">
          <option value="">All Cuisines</option>
          <option>Italian</option>
          <option>Mexican</option>
          <option>Chinese</option>
        </select>
        <div class="flex gap-2">
          <input
            v-model.number="maxTime"
            type="number"
            placeholder="Max min"
            class="w-full px-4 py-2 border rounded-lg"
          />
          <button
            @click="search"
            class="px-6 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700"
          >
            Search
          </button>
        </div>
      </div>
    </div>

    <div v-if="recipes.length === 0" class="text-center text-gray-500 py-10">
      No recipes found. Try searching!
    </div>

    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <div
        v-for="recipe in recipes"
        :key="recipe.id"
        class="bg-white p-4 rounded-lg shadow hover:shadow-md transition"
      >
        <h3 class="font-semibold text-lg">{{ recipe.title }}</h3>
        <p class="text-sm text-gray-600">
          {{ recipe.cuisine }} • {{ recipe.cookTime }} min
        </p>
        <button class="mt-2 text-indigo-600 text-sm hover:underline">
          View Recipe →
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const ingredient = ref('')
const cuisine = ref('')
const maxTime = ref('')
const recipes = ref([])

const search = () => {
  // Mock data
  recipes.value = [
    {
      id: 1,
      title: 'Spaghetti Carbonara',
      cuisine: 'Italian',
      cookTime: 20
    }
  ]
}
</script>