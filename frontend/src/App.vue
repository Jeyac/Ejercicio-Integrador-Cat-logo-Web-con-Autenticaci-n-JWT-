<!--
  Componente Principal de la Aplicación
  =====================================
  
  Este es el componente raíz de la aplicación Vue.js que:
  - Define la estructura general de la aplicación
  - Incluye el componente Navbar para navegación
  - Configura el contenedor principal para las vistas
  - Maneja las transiciones entre páginas
  - Inicializa la autenticación al cargar la aplicación
  
  Características:
  - Layout responsive con Bootstrap
  - Transiciones suaves entre páginas
  - Inicialización automática del estado de autenticación
  - Estructura consistente para todas las vistas
-->

<template>
  <div id="app">
    <!-- Barra de navegación principal -->
    <Navbar />
    
    <!-- Contenedor principal para el contenido de las páginas -->
    <div class="main-content">
      <div class="container-fluid">
        <!-- Router view con transiciones -->
        <router-view v-slot="{ Component }">
          <transition name="page" mode="out-in">
            <component :is="Component" />
          </transition>
        </router-view>
      </div>
    </div>
  </div>
</template>

<script>
import { onMounted } from 'vue'
import Navbar from './components/Navbar.vue'
import { useAuthStore } from './store/auth'

export default {
  name: 'App',
  
  // Componentes utilizados en este componente
  components: {
    Navbar
  },
  
  // Configuración del componente usando Composition API
  setup() {
    // Obtener el store de autenticación
    const authStore = useAuthStore()
    
    // Hook que se ejecuta cuando el componente se monta
    onMounted(() => {
      // Inicializar el estado de autenticación al cargar la aplicación
      authStore.initializeAuth()
    })
  }
}
</script>

<style>
/* Estilos globales de la aplicación */

/* Configuración base del body */
body {
  margin: 0;
  padding: 0;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  min-height: 100vh;
}

/* Contenedor principal de la aplicación */
#app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

/* Contenedor del contenido principal */
.main-content {
  flex: 1;
  padding-top: 20px;
  padding-bottom: 20px;
}

/* Transiciones entre páginas */
.page-enter-active,
.page-leave-active {
  transition: all 0.3s ease;
}

.page-enter-from {
  opacity: 0;
  transform: translateX(30px);
}

.page-leave-to {
  opacity: 0;
  transform: translateX(-30px);
}

/* Estilos para el spinner de carga */
.loading-spinner {
  display: inline-block;
  width: 16px;
  height: 16px;
  border: 2px solid #ffffff;
  border-radius: 50%;
  border-top-color: transparent;
  animation: spin 1s ease-in-out infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

/* Estilos para botones modernos */
.btn-modern {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border: none;
  border-radius: 12px;
  padding: 12px 24px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
}

.btn-modern:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
  background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
}

/* Estilos para tarjetas modernas */
.card-modern {
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.95), rgba(255, 255, 255, 0.9));
  backdrop-filter: blur(10px);
  border-radius: 16px;
  border: 1px solid rgba(255, 255, 255, 0.2);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  transition: all 0.3s ease;
}

.card-modern:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.12);
}

/* Responsive design */
@media (max-width: 768px) {
  .main-content {
    padding-top: 10px;
    padding-bottom: 10px;
  }
  
  .btn-modern {
    padding: 10px 20px;
    font-size: 0.9rem;
  }
}
</style>
