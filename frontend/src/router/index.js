/**
 * Router de Vue - Configuración de Rutas
 * ======================================
 * 
 * Este módulo configura Vue Router para la navegación de la aplicación:
 * - Definición de todas las rutas disponibles
 * - Guards de autenticación para rutas protegidas
 * - Lazy loading de componentes para mejor rendimiento
 * - Manejo de redirecciones automáticas
 * 
 * Estructura de rutas:
 * - / (Home): Página pública principal
 * - /login: Página de autenticación
 * - /categorias: CRUD de categorías (protegida)
 * - /presentaciones: CRUD de presentaciones (protegida)
 * - /productos: CRUD de productos (protegida)
 */

import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../store/auth'

// Importar componentes de vistas (lazy loading para mejor rendimiento)
const HomeView = () => import('../views/HomeView.vue')
const LoginView = () => import('../views/LoginView.vue')
const CategoriaView = () => import('../views/CategoriaView.vue')
const PresentacionView = () => import('../views/PresentacionView.vue')
const ProductoView = () => import('../views/ProductoView.vue')

// Definir las rutas de la aplicación
const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView,
    meta: {
      title: 'Inicio - Catálogo de Productos',
      requiresAuth: false // Ruta pública
    }
  },
  {
    path: '/login',
    name: 'login',
    component: LoginView,
    meta: {
      title: 'Iniciar Sesión',
      requiresAuth: false // Ruta pública
    }
  },
  {
    path: '/categorias',
    name: 'categorias',
    component: CategoriaView,
    meta: {
      title: 'Categorías - Administración',
      requiresAuth: true // Ruta protegida
    }
  },
  {
    path: '/presentaciones',
    name: 'presentaciones',
    component: PresentacionView,
    meta: {
      title: 'Presentaciones - Administración',
      requiresAuth: true // Ruta protegida
    }
  },
  {
    path: '/productos',
    name: 'productos',
    component: ProductoView,
    meta: {
      title: 'Productos - Administración',
      requiresAuth: true // Ruta protegida
    }
  },
  {
    // Ruta para manejar URLs no encontradas
    path: '/:pathMatch(.*)*',
    redirect: '/'
  }
]

// Crear instancia del router
const router = createRouter({
  // Usar history mode para URLs limpias (sin #)
  history: createWebHistory(process.env.BASE_URL),
  routes
})

// Guard global para proteger rutas que requieren autenticación
router.beforeEach(async (to, from, next) => {
  // Obtener el store de autenticación
  const authStore = useAuthStore()
  
  // Inicializar autenticación si no se ha hecho
  authStore.initializeAuth()
  
  // Verificar si la ruta requiere autenticación
  if (to.meta.requiresAuth) {
    // Verificar si el usuario está autenticado
    const isAuthenticated = await authStore.ensureAuthenticated()
    
    if (!isAuthenticated) {
      // Si no está autenticado, redirigir al login
      next({ name: 'login' })
      return
    }
  }
  
  // Si el usuario está en login y ya está autenticado, redirigir al home
  if (to.name === 'login' && authStore.isAuthenticated) {
    next({ name: 'home' })
    return
  }
  
  // Actualizar el título de la página
  if (to.meta.title) {
    document.title = to.meta.title
  }
  
  // Continuar con la navegación
  next()
})

// Exportar la instancia del router
export default router
