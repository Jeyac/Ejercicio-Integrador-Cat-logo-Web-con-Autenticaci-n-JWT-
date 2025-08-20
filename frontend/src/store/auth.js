/**
 * Store de Autenticación - Pinia
 * ==============================
 * 
 * Este módulo maneja todo el estado relacionado con la autenticación de usuarios:
 * - Almacenamiento de tokens JWT (access y refresh)
 * - Información del usuario autenticado
 * - Estados de carga y autenticación
 * - Operaciones de login, logout y refresh de tokens
 * 
 * Funcionalidades:
 * - Persistencia de tokens en localStorage
 * - Validación automática de autenticación
 * - Manejo de sesiones expiradas
 * - Carga de información del usuario
 * - Refresh automático de tokens
 */

import { defineStore } from 'pinia'
import { authApi } from '../api/auth'
import api from '../api/http'

export const useAuthStore = defineStore('auth', {
  // Estado reactivo del store
  state: () => ({
    // Información del usuario autenticado
    user: null,
    
    // Tokens JWT (se cargan desde localStorage al inicializar)
    accessToken: localStorage.getItem('access_token') || null,
    refreshToken: localStorage.getItem('refresh_token') || null,
    
    // Estado de carga para operaciones de autenticación
    loading: false
  }),

  // Getters (propiedades computadas)
  getters: {
    /**
     * Verifica si el usuario está autenticado
     * @returns {boolean} true si hay un token de acceso válido
     */
    isAuthenticated: (state) => {
      return !!(state.accessToken || localStorage.getItem('access_token'))
    },

    /**
     * Obtiene la información del usuario actual
     * @returns {Object|null} Información del usuario o null si no está autenticado
     */
    currentUser: (state) => state.user
  },

  // Acciones (métodos que modifican el estado)
  actions: {
    /**
     * Verifica si el usuario está autenticado sin hacer peticiones al servidor
     * @returns {boolean} true si hay un token de acceso
     */
    async ensureAuthenticated() {
      if (!this.accessToken) {
        return false
      }
      return true
    },

    /**
     * Inicia sesión del usuario
     * @param {Object} credentials - Credenciales de login (email, password)
     * @returns {Object} Resultado de la operación {success, message}
     */
    async login(credentials) {
      try {
        this.loading = true
        
        // Realizar petición de login al backend
        const response = await authApi.login(credentials)
        
        if (response.success) {
          // Guardar información del usuario y tokens
          this.user = response.data.user
          this.accessToken = response.data.access_token
          this.refreshToken = response.data.refresh_token
          
          // Persistir tokens en localStorage
          localStorage.setItem('access_token', this.accessToken)
          localStorage.setItem('refresh_token', this.refreshToken)
          
          return { success: true }
        } else {
          return { success: false, message: response.message }
        }
      } catch (error) {
        console.error('Error en login:', error)
        return { 
          success: false, 
          message: error.response?.data?.message || 'Error de conexión' 
        }
      } finally {
        this.loading = false
      }
    },

    /**
     * Refresca el token de acceso usando el refresh token
     * @returns {boolean} true si el refresh fue exitoso
     */
    async refreshAccessToken() {
      try {
        if (!this.refreshToken) {
          return false
        }

        const response = await authApi.refresh()
        
        if (response.success) {
          // Actualizar tokens
          this.accessToken = response.data.access_token
          localStorage.setItem('access_token', this.accessToken)
          return true
        }
        
        return false
      } catch (error) {
        console.error('Error refreshing token:', error)
        return false
      }
    },

    /**
     * Cierra la sesión del usuario
     * Limpia todos los datos de autenticación
     */
    logout() {
      // Limpiar estado del store
      this.user = null
      this.accessToken = null
      this.refreshToken = null
      
      // Limpiar localStorage
      localStorage.removeItem('access_token')
      localStorage.removeItem('refresh_token')
    },

    /**
     * Inicializa la autenticación al cargar la aplicación
     * Carga tokens desde localStorage y verifica validez
     */
    initializeAuth() {
      const accessToken = localStorage.getItem('access_token')
      const refreshToken = localStorage.getItem('refresh_token')
      
      if (accessToken && refreshToken) {
        this.accessToken = accessToken
        this.refreshToken = refreshToken
        // Cargar información del usuario si hay tokens válidos
        this.loadUserInfo()
      }
    },

    /**
     * Verifica la validez del token actual
     * @returns {boolean} true si el token es válido
     */
    async checkTokenValidity() {
      try {
        const response = await authApi.me()
        return response.success
      } catch (error) {
        return false
      }
    },

    /**
     * Carga la información del usuario autenticado
     */
    async loadUserInfo() {
      try {
        const response = await authApi.me()
        if (response.success) {
          this.user = response.data.user
        }
      } catch (error) {
        console.error('Error loading user info:', error)
      }
    }
  }
})
