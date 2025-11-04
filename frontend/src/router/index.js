import { createRouter, createWebHistory } from 'vue-router'

// Lazy-load views (only download when visited)
const HomeView = () => import('../views/HomeView.vue')
const LoginView = () => import('../views/LoginView.vue')
const RegisterView = () => import('../views/RegisterView.vue')
const SearchView = () => import('../views/SearchView.vue')
const CollectionView = () => import('../views/CollectionView.vue')

const routes = [
  { path: '/', name: 'Home', component: HomeView },
  { path: '/login', name: 'Login', component: LoginView },
  { path: '/register', name: 'Register', component: RegisterView },
  { path: '/search', name: 'Search', component: SearchView },
  { path: '/collection', name: 'Collection', component: CollectionView }
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior() {
    return { top: 0 }
  }
})

export default router