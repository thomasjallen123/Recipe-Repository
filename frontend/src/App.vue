<!-- src/App.vue — VIBRANT GRADIENT + PARALLAX TEXTURE -->
<template>
  <div class="min-h-screen relative overflow-x-hidden">
    <!-- VIBRANT BACKGROUND: CORAL-TO-ORANGE GRADIENT + PARALLAX LAYERS -->
    <div 
      class="fixed inset-0 -z-50 bg-gradient-to-br from-orange-400/20 via-red-400/20 to-yellow-500/20"
      style="
        background: linear-gradient(to bottom right, #FF6B35 0%, #F7931E 50%, #FDCB6E 100%) !important;
        transform: translateZ(0); /* Enable hardware accel */
      "
    ></div>
    <!-- ANIMATED FLOATING ORBS FOR DEPTH (PARALLAX) -->
    <div class="fixed inset-0 -z-40 pointer-events-none overflow-hidden">
      <div class="absolute top-20 left-10 w-64 h-64 bg-teal-400/20 rounded-full blur-3xl animate-float slow"></div>
      <div class="absolute bottom-20 right-10 w-96 h-96 bg-lime-400/20 rounded-full blur-3xl animate-float fast"></div>
      <div class="absolute top-1/2 left-1/2 w-48 h-48 bg-red-400/10 rounded-full blur-2xl animate-float medium delay-1"></div>
    </div>

    <!-- MAIN CONTENT -->
    <router-view class="relative z-10" />
  </div>
</template>

<script setup>
// UNCHANGED
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@100..900&display=swap');
* {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

a, a:hover, a:visited, a:active {
  color: inherit !important;
  text-decoration: none !important;
}

html {
  scroll-behavior: smooth;
}

/* ADVANCED ANIMATIONS: FLOAT, TYPEWRITER, BOUNCE */
.animate-float {
  animation: float 6s ease-in-out infinite;
}
@keyframes float {
  0%, 100% { transform: translateY(0px) rotate(0deg); }
  50% { transform: translateY(-20px) rotate(5deg); }
}
.animate-float.slow { animation-duration: 8s; }
.animate-float.fast { animation-duration: 4s; }
.animate-float.medium { animation-duration: 6s; }
.animate-float.delay-1 { animation-delay: 1s; }

.typewriter {
  overflow: hidden;
  border-right: 3px solid #00D4AA;
  white-space: nowrap;
  animation: typing 3s steps(40, end), blink-caret 0.75s step-end infinite;
}
@keyframes typing {
  from { width: 0; }
  to { width: 100%; }
}
@keyframes blink-caret {
  from, to { border-color: transparent; }
  50% { border-color: #00D4AA; }
}

.bounce-hover {
  transition: all 0.3s cubic-bezier(0.68, -0.55, 0.265, 1.55);
}
.bounce-hover:hover {
  transform: scale(1.05) translateY(-2px);
  animation: bounce 0.6s ease;
}
@keyframes bounce {
  0%, 20%, 50%, 80%, 100% { transform: translateY(0); }
  40% { transform: translateY(-10px); }
  60% { transform: translateY(-5px); }
}

/* PAGE FADE-IN */
.animate-pageIn {
  animation: pageIn 1s ease-out;
}
@keyframes pageIn {
  from { opacity: 0; transform: scale(0.95); }
  to { opacity: 1; transform: scale(1); }
}
</style>