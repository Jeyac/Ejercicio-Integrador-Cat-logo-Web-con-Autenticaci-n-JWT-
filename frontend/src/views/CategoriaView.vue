<template>
  <div class="categoria-view">
    <div class="container-fluid py-4">
      <div class="row">
        <div class="col-12">
          <div class="page-header mb-4">
            <div class="d-flex justify-content-between align-items-center">
              <div class="header-content">
                <h1 class="page-title">
                  <i class="bi bi-tags animated-icon"></i>
                  Categorías
                </h1>
                <p class="page-subtitle">Administra las categorías de productos</p>
              </div>
              <button 
                class="btn btn-primary btn-modern"
                data-bs-toggle="modal" 
                data-bs-target="#categoriaModal"
                @click="openCreateModal"
              >
                <i class="bi bi-plus-circle me-2"></i>
                Nueva Categoría
              </button>
            </div>
          </div>
        
          <div class="filter-card mb-4">
            <div class="card-body">
              <div class="row g-3 align-items-end">
                <div class="col-md-6">
                  <label class="form-label fw-semibold">
                    <i class="bi bi-search me-1"></i>Buscar categorías
                  </label>
                  <div class="search-input-wrapper">
                    <input 
                      type="text" 
                      class="form-control search-input" 
                      placeholder="Escribe para buscar..."
                      v-model="searchTerm"
                      @input="debouncedSearch"
                    >
                    <i class="bi bi-search search-icon"></i>
                  </div>
                </div>
                <div class="col-md-3">
                  <label class="form-label fw-semibold">
                    <i class="bi bi-list-ul me-1"></i>Mostrar
                  </label>
                  <select class="form-select modern-select" v-model="pageSize" @change="loadCategorias">
                    <option value="10">10 por página</option>
                    <option value="25">25 por página</option>
                    <option value="50">50 por página</option>
                  </select>
                </div>
                <div class="col-md-3">
                  <button class="btn btn-outline-primary w-100" @click="resetFilters">
                    <i class="bi bi-arrow-clockwise me-2"></i>Limpiar
                  </button>
                </div>
              </div>
            </div>
          </div>
        
          <div class="card">
            <div class="card-body">
              <CrudTable
                :items="categorias"
                :columns="columns"
                :loading="loading"
                empty-message="No hay categorías registradas"
                @edit="openEditModal"
                @delete="confirmDelete"
              />
              
              <div v-if="totalPages > 1" class="d-flex justify-content-between align-items-center mt-4">
                <div class="text-muted">
                  Mostrando {{ (currentPage - 1) * pageSize + 1 }} - {{ Math.min(currentPage * pageSize, totalItems) }} 
                  de {{ totalItems }} resultados
                </div>
                <nav>
                  <ul class="pagination mb-0">
                    <li class="page-item" :class="{ disabled: currentPage === 1 }">
                      <button class="page-link" @click="goToPage(currentPage - 1)" :disabled="currentPage === 1">
                        Anterior
                      </button>
                    </li>
                    <li 
                      v-for="page in visiblePages" 
                      :key="page"
                      class="page-item" 
                      :class="{ active: page === currentPage }"
                    >
                      <button class="page-link" @click="goToPage(page)">
                        {{ page }}
                      </button>
                    </li>
                    <li class="page-item" :class="{ disabled: currentPage === totalPages }">
                      <button class="page-link" @click="goToPage(currentPage + 1)" :disabled="currentPage === totalPages">
                        Siguiente
                      </button>
                    </li>
                  </ul>
                </nav>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <CrudForm
      modal-id="categoriaModal"
      title="Categoría"
      :item="selectedItem"
      :loading="formLoading"
      :errors="formErrors"
      @submit="handleSubmit"
      @close="closeModal"
    >
      <template #default="{ formData, errors }">
        <div class="mb-3">
          <label for="nombre" class="form-label">Nombre *</label>
          <input 
            type="text" 
            class="form-control"
            :class="{ 'is-invalid': errors.nombre }"
            id="nombre"
            v-model="formData.nombre"
            required
            maxlength="100"
          >
          <div v-if="errors.nombre" class="invalid-feedback">
            {{ errors.nombre }}
          </div>
        </div>
        
        <div class="mb-3">
          <label for="descripcion" class="form-label">Descripción</label>
          <textarea 
            class="form-control"
            :class="{ 'is-invalid': errors.descripcion }"
            id="descripcion"
            v-model="formData.descripcion"
            rows="3"
            maxlength="500"
          ></textarea>
          <div v-if="errors.descripcion" class="invalid-feedback">
            {{ errors.descripcion }}
          </div>
          <div class="form-text">
            {{ (formData.descripcion || '').length }}/500 caracteres
          </div>
        </div>
      </template>
    </CrudForm>
    
    <div class="modal fade" id="deleteModal" tabindex="-1">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Confirmar eliminación</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
          </div>
          <div class="modal-body">
            <p>¿Estás seguro de que deseas eliminar la categoría <strong>{{ itemToDelete?.nombre }}</strong>?</p>
            <p class="text-muted">Esta acción no se puede deshacer.</p>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancelar</button>
            <button type="button" class="btn btn-danger" @click="deleteItem" :disabled="formLoading">
              <span v-if="formLoading" class="loading-spinner me-2"></span>
              Eliminar
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, computed } from 'vue'
import CrudTable from '../components/CrudTable.vue'
import CrudForm from '../components/CrudForm.vue'
import { categoriasApi } from '../api/categorias'
import { useAuthStore } from '../store/auth'

