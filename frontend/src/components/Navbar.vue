<!--
  Componente Navbar - Barra de Navegación
  =======================================
  
  Este componente proporciona la navegación principal de la aplicación:
  - Logo y título de la aplicación
  - Menú de navegación con enlaces a las diferentes secciones
  - Menú desplegable para administración (cuando está autenticado)
  - Información del usuario autenticado
  - Botón de cerrar sesión
  
  Características:
  - Responsive design con Bootstrap
  - Menú colapsable en dispositivos móviles
  - Indicadores visuales de autenticación
  - Navegación dinámica basada en el estado de autenticación
-->

<template>
  <nav class="navbar navbar-expand-lg navbar-dark bg-gradient">
    <div class="container-fluid">
      <!-- Logo y título de la aplicación -->
      <router-link class="navbar-brand d-flex align-items-center" to="/">
        <i class="bi bi-shop me-2 brand-icon"></i>
        <span class="brand-text">Catálogo de Productos</span>
      </router-link>

      <!-- Botón para colapsar el menú en dispositivos móviles -->
      <button 
        class="navbar-toggler" 
        type="button" 
        data-bs-toggle="collapse" 
        data-bs-target="#navbarNav"
        aria-controls="navbarNav" 
        aria-expanded="false" 
        aria-label="Toggle navigation"
      >
        <span class="navbar-toggler-icon"></span>
      </button>

      <!-- Contenido del menú de navegación -->
      <div class="collapse navbar-collapse" id="navbarNav">
        <ul class="navbar-nav me-auto">
          <!-- Enlace al home -->
          <li class="nav-item">
            <router-link class="nav-link" to="/">
              <i class="bi bi-house me-1"></i>Inicio
            </router-link>
          </li>
        </ul>

        <!-- Menú del lado derecho -->
        <ul class="navbar-nav">
          <!-- Si el usuario está autenticado, mostrar menú de administración -->
          <li v-if="authStore.isAuthenticated" class="nav-item dropdown">
            <a 
              class="nav-link dropdown-toggle" 
              href="#" 
              role="button" 
              data-bs-toggle="dropdown" 
              aria-expanded="false"
            >
              <i class="bi bi-gear me-1"></i>Administrar
            </a>
            <ul class="dropdown-menu dropdown-menu-end">
              <!-- Enlaces a las secciones de administración -->
              <li>
                <router-link class="dropdown-item" to="/categorias">
                  <i class="bi bi-tags me-2"></i>Categorías
                </router-link>
              </li>
              <li>
                <router-link class="dropdown-item" to="/presentaciones">
                  <i class="bi bi-box me-2"></i>Presentaciones
                </router-link>
              </li>
              <li>
                <router-link class="dropdown-item" to="/productos">
                  <i class="bi bi-basket me-2"></i>Productos
                </router-link>
              </li>
            </ul>
          </li>

          <!-- Información del usuario y botón de logout -->
          <li v-if="authStore.isAuthenticated" class="nav-item dropdown">
            <a 
              class="nav-link dropdown-toggle" 
              href="#" 
              role="button" 
              data-bs-toggle="dropdown" 
              aria-expanded="false"
            >
              <i class="bi bi-person-circle me-1"></i>
              {{ authStore.currentUser?.email || 'Usuario' }}
            </a>
            <ul class="dropdown-menu dropdown-menu-end">
              <li>
                <button class="dropdown-item" @click="logout">
                  <i class="bi bi-box-arrow-right me-2"></i>Cerrar Sesión
                </button>
              </li>
            </ul>
          </li>

          <!-- Si no está autenticado, mostrar enlace al login -->
          <li v-else class="nav-item">
            <router-link class="nav-link" to="/login">
              <i class="bi bi-box-arrow-in-right me-1"></i>Iniciar Sesión
            </router-link>
          </li>
        </ul>
      </div>
    </div>
  </nav>
</template>

<script>
import { useAuthStore } from '../store/auth'
import { useRouter } from 'vue-router'

export default {
  name: 'Navbar',
  
  // Configuración del componente usando Composition API
  setup() {
    // Obtener el store de autenticación y el router
    const authStore = useAuthStore()
    const router = useRouter()
    
    /**
     * Función para cerrar sesión del usuario
     * Limpia el estado de autenticación y redirige al login
     */
    const logout = () => {
      // Cerrar sesión en el store
      authStore.logout()
      
      // Redirigir al login
      router.push('/login')
    }
    
    // Retornar las propiedades y métodos que necesita el template
    return {
      authStore,
      logout
    }
  }
}
</script>

<style scoped>
/* Estilos específicos del navbar */

/* Fondo con gradiente para el navbar */
.navbar.bg-gradient {
  background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%) !important;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  backdrop-filter: blur(10px);
}

/* Estilos para el logo y título */
.navbar-brand {
  font-weight: 700;
  font-size: 1.3rem;
  color: #ffffff !important;
  text-decoration: none;
  transition: all 0.3s ease;
}

.navbar-brand:hover {
  color: #ecf0f1 !important;
  transform: translateY(-1px);
}

.brand-icon {
  font-size: 1.5rem;
  color: #3498db;
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0%, 100% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.1);
  }
}

.brand-text {
  background: linear-gradient(45deg, #3498db, #2ecc71);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

/* Estilos para los enlaces de navegación */
.navbar-nav .nav-link {
  color: rgba(255, 255, 255, 0.9) !important;
  font-weight: 500;
  padding: 0.5rem 1rem;
  border-radius: 8px;
  margin: 0 0.2rem;
  transition: all 0.3s ease;
}

.navbar-nav .nav-link:hover {
  color: #ffffff !important;
  background: rgba(255, 255, 255, 0.1);
  transform: translateY(-1px);
}

/* Estilos para el menú desplegable */
.dropdown-menu {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 12px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
  margin-top: 0.5rem;
}

.dropdown-item {
  color: #2c3e50;
  font-weight: 500;
  padding: 0.75rem 1rem;
  transition: all 0.3s ease;
  border-radius: 8px;
  margin: 0.2rem;
}

.dropdown-item:hover {
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: #ffffff;
  transform: translateX(5px);
}

/* Estilos para el botón de logout */
.dropdown-item[data-v-] {
  color: #e74c3c;
}

.dropdown-item[data-v-]:hover {
  background: linear-gradient(135deg, #e74c3c, #c0392b);
  color: #ffffff;
}

/* Responsive design */
@media (max-width: 991.98px) {
  .navbar-brand {
    font-size: 1.1rem;
  }
  
  .brand-icon {
    font-size: 1.3rem;
  }
  
  .navbar-nav .nav-link {
    padding: 0.75rem 1rem;
    margin: 0.1rem 0;
  }
  
  .dropdown-menu {
    background: rgba(255, 255, 255, 0.98);
    border: none;
    box-shadow: none;
  }
}
</style>
