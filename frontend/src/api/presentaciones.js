import api from './http'

export const presentacionesApi = {
  async getAll(params = {}) {
    const response = await api.get('/presentaciones', { params })
    return response.data
  },

  async getById(id) {
    const response = await api.get(`/presentaciones/${id}`)
    return response.data
  },

  async create(data) {
    const response = await api.post('/presentaciones', data)
    return response.data
  },

  async update(id, data) {
    // Actualizar una presentación existente por su ID
    const response = await api.put(`/presentaciones/${id}`, data)
    return response.data
  },

  async delete(id) {
    const response = await api.delete(`/presentaciones/${id}`)
    return response.data
  }
}