export default {
  name: 'CategoriaView',
  components: {
    CrudTable,
    CrudForm
  },
  setup() {
    const authStore = useAuthStore()
    const categorias = ref([])
    const loading = ref(false)
    const formLoading = ref(false)
    const selectedItem = ref(null)
    const itemToDelete = ref(null)
    const formErrors = ref({})
    
    const currentPage = ref(1)
    const pageSize = ref(10)
    const totalItems = ref(0)
    const searchTerm = ref('')
    let searchTimeout = null
    
    const columns = [
      { key: 'id', label: 'ID' },
      { key: 'nombre', label: 'Nombre' },
      { key: 'descripcion', label: 'Descripción' },
      { key: 'created_at', label: 'Creado', type: 'date' }
    ]
    
    const totalPages = computed(() => Math.ceil(totalItems.value / pageSize.value))
    
    const visiblePages = computed(() => {
      const pages = []
      const start = Math.max(1, currentPage.value - 2)
      const end = Math.min(totalPages.value, start + 4)
      
      for (let i = start; i <= end; i++) {
        pages.push(i)
      }
      return pages
    })
    
    const loadCategorias = async (page = currentPage.value) => {
      try {
        loading.value = true
        const params = {
          page,
          size: pageSize.value
        }
        
        if (searchTerm.value.trim()) {
          params.q = searchTerm.value.trim()
        }
        
        const response = await categoriasApi.getAll(params)
        
        if (response.success) {
          categorias.value = response.data.items
          totalItems.value = response.data.total
          currentPage.value = response.data.page
        }
      } catch (error) {
        console.error('Error cargando categorías:', error)
        if (error.response?.status === 401) {
          console.log('Error de autenticación al cargar categorías')
        }
      } finally {
        loading.value = false
      }
    }
    
    const debouncedSearch = () => {
      clearTimeout(searchTimeout)
      searchTimeout = setTimeout(() => {
        currentPage.value = 1
        loadCategorias()
      }, 500)
    }
    
    const resetFilters = () => {
      searchTerm.value = ''
      pageSize.value = 10
      currentPage.value = 1
      loadCategorias()
    }
    
    const goToPage = (page) => {
      if (page >= 1 && page <= totalPages.value) {
        loadCategorias(page)
      }
    }
    
    const openCreateModal = () => {
      selectedItem.value = null
      formErrors.value = {}
    }
    
    const openEditModal = (item) => {
      // Configurar el item seleccionado para edición
      selectedItem.value = { ...item }
      formErrors.value = {}
      
      // Abrir el modal usando Bootstrap
      const modalElement = document.getElementById('categoriaModal')
      if (modalElement) {
        const modal = new bootstrap.Modal(modalElement)
        modal.show()
      }
    }
    
    const closeModal = () => {
      selectedItem.value = null
      formErrors.value = {}
    }
    
    const handleSubmit = async (formData) => {
      try {
        formLoading.value = true
        formErrors.value = {}
        
        let response
        if (selectedItem.value?.id) {
          // Modo edición: enviar solo los campos necesarios para actualización
          const updateData = {
            nombre: formData.nombre,
            descripcion: formData.descripcion
          }
          response = await categoriasApi.update(selectedItem.value.id, updateData)
        } else {
          // Modo creación: enviar todos los datos del formulario
          response = await categoriasApi.create(formData)
        }
        
        if (response.success) {
          const modal = bootstrap.Modal.getInstance(document.getElementById('categoriaModal'))
          modal.hide()
          await loadCategorias()
          alert(response.message)
        }
      } catch (error) {
        console.error('Error guardando categoría:', error)
        if (error.response?.data?.message) {
          alert(error.response.data.message)
        } else if (error.response?.status === 401) {
          alert('Error de autenticación. Por favor, inicie sesión nuevamente.')
        }
      } finally {
        formLoading.value = false
      }
    }
    
    const confirmDelete = (item) => {
      itemToDelete.value = item
      const modal = new bootstrap.Modal(document.getElementById('deleteModal'))
      modal.show()
    }
    
    const deleteItem = async () => {
      try {
        formLoading.value = true
        
        const response = await categoriasApi.delete(itemToDelete.value.id)
        
        if (response.success) {
          const modal = bootstrap.Modal.getInstance(document.getElementById('deleteModal'))
          modal.hide()
          await loadCategorias()
          alert(response.message)
        }
      } catch (error) {
        console.error('Error eliminando categoría:', error)
        if (error.response?.data?.message) {
          alert(error.response.data.message)
        } else if (error.response?.status === 401) {
          alert('Error de autenticación. Por favor, inicie sesión nuevamente.')
        }
      } finally {
        formLoading.value = false
      }
    }
    
    onMounted(() => {
      loadCategorias()
    })
    
    return {
      categorias,
      loading,
      formLoading,
      selectedItem,
      itemToDelete,
      formErrors,
      columns,
      currentPage,
      pageSize,
      totalItems,
      totalPages,
      visiblePages,
      searchTerm,
      loadCategorias,
      debouncedSearch,
      resetFilters,
      goToPage,
      openCreateModal,
      openEditModal,
      closeModal,
      handleSubmit,
      confirmDelete,
      deleteItem
    }
  }
}
</script>

