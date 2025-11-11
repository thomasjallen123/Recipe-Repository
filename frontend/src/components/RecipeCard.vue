<!-- src/components/RecipeCard.vue -->
<template>
  <div
    class="bg-white dark:bg-gray-800 rounded-3xl shadow-xl overflow-hidden hover:shadow-2xl hover:scale-105 transition-all duration-500 cursor-pointer group"
    @click="goToRecipe"
  >
    <div class="relative">
      <img :src="recipe.image" class="w-full h-64 object-cover" alt="Recipe" />

      <!-- HEART BUTTON — FIXED: inline style -->
      <button
        @click.stop="toggleSave"
        class="absolute top-4 right-4 bg-white/90 dark:bg-gray-900/90 p-3 rounded-full shadow-2xl hover:scale-125 transition-all duration-300 backdrop-blur-sm"
      >
        <!-- FILLED HEART -->
        <svg
          v-if="recipe.isSaved"
          style="width: 24px; height: 24px;"
          class="text-red-600"
          fill="currentColor"
          viewBox="0 0 24 24"
        >
          <path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z"/>
        </svg>

        <!-- EMPTY HEART -->
        <svg
          v-else
          style="width: 24px; height: 24px;"
          class="text-gray-400"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
          stroke-width="2"
        >
          <path stroke-linecap="round" stroke-linejoin="round" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"/>
        </svg>
      </button>
    </div>

    <div class="p-6">
      <h3 class="font-bold text-2xl text-gray-800 dark:text-white">{{ recipe.title }}</h3>
      <p class="text-gray-600 dark:text-gray-400 mt-2">{{ recipe.cuisine }} • {{ recipe.cookTime }} min</p>
      <div class="mt-4 text-indigo-600 dark:text-indigo-400 font-bold group-hover:underline">
        View Recipe
      </div>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
const router = useRouter()
const props = defineProps(['recipe'])
const emit = defineEmits(['toggle-save'])

const goToRecipe = () => {
  router.push(`/recipe/${props.recipe.id}`)
}

const toggleSave = () => {
  emit('toggle-save', props.recipe)
}
</script>