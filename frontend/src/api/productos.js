import api from './http'

export const productosApi = {
  async getAll(params = {}) {
    const response = await api.get('/productos', { params })
    return response.data
  },

  async getById(id) {
    const response = await api.get(`/productos/${id}`)
    return response.data
  },

  async create(data) {
    const response = await api.post('/productos', data)
    return response.data
  },

  async update(id, data) {
    // Actualizar un producto existente por su ID
    const response = await api.put(`/productos/${id}`, data)
    return response.data
  },

  async delete(id) {
    const response = await api.delete(`/productos/${id}`)
    return response.data
  }
}

