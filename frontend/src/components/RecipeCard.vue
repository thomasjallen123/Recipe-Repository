<!-- src/components/RecipeCard.vue -->
<template>
  <div 
    class="bg-white rounded-2xl shadow-lg overflow-hidden hover:shadow-2xl transition transform hover:-translate-y-2 cursor-pointer"
    @click="goToRecipe"
  >
    <div class="relative">
      <img :src="recipe.image" class="w-full h-64 object-cover" />
      <button
        @click.stop="toggleSave"
        class="absolute top-4 right-4 bg-white/90 p-3 rounded-full shadow-lg hover:scale-110 transition"
      >
        <span class="text-2xl">{{ recipe.isSaved ? '♥' : '♡' }}</span>
      </button>
    </div>
    <div class="p-6">
      <h3 class="font-bold text-xl text-gray-800">{{ recipe.title }}</h3>
      <p class="text-gray-600 mt-1">{{ recipe.cuisine }} • {{ recipe.cookTime }} min</p>
      <button class="mt-4 text-indigo-600 font-medium hover:underline">
        View Recipe →
      </button>
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