<style scoped>
.categoria-view {
  animation: fadeInUp 0.6s ease-out;
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.page-header {
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.95), rgba(255, 255, 255, 0.8));
  backdrop-filter: blur(10px);
  border-radius: 20px;
  padding: 2rem;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  margin-bottom: 2rem;
}

.page-title {
  font-size: 2.5rem;
  font-weight: 700;
  color: #2c3e50;
  margin: 0;
  display: flex;
  align-items: center;
}

.page-subtitle {
  color: #6c757d;
  font-size: 1.1rem;
  margin: 0.5rem 0 0 0;
  font-weight: 500;
}

.animated-icon {
  color: #667eea;
  margin-right: 1rem;
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

.filter-card {
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.95), rgba(255, 255, 255, 0.9));
  backdrop-filter: blur(10px);
  border-radius: 16px;
  border: 1px solid rgba(255, 255, 255, 0.2);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  transition: all 0.3s ease;
}

.filter-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.12);
}

.search-input-wrapper {
  position: relative;
}

.search-input {
  padding-left: 3rem;
  border-radius: 12px;
  border: 2px solid rgba(102, 126, 234, 0.2);
  transition: all 0.3s ease;
  background: rgba(255, 255, 255, 0.9);
}

.search-input:focus {
  border-color: #667eea;
  box-shadow: 0 0 0 0.2rem rgba(102, 126, 234, 0.25);
  background: #fff;
}

.search-icon {
  position: absolute;
  left: 1rem;
  top: 50%;
  transform: translateY(-50%);
  color: #6c757d;
  pointer-events: none;
}

.modern-select {
  border-radius: 12px;
  border: 2px solid rgba(102, 126, 234, 0.2);
  background: rgba(255, 255, 255, 0.9);
  transition: all 0.3s ease;
}

.modern-select:focus {
  border-color: #667eea;
  box-shadow: 0 0 0 0.2rem rgba(102, 126, 234, 0.25);
  background: #fff;
}

.form-label {
  color: #495057;
  font-size: 0.9rem;
  margin-bottom: 0.5rem;
}

.btn-outline-primary {
  border: 2px solid #667eea;
  color: #667eea;
  border-radius: 12px;
  font-weight: 600;
  transition: all 0.3s ease;
}

.btn-outline-primary:hover {
  background: linear-gradient(135deg, #667eea, #764ba2);
  border-color: #667eea;
  transform: translateY(-1px);
  box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
}

.card {
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.95), rgba(255, 255, 255, 0.9));
  backdrop-filter: blur(10px);
  border-radius: 16px;
  border: 1px solid rgba(255, 255, 255, 0.2);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
}

@media (max-width: 768px) {
  .page-title {
    font-size: 2rem;
  }
  
  .page-header {
    padding: 1.5rem;
  }
  
  .btn-modern {
    padding: 10px 20px;
    font-size: 0.9rem;
  }
}
</style> 