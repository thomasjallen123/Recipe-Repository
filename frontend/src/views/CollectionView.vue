<template>
  <div class="container mx-auto px-4 py-8">
    <h1 class="text-3xl font-bold text-indigo-600 mb-6">My Collection</h1>

    <div v-if="collection.length === 0" class="text-center py-10 text-gray-500">
      Your collection is empty. Start saving recipes!
      <router-link to="/search" class="text-indigo-600 hover:underline ml-1">
        Go to Search
      </router-link>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <div
        v-for="recipe in collection"
        :key="recipe.id"
        class="bg-white p-4 rounded-lg shadow"
      >
        <h3 class="font-semibold text-lg">{{ recipe.title }}</h3>
        <p class="text-sm text-gray-600">{{ recipe.cuisine }}</p>
        <button class="mt-2 text-red-600 text-sm hover:underline">
          Remove
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const collection = ref([])
</script>