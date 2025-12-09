<!-- src/components/RecipeCard.vue — FINAL: CUISINE ALWAYS TITLE CASE -->
<template>
  <div
    class="group/card bg-gradient-to-br from-yellow-50/80 to-orange-50/80 rounded-3xl shadow-2xl overflow-hidden hover:shadow-red-500/30 transition-all duration-700 cursor-pointer border border-teal-200/50 backdrop-blur-md animate-stagger float-in"
    :style="{ '--delay': `${index * 0.1}s` }"
    @click="goToRecipe"
  >
    <div class="relative">
      <img
        :src="recipe.image_url || recipe.image || 'https://via.placeholder.com/400x300?text=No+Image'"
        class="w-full h-64 object-cover transition-transform duration-700 group-hover/card:scale-110"
        alt="Recipe"
      />

      <!-- HEART BUTTON -->
      <button
        @click.stop="toggleSave"
        class="absolute top-4 right-4 bg-white/90 p-3 rounded-full shadow-2xl hover:scale-125 transition-all duration-300 backdrop-blur-sm border border-red-200/50 hover:shadow-red-500/50"
      >
        <svg v-if="isSaved" class="text-red-500 w-6 h-6 animate-pulse" fill="currentColor" viewBox="0 0 24 24">
          <path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z"/>
        </svg>
        <svg v-else class="text-teal-500 w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="2">
          <path stroke-linecap="round" stroke-linejoin="round" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"/>
        </svg>
      </button>
    </div>

    <div class="p-6">
      <h3 class="font-black text-2xl leading-tight text-orange-900 mb-3 group-hover/card:text-red-600 transition-all duration-300">
        {{ recipe.title }}
      </h3>
      <p class="text-teal-700 font-semibold mb-4">
        {{ displayCuisine }} • {{ recipe.total_time_minutes || recipe.cook_time_minutes || '?' }} min
      </p>

      <!-- INSTRUCTIONS PREVIEW -->
      <div class="mt-4 text-sm text-orange-800 leading-relaxed space-y-1 border-t border-orange-200 pt-4">
        <template v-for="(step, i) in previewInstructions" :key="i">
          <div class="flex">
            <span class="text-red-500 font-bold mr-2">{{ i + 1 }}.</span>
            <span class="line-clamp-2">{{ step }}</span>
          </div>
        </template>
        <div v-if="totalInstructions > 3" class="text-orange-600 italic text-xs pt-1">
          …and {{ totalInstructions - 3 }} more steps — tap to view full recipe
        </div>
      </div>

      <div class="mt-4 text-teal-600 font-bold text-lg group-hover/card:underline group-hover/card:text-lime-600 transition-all">
        View Recipe
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { useRecipeStore } from '@/stores/recipes'

const router = useRouter()
const recipeStore = useRecipeStore()

const props = defineProps({
  recipe: { type: Object, required: true },
  index: { type: Number, default: 0 }
})

// PERFECT TITLE CASE CUISINE — NO MORE lowercase
const displayCuisine = computed(() => {
  if (!props.recipe.cuisine) return 'Cuisine'
  return props.recipe.cuisine
    .toLowerCase()
    .split(' ')
    .map(word => word.charAt(0).toUpperCase() + word.slice(1))
    .join(' ')
})

// First 3 steps
const previewInstructions = computed(() => {
  const inst = props.recipe.instructions || []
  return inst
    .map(i => (i.step_text || i.text || '').trim())
    .filter(t => t)
    .slice(0, 3)
})

// Count total steps for "and X more"
const totalInstructions = computed(() => {
  const inst = props.recipe.instructions || []
  return inst
    .map(i => (i.step_text || i.text || '').trim())
    .filter(t => t).length
})

const isSaved = computed(() => recipeStore.savedRecipeIds.includes(props.recipe.id))

const goToRecipe = () => router.push(`/recipe/${props.recipe.id}`)
const toggleSave = () => recipeStore.toggleSave(props.recipe)
</script>

<style scoped>
.float-in {
  opacity: 0;
  transform: translateY(50px) rotate(-5deg);
  animation: floatIn 0.8s cubic-bezier(0.25, 0.46, 0.45, 0.94) forwards;
}
@keyframes floatIn {
  to { opacity: 1; transform: translateY(0) rotate(0deg); }
}
.animate-stagger { animation-delay: var(--delay, 0s); }
</style>