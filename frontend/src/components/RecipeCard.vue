<!-- src/components/RecipeCard.vue — VIBRANT CARDS + STAGGER FLOAT-IN -->
<template>
  <div
    class="group/card bg-gradient-to-br from-yellow-50/80 to-orange-50/80 rounded-3xl shadow-2xl overflow-hidden hover:shadow-red-500/30 transition-all duration-700 cursor-pointer border border-teal-200/50 backdrop-blur-md animate-stagger float-in"
    :style="{ '--delay': `${index * 0.1}s` }"
    @click="goToRecipe"
  >
    <div class="relative">
      <img :src="recipe.image" class="w-full h-64 object-cover transition-transform duration-700 group-hover/card:scale-110" alt="Recipe" />

      <!-- HEART BUTTON — VIBRANT RED GLOW -->
      <button
        @click.stop="toggleSave"
        class="absolute top-4 right-4 bg-white/90 p-3 rounded-full shadow-2xl hover:scale-125 transition-all duration-300 backdrop-blur-sm border border-red-200/50 hover:shadow-red-500/50"
      >
        <!-- FILLED HEART — BERRY RED -->
        <svg
          v-if="recipe.isSaved"
          style="width: 24px; height: 24px;"
          class="text-red-500 animate-pulse"
          fill="currentColor"
          viewBox="0 0 24 24"
        >
          <path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z"/>
        </svg>

        <!-- EMPTY HEART — TEAL STROKE -->
        <svg
          v-else
          style="width: 24px; height: 24px;"
          class="text-teal-500"
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
      <h3 class="font-black text-2xl leading-tight text-orange-900 mb-3 group-hover/card:text-red-600 transition-all duration-300">{{ recipe.title }}</h3>
      <p class="text-teal-700 font-semibold mb-4">{{ recipe.cuisine }} • {{ recipe.cookTime }} min</p>
      <div class="mt-4 text-teal-600 font-bold text-lg group-hover/card:underline group-hover/card:text-lime-600 transition-all">
        View Recipe →
      </div>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
const router = useRouter()
const props = defineProps(['recipe', 'index']) // Added index for stagger
const emit = defineEmits(['toggle-save'])

const goToRecipe = () => {
  router.push(`/recipe/${props.recipe.id}`)
}

const toggleSave = () => {
  emit('toggle-save', props.recipe)
}
</script>

<style scoped>
/* STAGGERED FLOAT-IN */
.float-in {
  opacity: 0;
  transform: translateY(50px) rotate(-5deg);
  animation: floatIn 0.8s cubic-bezier(0.25, 0.46, 0.45, 0.94) forwards;
}
@keyframes floatIn {
  to {
    opacity: 1;
    transform: translateY(0) rotate(0deg);
  }
}
.animate-stagger {
  animation-delay: var(--delay, 0s);
}
</style>