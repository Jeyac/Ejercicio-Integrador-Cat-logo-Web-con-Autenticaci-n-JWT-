<template>
  <div class="container py-5">
    <div class="row justify-content-center">
      <div class="col-lg-8">
        <div class="text-center mb-5">
          <h1 class="display-4 fw-bold text-primary">Catálogo de Productos</h1>
          <p class="lead text-muted">
            Sistema completo de administración de productos, categorías y presentaciones
          </p>
          
          <!-- Botones de acción arriba de las tarjetas -->
          <div class="mt-4">
            <div v-if="!isAuthenticated">
              <router-link to="/login" class="btn btn-login btn-lg px-5 py-3">
                <i class="bi bi-shield-lock me-2"></i>
                <span>Iniciar Sesión</span>
                <i class="bi bi-arrow-right ms-2"></i>
              </router-link>
            </div>
            <div v-else>
              <p class="mb-4 text-muted">¡Bienvenido de vuelta! Comienza a administrar tu catálogo.</p>
              <div class="d-flex gap-4 justify-content-center flex-wrap">
                <router-link to="/categorias" class="btn btn-outline-primary btn-lg px-4 py-3">
                  <i class="bi bi-tags me-2"></i>Categorías
                </router-link>
                <router-link to="/presentaciones" class="btn btn-outline-success btn-lg px-4 py-3">
                  <i class="bi bi-box me-2"></i>Presentaciones
                </router-link>
                <router-link to="/productos" class="btn btn-outline-warning btn-lg px-4 py-3">
                  <i class="bi bi-basket me-2"></i>Productos
                </router-link>
              </div>
            </div>
          </div>
        </div>
        
        <div class="row g-4">
          <div class="col-md-4">
            <router-link 
              :to="isAuthenticated ? '/categorias' : '#'" 
              class="text-decoration-none"
              :class="{ 'card-clickable': isAuthenticated }"
            >
              <div class="card h-100 shadow-sm" :class="{ 'card-interactive': isAuthenticated }">
                <div class="card-body text-center">
                  <div class="bg-primary bg-opacity-10 rounded-circle d-inline-flex align-items-center justify-content-center mb-3" style="width: 80px; height: 80px;">
                    <i class="bi bi-tags fs-1 text-primary"></i>
                  </div>
                  <h5 class="card-title">Categorías</h5>
                  <p class="card-text text-muted">
                    Organiza tus productos por categorías para una mejor gestión y búsqueda.
                  </p>
                  <div v-if="isAuthenticated" class="mt-3">
                    <span class="badge bg-primary">Click para administrar</span>
                  </div>
                </div>
              </div>
            </router-link>
          </div>
          
          <div class="col-md-4">
            <router-link 
              :to="isAuthenticated ? '/presentaciones' : '#'" 
              class="text-decoration-none"
              :class="{ 'card-clickable': isAuthenticated }"
            >
              <div class="card h-100 shadow-sm" :class="{ 'card-interactive': isAuthenticated }">
                <div class="card-body text-center">
                  <div class="bg-success bg-opacity-10 rounded-circle d-inline-flex align-items-center justify-content-center mb-3" style="width: 80px; height: 80px;">
                    <i class="bi bi-box fs-1 text-success"></i>
                  </div>
                  <h5 class="card-title">Presentaciones</h5>
                  <p class="card-text text-muted">
                    Define diferentes presentaciones para tus productos (tamaños, formatos, etc.).
                  </p>
                  <div v-if="isAuthenticated" class="mt-3">
                    <span class="badge bg-success">Click para administrar</span>
                  </div>
                </div>
              </div>
            </router-link>
          </div>
          
          <div class="col-md-4">
            <router-link 
              :to="isAuthenticated ? '/productos' : '#'" 
              class="text-decoration-none"
              :class="{ 'card-clickable': isAuthenticated }"
            >
              <div class="card h-100 shadow-sm" :class="{ 'card-interactive': isAuthenticated }">
                <div class="card-body text-center">
                  <div class="bg-warning bg-opacity-10 rounded-circle d-inline-flex align-items-center justify-content-center mb-3" style="width: 80px; height: 80px;">
                    <i class="bi bi-basket fs-1 text-warning"></i>
                  </div>
                  <h5 class="card-title">Productos</h5>
                  <p class="card-text text-muted">
                    Administra tu inventario completo con precios, categorías y presentaciones.
                  </p>
                  <div v-if="isAuthenticated" class="mt-3">
                    <span class="badge bg-warning">Click para administrar</span>
                  </div>
                </div>
              </div>
            </router-link>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { computed } from 'vue'
import { useAuthStore } from '../store/auth'

export default {
  name: 'HomeView',
  setup() {
    const authStore = useAuthStore()
    
    const isAuthenticated = computed(() => authStore.isAuthenticated)
    
    return {
      isAuthenticated
    }
  }
}
</script>

<style scoped>
/* Fondo blanco para la página */
.container {
  background-color: white;
  border-radius: 15px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  padding: 2rem;
}

/* Estilos para los botones grandes */
.btn-lg {
  font-size: 1.1rem;
  font-weight: 600;
  border-radius: 12px;
  transition: all 0.3s ease;
}

.btn-lg:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.15);
}

/* Estilos especiales para el botón de login */
.btn-login {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border: none;
  color: white;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 1px;
  position: relative;
  overflow: hidden;
  box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3);
}

.btn-login:hover {
  background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
  transform: translateY(-3px);
  box-shadow: 0 12px 35px rgba(102, 126, 234, 0.4);
  color: white;
}

.btn-login:before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
  transition: left 0.5s;
}

.btn-login:hover:before {
  left: 100%;
}

.btn-login i {
  transition: transform 0.3s ease;
}

.btn-login:hover i.bi-arrow-right {
  transform: translateX(5px);
}

/* Espaciado mejorado */
.gap-4 {
  gap: 1.5rem !important;
}

/* Estilos para las tarjetas */
.card {
  border: none;
  border-radius: 15px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
  transition: all 0.3s ease;
}

.card:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.12);
}

/* Estilos para tarjetas interactivas (cuando el usuario está autenticado) */
.card-interactive {
  cursor: pointer;
  border: 2px solid transparent;
}

.card-interactive:hover {
  transform: translateY(-5px);
  box-shadow: 0 12px 35px rgba(0, 0, 0, 0.15);
  border-color: #007bff;
}

/* Estilos para el enlace de las tarjetas */
.card-clickable {
  display: block;
}

.card-clickable .card-interactive:hover .card-title {
  color: #007bff;
}

/* Efecto de pulso para las badges */
.badge {
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0% {
    opacity: 1;
  }
  50% {
    opacity: 0.7;
  }
  100% {
    opacity: 1;
  }
}

/* Estilos específicos para tarjetas no interactivas */
.card:not(.card-interactive) {
  opacity: 0.9;
}

.card:not(.card-interactive):hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.1);
}
</style>

