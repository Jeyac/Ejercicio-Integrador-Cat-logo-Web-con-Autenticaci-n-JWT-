<template>
  <div class="login-container">
    <div class="container py-5">
      <div class="row justify-content-center">
        <div class="col-md-6 col-lg-5">
          <div class="login-card">
            <div class="login-header">
              <div class="login-icon">
                <i class="bi bi-shield-lock"></i>
              </div>
              <h2 class="login-title">{{ isLoginMode ? 'Iniciar Sesión' : 'Registro' }}</h2>
              <p class="login-subtitle">
                {{ isLoginMode ? 'Accede a tu cuenta del catálogo' : 'Crea tu cuenta nueva' }}
              </p>
            </div>
            
            <div v-if="message" class="alert" :class="messageClass" role="alert">
              {{ message }}
            </div>
            
            <form @submit.prevent="handleSubmit" class="login-form">
              <div v-if="!isLoginMode" class="form-group">
                <div class="input-wrapper">
                  <i class="bi bi-person input-icon"></i>
                  <input 
                    type="text" 
                    class="form-control-modern" 
                    id="nombre"
                    v-model="formData.nombre"
                    placeholder="Nombre completo"
                    required
                    :disabled="loading"
                  >
                  <label for="nombre" class="floating-label">Nombre completo</label>
                </div>
              </div>
              
              <div class="form-group">
                <div class="input-wrapper">
                  <i class="bi bi-envelope input-icon"></i>
                  <input 
                    type="email" 
                    class="form-control-modern" 
                    id="email"
                    v-model="formData.email"
                    placeholder="Email"
                    required
                    :disabled="loading"
                  >
                  <label for="email" class="floating-label">Email</label>
                </div>
              </div>
              
              <div class="form-group">
                <div class="input-wrapper">
                  <i class="bi bi-lock input-icon"></i>
                  <input 
                    type="password" 
                    class="form-control-modern" 
                    id="password"
                    v-model="formData.password"
                    placeholder="Contraseña"
                    required
                    :disabled="loading"
                    :minlength="isLoginMode ? 1 : 6"
                  >
                  <label for="password" class="floating-label">Contraseña</label>
                </div>
                <div v-if="!isLoginMode" class="form-hint">
                  Mínimo 6 caracteres
                </div>
              </div>
              
              <div class="form-group">
                <button 
                  type="submit" 
                  class="btn-submit"
                  :disabled="loading"
                >
                  <span v-if="loading" class="loading-spinner me-2"></span>
                  <i class="bi bi-box-arrow-in-right me-2"></i>
                  {{ isLoginMode ? 'Iniciar Sesión' : 'Registrarse' }}
                  <i class="bi bi-arrow-right ms-2"></i>
                </button>
              </div>
            </form>
            
            <div class="login-footer">
              <button 
                type="button" 
                class="btn-toggle"
                @click="toggleMode"
                :disabled="loading"
              >
                {{ isLoginMode ? '¿No tienes cuenta? Regístrate' : '¿Ya tienes cuenta? Inicia sesión' }}
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../store/auth'

export default {
  name: 'LoginView',
  setup() {
    const router = useRouter()
    const authStore = useAuthStore()
    
    const isLoginMode = ref(true)
    const loading = ref(false)
    const message = ref('')
    const messageType = ref('success')
    
    const formData = ref({
      email: '',
      password: '',
      nombre: ''
    })
    
    const messageClass = computed(() => {
      return messageType.value === 'success' ? 'alert-success' : 'alert-danger'
    })
    
    const toggleMode = () => {
      isLoginMode.value = !isLoginMode.value
      message.value = ''
      formData.value = {
        email: '',
        password: '',
        nombre: ''
      }
    }
    
    const handleSubmit = async () => {
      loading.value = true
      message.value = ''
      
      try {
        let result
        
        if (isLoginMode.value) {
          result = await authStore.login({
            email: formData.value.email,
            password: formData.value.password
          })
        } else {
          result = await authStore.register({
            email: formData.value.email,
            password: formData.value.password,
            nombre: formData.value.nombre
          })
        }
        
        if (result.success) {
          message.value = isLoginMode.value ? 'Inicio de sesión exitoso' : 'Registro exitoso'
          messageType.value = 'success'
          
          setTimeout(() => {
            router.push('/')
          }, 1000)
        } else {
          message.value = result.message || 'Error en la operación'
          messageType.value = 'danger'
        }
      } catch (error) {
        message.value = 'Error de conexión'
        messageType.value = 'danger'
      } finally {
        loading.value = false
      }
    }
    
    return {
      isLoginMode,
      loading,
      message,
      messageClass,
      formData,
      toggleMode,
      handleSubmit
    }
  }
}
</script>

