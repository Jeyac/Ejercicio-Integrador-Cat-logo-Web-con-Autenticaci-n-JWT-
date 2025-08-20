import api from './http'

export const categoriasApi = {
  async getAll(params = {}) {
    const response = await api.get('/categorias', { params })
    return response.data
  },

  async getById(id) {
    const response = await api.get(`/categorias/${id}`)
    return response.data
  },

  async create(data) {
    const response = await api.post('/categorias', data)
    return response.data
  },

  async update(id, data) {
    // Actualizar una categoría existente por su ID
    const response = await api.put(`/categorias/${id}`, data)
    return response.data
  },

  async delete(id) {
    const response = await api.delete(`/categorias/${id}`)
    return response.data
  }
}

