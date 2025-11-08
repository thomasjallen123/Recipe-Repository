<!-- src/components/ServingScaler.vue -->
<template>
  <div class="flex items-center gap-4 bg-gradient-to-r from-indigo-50 to-purple-50 p-4 rounded-2xl shadow-md">
    <span class="font-bold text-indigo-700">Servings:</span>
    
    <button 
      @click="servings--"
      :disabled="servings <= 1"
      class="w-10 h-10 rounded-full bg-indigo-600 text-white font-bold hover:bg-indigo-700 disabled:opacity-50 disabled:cursor-not-allowed transition"
    >
      −
    </button>

    <input 
      v-model.number="servings" 
      type="number" 
      min="1"
      class="w-20 px-3 py-2 text-center text-xl font-bold border-2 border-indigo-300 rounded-lg focus:border-indigo-600 focus:outline-none"
    />

    <button 
      @click="servings++"
      class="w-10 h-10 rounded-full bg-indigo-600 text-white font-bold hover:bg-indigo-700 transition"
    >
      +
    </button>

    <span class="text-lg font-medium text-purple-700">
      ({{ scaleFactor.toFixed(2) }}x)
    </span>
  </div>
</template>

<script setup>
import { computed } from 'vue'

// THIS LINE WAS MISSING — THIS IS THE ENTIRE FIX
const props = defineProps({
  originalServings: {
    type: Number,
    required: true
  }
})

const servings = defineModel('servings', { 
  type: Number, 
  required: true 
})

const scaleFactor = computed(() => {
  return servings.value / props.originalServings
})
</script>

<style scoped>
input::-webkit-outer-spin-button,
input::-webkit-inner-spin-button {
  -webkit-appearance: none;
  margin: 0;
}
input[type=number] {
  -moz-appearance: textfield;
}
</style>