<style scoped>
/* Contenedor principal del login */
.login-container {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  padding: 2rem 0;
}

/* Tarjeta de login */
.login-card {
  background: white;
  border-radius: 20px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.1);
  padding: 3rem 2.5rem;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
}

/* Header del login */
.login-header {
  text-align: center;
  margin-bottom: 2.5rem;
}

.login-icon {
  width: 80px;
  height: 80px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 1.5rem;
  box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3);
}

.login-icon i {
  font-size: 2rem;
  color: white;
}

.login-title {
  font-size: 1.8rem;
  font-weight: 700;
  color: #2c3e50;
  margin-bottom: 0.5rem;
}

.login-subtitle {
  color: #6c757d;
  font-size: 1rem;
  margin-bottom: 0;
}

/* Formulario */
.login-form {
  margin-bottom: 2rem;
}

.form-group {
  margin-bottom: 1.5rem;
}

/* Input wrapper */
.input-wrapper {
  position: relative;
}

.input-icon {
  position: absolute;
  left: 15px;
  top: 50%;
  transform: translateY(-50%);
  color: #6c757d;
  font-size: 1.1rem;
  z-index: 2;
}

/* Input moderno */
.form-control-modern {
  width: 100%;
  padding: 15px 15px 15px 45px;
  border: 2px solid #e9ecef;
  border-radius: 12px;
  font-size: 1rem;
  background: #f8f9fa;
  transition: all 0.3s ease;
  outline: none;
}

.form-control-modern:focus {
  border-color: #667eea;
  background: white;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.form-control-modern:focus + .floating-label,
.form-control-modern:not(:placeholder-shown) + .floating-label {
  top: -10px;
  left: 12px;
  font-size: 0.75rem;
  color: #667eea;
  background: white;
  padding: 0 5px;
}

/* Etiqueta flotante */
.floating-label {
  position: absolute;
  left: 45px;
  top: 50%;
  transform: translateY(-50%);
  color: #6c757d;
  font-size: 1rem;
  pointer-events: none;
  transition: all 0.3s ease;
  background: transparent;
}

/* Hint del formulario */
.form-hint {
  font-size: 0.875rem;
  color: #6c757d;
  margin-top: 0.5rem;
  padding-left: 15px;
}

/* Botón de submit */
.btn-submit {
  width: 100%;
  padding: 15px 20px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border: none;
  border-radius: 12px;
  color: white;
  font-size: 1.1rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  cursor: pointer;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
  box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3);
}

.btn-submit:hover:not(:disabled) {
  background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
  transform: translateY(-2px);
  box-shadow: 0 12px 35px rgba(102, 126, 234, 0.4);
}

.btn-submit:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.btn-submit:before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
  transition: left 0.5s;
}

.btn-submit:hover:not(:disabled):before {
  left: 100%;
}

/* Footer del login */
.login-footer {
  text-align: center;
  padding-top: 1rem;
  border-top: 1px solid #e9ecef;
}

.btn-toggle {
  background: none;
  border: none;
  color: #667eea;
  font-size: 0.95rem;
  cursor: pointer;
  transition: all 0.3s ease;
  text-decoration: none;
}

.btn-toggle:hover:not(:disabled) {
  color: #764ba2;
  text-decoration: underline;
}

.btn-toggle:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* Alertas mejoradas */
.alert {
  border-radius: 12px;
  border: none;
  padding: 12px 16px;
  margin-bottom: 1.5rem;
  font-size: 0.95rem;
}

.alert-success {
  background: #d1edff;
  color: #0c5460;
}

.alert-danger {
  background: #f8d7da;
  color: #721c24;
}

/* Loading spinner */
.loading-spinner {
  display: inline-block;
  width: 16px;
  height: 16px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-radius: 50%;
  border-top-color: white;
  animation: spin 1s ease-in-out infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

/* Responsive */
@media (max-width: 768px) {
  .login-card {
    padding: 2rem 1.5rem;
    margin: 1rem;
  }
  
  .login-title {
    font-size: 1.5rem;
  }
  
  .login-icon {
    width: 60px;
    height: 60px;
  }
  
  .login-icon i {
    font-size: 1.5rem;
  }
}
</style>

