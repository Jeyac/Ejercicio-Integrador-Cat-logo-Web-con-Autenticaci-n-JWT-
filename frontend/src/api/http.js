/**
 * Cliente HTTP - Configuración de Axios
 * =====================================
 * 
 * Este módulo configura Axios como cliente HTTP para todas las comunicaciones
 * con el backend Flask. Incluye:
 * 
 * - Configuración base (URL, timeout, headers)
 * - Interceptores para manejo automático de tokens JWT
 * - Manejo de errores de autenticación (401)
 * - Configuración de CORS y credenciales
 * 
 * Funcionalidades:
 * - Inyección automática del token de acceso en todas las peticiones
 * - Limpieza automática de tokens expirados
 * - Manejo centralizado de errores de autenticación
 * - Configuración consistente para toda la aplicación
 */

import axios from 'axios'

// Crear instancia de Axios con configuración base
const api = axios.create({
  // URL base del backend Flask - Usar variable de entorno o IP por defecto
  baseURL: process.env.VUE_APP_API_URL || 'http://192.168.0.105:5000/api',
  
  // Timeout de 10 segundos para evitar peticiones colgadas
  timeout: 10000,
  
  // Headers por defecto para todas las peticiones
  headers: {
    'Content-Type': 'application/json'
  }
})

// Interceptor de peticiones - Se ejecuta antes de cada petición
api.interceptors.request.use(
  (config) => {
    // Obtener el token de acceso del localStorage
    const accessToken = localStorage.getItem('access_token')
    
    // Si existe un token, agregarlo al header Authorization
    if (accessToken) {
      config.headers.Authorization = `Bearer ${accessToken}`
    }
    
    return config
  },
  (error) => {
    // En caso de error en la configuración de la petición
    return Promise.reject(error)
  }
)

// Interceptor de respuestas - Se ejecuta después de cada respuesta
api.interceptors.response.use(
  (response) => {
    // Si la respuesta es exitosa, devolverla tal como está
    return response
  },
  (error) => {
    // Si la respuesta es un error 401 (No autorizado)
    if (error.response?.status === 401) {
      // Limpiar tokens expirados del localStorage
      localStorage.removeItem('access_token')
      localStorage.removeItem('refresh_token')
      
      // Nota: No redirigimos automáticamente para evitar loops
      // El manejo de redirección se hace en los componentes
    }
    
    // Rechazar la promesa con el error original
    return Promise.reject(error)
  }
)

// Exportar la instancia configurada
export default api
