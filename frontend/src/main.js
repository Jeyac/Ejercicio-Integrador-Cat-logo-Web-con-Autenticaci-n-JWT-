/**
 * Punto de entrada principal de la aplicación Vue.js
 * ================================================
 * 
 * Este archivo inicializa y configura la aplicación Vue.js con:
 * - Pinia para manejo de estado (autenticación, datos globales)
 * - Vue Router para navegación entre páginas
 * - Bootstrap 5 para estilos y componentes UI
 * - Bootstrap Icons para iconografía
 * 
 * Arquitectura del Frontend:
 * - Components: Componentes reutilizables (Navbar, CrudTable, CrudForm)
 * - Views: Páginas principales (Home, Login, CRUD de entidades)
 * - Store: Manejo de estado con Pinia (auth, datos)
 * - API: Cliente HTTP con Axios para comunicación con backend
 * - Router: Configuración de rutas y guards de autenticación
 */

import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'

// Importar Bootstrap CSS y JS para estilos y funcionalidad
import 'bootstrap/dist/css/bootstrap.min.css'
import 'bootstrap-icons/font/bootstrap-icons.css'
import * as bootstrap from 'bootstrap/dist/js/bootstrap.bundle.min.js'

// Hacer Bootstrap disponible globalmente para usar en componentes
// Esto permite usar new bootstrap.Modal() en cualquier parte de la app
window.bootstrap = bootstrap

// Crear instancia de la aplicación Vue
const app = createApp(App)

// Configurar Pinia para manejo de estado
const pinia = createPinia()
app.use(pinia)

// Configurar Vue Router para navegación
app.use(router)

// Montar la aplicación en el elemento #app del DOM
app.mount('#app')
