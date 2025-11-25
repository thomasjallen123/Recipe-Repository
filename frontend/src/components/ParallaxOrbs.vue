<!-- src/components/ParallaxOrbs.vue -->
<template>
  <div 
    class="fixed inset-0 -z-50 pointer-events-none overflow-hidden opacity-60"
    aria-hidden="true"
  >
    <div 
      v-for="orb in orbs" 
      :key="orb.id" 
      class="absolute rounded-full blur-3xl animate-float"
      :class="orb.classes" 
      :style="orb.style"
    ></div>
  </div>
</template>

<script setup>
const orbs = [
  { id: 1, classes: 'top-20 left-10 w-64 h-64 bg-teal-400/20 slow', style: { animationDelay: '0s' } },
  { id: 2, classes: 'bottom-20 right-10 w-96 h-96 bg-lime-400/20 fast', style: { animationDelay: '0.5s' } },
  { id: 3, classes: 'top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-48 h-48 bg-red-400/10 medium', style: { animationDelay: '1s' } }
]
</script>

<style scoped>
@keyframes float {
  0%, 100% { transform: translateY(0) rotate(0deg); }
  50% { transform: translateY(-20px) rotate(5deg); }
}
.animate-float { animation: float 6s ease-in-out infinite; }
.slow { animation-duration: 8s; }
.fast { animation-duration: 4s; }
.medium { animation-duration: 6s; }
</style>