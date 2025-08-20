/**
 * API de Autenticación
 * ====================
 * 
 * Este módulo contiene todas las funciones para interactuar con los endpoints
 * de autenticación del backend Flask:
 * 
 * - Login de usuarios
 * - Registro de nuevos usuarios
 * - Refresh de tokens JWT
 * - Verificación de información del usuario
 * - Logout (invalidación de tokens)
 * 
 * Todas las funciones utilizan el cliente HTTP configurado en http.js
 * que maneja automáticamente la inyección de tokens y manejo de errores.
 */

import api from './http'

export const authApi = {
  /**
   * Inicia sesión de un usuario
   * @param {Object} credentials - Credenciales de login
   * @param {string} credentials.email - Email del usuario
   * @param {string} credentials.password - Contraseña del usuario
   * @returns {Promise<Object>} Respuesta del servidor con tokens y datos del usuario
   */
  async login(credentials) {
    const response = await api.post('/auth/login', credentials)
    return response.data
  },

  /**
   * Registra un nuevo usuario
   * @param {Object} userData - Datos del usuario a registrar
   * @param {string} userData.email - Email del usuario
   * @param {string} userData.password - Contraseña del usuario
   * @param {string} userData.nombre - Nombre del usuario
   * @returns {Promise<Object>} Respuesta del servidor con tokens y datos del usuario
   */
  async register(userData) {
    const response = await api.post('/auth/register', userData)
    return response.data
  },

  /**
   * Refresca el token de acceso usando el refresh token
   * @returns {Promise<Object>} Respuesta del servidor con el nuevo access token
   */
  async refresh() {
    const response = await api.post('/auth/refresh')
    return response.data
  },

  /**
   * Obtiene la información del usuario autenticado
   * @returns {Promise<Object>} Respuesta del servidor con datos del usuario
   */
  async me() {
    const response = await api.get('/auth/me')
    return response.data
  },

  /**
   * Cierra la sesión del usuario (invalida el refresh token)
   * @returns {Promise<Object>} Respuesta del servidor
   */
  async logout() {
    const response = await api.post('/auth/logout')
    return response.data
  }
}
