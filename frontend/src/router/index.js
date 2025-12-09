// src/router/index.js
import { createRouter, createWebHistory } from 'vue-router'

const HomeView = () => import('@/views/HomeView.vue')
const LoginView = () => import('@/views/LoginView.vue')
const RegisterView = () => import('@/views/RegisterView.vue')
const SearchView = () => import('@/views/SearchView.vue')
const RecipeDetailView = () => import('@/views/RecipeDetailView.vue')
const CollectionView = () => import('@/views/CollectionView.vue')

const routes = [
  { path: '/', name: 'Home', component: HomeView },
  { path: '/login', name: 'Login', component: LoginView },
  { path: '/register', name: 'Register', component: RegisterView },
  { path: '/search', name: 'Search', component: SearchView },
  { path: '/recipe/:id', name: 'RecipeDetail', component: RecipeDetailView },
  { path: '/collection', name: 'Collection', component: CollectionView },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router