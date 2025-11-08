// src/main.js
import { createApp } from 'vue'
import { createPinia } from 'pinia'  // ← THIS WAS MISSING
import App from './App.vue'
import router from './router'
import './index.css'

const app = createApp(App)
const pinia = createPinia()  // ← CREATE PINIA

app.use(pinia)   // ← USE IT
app.use(router)
app.mount('#app')