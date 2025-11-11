<template>
  <div class="min-h-screen container mx-auto px-4 py-12 relative z-10 animate-pageIn">
    <button @click="$router.back()" class="mb-8 inline-flex items-center bg-gradient-to-r from-teal-500 to-lime-500 text-white font-semibold text-xl hover:from-teal-600 hover:to-lime-600 transition-all px-6 py-3 rounded-xl shadow-lg bounce-hover">
      ← Back to Search
    </button>

    <div v-if="!recipe" class="text-center py-32 text-3xl text-orange-800 font-semibold">
      Recipe not found
    </div>

    <div v-else class="bg-gradient-to-br from-yellow-50/95 to-orange-50/95 backdrop-blur-md rounded-3xl shadow-2xl overflow-hidden border border-teal-200/50 animate-slideIn">
      <img :src="recipe.image" class="w-full h-96 object-cover transition-transform duration-700 hover:scale-105" alt="Recipe" />

      <div class="p-12">
        <div class="flex justify-between items-start mb-10">
          <div class="flex-1">
            <h1 class="text-6xl font-black bg-gradient-to-r from-orange-800 to-red-600 bg-clip-text text-transparent mb-4 leading-tight typewriter">{{ recipe.title }}</h1>
            <p class="text-2xl text-teal-700 font-semibold animate-slideIn delay-1">
              {{ recipe.cuisine }} • {{ recipe.cookTime }} min • Serves {{ servings }}
            </p>
          </div>

          <button @click="toggleSave" class="hover:scale-110 transition-transform p-3 rounded-full bg-gradient-to-r from-red-500/20 to-yellow-500/20 shadow-lg border border-red-200/50 animate-pulse">
            <svg v-if="recipe.isSaved" style="width: 48px; height: 48px;" class="text-red-500" fill="currentColor" viewBox="0 0 24 24">
              <path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z"/>
            </svg>
            <svg v-else style="width: 48px; height: 48px;" class="text-teal-500" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"/>
            </svg>
          </button>
        </div>

        <div class="mb-12 p-8 bg-gradient-to-r from-teal-50/80 to-lime-50/80 rounded-3xl border border-teal-200/50 shadow-inner animate-slideIn delay-2">
          <ServingScaler v-model:servings="servings" :original-servings="originalServings" />
        </div>

        <h2 class="text-4xl font-black mb-8 bg-gradient-to-r from-teal-600 to-lime-600 bg-clip-text text-transparent animate-slideIn delay-3">Ingredients</h2>
        <ul class="space-y-4 text-lg bg-teal-50/60 p-8 rounded-3xl border border-teal-200/50 animate-cascade">
          <li v-for="(ing, idx) in scaledIngredients" :key="ing.name" class="flex items-center py-3 px-4 rounded-2xl bg-white/50 hover:bg-lime-100/50 transition-all animate-slideIn" :style="{ animationDelay: `${idx * 0.1}s` }">
            <span class="font-bold text-teal-600 w-32 text-xl">{{ ing.scaled }} {{ ing.unit || '' }}</span>
            <span class="text-orange-800 font-semibold flex-1">{{ ing.name }}</span>
          </li>
        </ul>

        <h2 class="text-4xl font-black mt-16 mb-8 bg-gradient-to-r from-teal-600 to-lime-600 bg-clip-text text-transparent animate-slideIn delay-4">Instructions</h2>
        <div class="text-lg text-orange-800 leading-relaxed whitespace-pre-line bg-teal-50/60 p-8 rounded-3xl border border-teal-200/50 animate-typewriter">
          <div class="space-y-6">
            <p v-for="(step, index) in recipe.instructions.split('\n\n')" :key="index" class="py-4 px-6 bg-white/50 rounded-2xl shadow-sm animate-slideIn" :style="{ animationDelay: `${(index + 5) * 0.2}s` }">{{ step }}</p>
          </div>
        </div>
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

<style scoped>
.animate-cascade {
  --cascade-delay: 0s;
}
.delay-1 { animation-delay: 0.2s; }
.delay-2 { animation-delay: 0.4s; }
.delay-3 { animation-delay: 0.6s; }
.delay-4 { animation-delay: 0.8s; }
.animate-typewriter {
  overflow: hidden;
  animation: typewriter-scroll 2s steps(40, end) forwards;
}
@keyframes typewriter-scroll {
  from { max-height: 0; }
  to { max-height: 100vh; }
}
</style>

