<!-- src/components/ServingScaler.vue — VIBRANT GRADIENT + BOUNCE BUTTONS -->
<template>
  <div class="flex items-center gap-4 bg-gradient-to-r from-teal-50/80 to-lime-50/80 p-6 rounded-3xl shadow-xl border border-teal-200/50 backdrop-blur-sm">
    <span class="font-black text-xl text-teal-700">Servings:</span>
    
    <button 
      @click="servings--"
      :disabled="servings <= 1"
      class="w-12 h-12 rounded-full bg-gradient-to-r from-teal-500 to-lime-500 text-white font-bold shadow-lg hover:shadow-teal-500/50 bounce-hover disabled:opacity-50 disabled:cursor-not-allowed disabled:shadow-none transition-all"
    >
      −
    </button>

    <input 
      v-model.number="servings" 
      type="number" 
      min="1"
      class="w-24 px-4 py-3 text-center text-2xl font-black border-2 border-teal-300 rounded-xl focus:border-lime-500 focus:ring-4 focus:ring-lime-200/50 focus:outline-none shadow-inner transition-all bg-yellow-50/50"
    />

    <button 
      @click="servings++"
      class="w-12 h-12 rounded-full bg-gradient-to-r from-teal-500 to-lime-500 text-white font-bold shadow-lg hover:shadow-teal-500/50 bounce-hover transition-all"
    >
      +
    </button>

    <span class="text-xl font-semibold text-red-600">
      ({{ scaleFactor.toFixed(2) }}x)
    </span>
  </div>
</template>

<script setup>
import { computed } from 'vue'

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