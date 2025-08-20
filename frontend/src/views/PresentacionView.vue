<template>
  <div class="container-fluid py-4">
    <div class="row">
      <div class="col-12">
        <div class="d-flex justify-content-between align-items-center mb-4">
          <h2 class="h3 mb-0">
            <i class="bi bi-box me-2"></i>Presentaciones
          </h2>
          <button 
            class="btn btn-success"
            data-bs-toggle="modal" 
            data-bs-target="#presentacionModal"
            @click="openCreateModal"
          >
            <i class="bi bi-plus-circle me-2"></i>Nueva Presentación
          </button>
        </div>
        
        <!-- Filtros -->
        <div class="card mb-4">
          <div class="card-body">
            <div class="row g-3">
              <div class="col-md-6">
                <input 
                  type="text" 
                  class="form-control" 
                  placeholder="Buscar por nombre..."
                  v-model="searchTerm"
                  @input="debouncedSearch"
                >
              </div>
              <div class="col-md-3">
                <select class="form-select" v-model="pageSize" @change="loadPresentaciones">
                  <option value="10">10 por página</option>
                  <option value="25">25 por página</option>
                  <option value="50">50 por página</option>
                </select>
              </div>
            </div>
          </div>
        </div>
        
        <!-- Tabla -->
        <div class="card">
          <div class="card-body">
            <CrudTable
              :items="presentaciones"
              :columns="columns"
              :loading="loading"
              empty-message="No hay presentaciones registradas"
              @edit="openEditModal"
              @delete="confirmDelete"
            />
            
            <!-- Paginación -->
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
    
    <!-- Modal de formulario -->
    <CrudForm
      modal-id="presentacionModal"
      title="Presentación"
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
    
    <!-- Modal de confirmación de eliminación -->
    <div class="modal fade" id="deleteModal" tabindex="-1">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Confirmar eliminación</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
          </div>
          <div class="modal-body">
            <p>¿Estás seguro de que deseas eliminar la presentación <strong>{{ itemToDelete?.nombre }}</strong>?</p>
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
import { presentacionesApi } from '../api/presentaciones'

export default {
  name: 'PresentacionView',
  components: {
    CrudTable,
    CrudForm
  },
  setup() {
    const presentaciones = ref([])
    const loading = ref(false)
    const formLoading = ref(false)
    const selectedItem = ref(null)
    const itemToDelete = ref(null)
    const formErrors = ref({})
    
    // Paginación y búsqueda
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
    
    const loadPresentaciones = async (page = currentPage.value) => {
      try {
        loading.value = true
        const params = {
          page,
          size: pageSize.value
        }
        
        if (searchTerm.value.trim()) {
          params.q = searchTerm.value.trim()
        }
        
        const response = await presentacionesApi.getAll(params)
        
        if (response.success) {
          presentaciones.value = response.data.items
          totalItems.value = response.data.total
          currentPage.value = response.data.page
        }
      } catch (error) {
        console.error('Error cargando presentaciones:', error)
      } finally {
        loading.value = false
      }
    }
    
    const debouncedSearch = () => {
      clearTimeout(searchTimeout)
      searchTimeout = setTimeout(() => {
        currentPage.value = 1
        loadPresentaciones()
      }, 500)
    }
    
    const goToPage = (page) => {
      if (page >= 1 && page <= totalPages.value) {
        loadPresentaciones(page)
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
      const modal = new bootstrap.Modal(document.getElementById('presentacionModal'))
      modal.show()
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
          response = await presentacionesApi.update(selectedItem.value.id, updateData)
        } else {
          // Modo creación: enviar todos los datos del formulario
          response = await presentacionesApi.create(formData)
        }
        
        if (response.success) {
          // Cerrar modal
          const modal = bootstrap.Modal.getInstance(document.getElementById('presentacionModal'))
          modal.hide()
          
          // Recargar datos
          await loadPresentaciones()
          
          // Mostrar mensaje de éxito
          alert(response.message)
        }
      } catch (error) {
        console.error('Error guardando presentación:', error)
        if (error.response?.data?.message) {
          alert(error.response.data.message)
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
        
        const response = await presentacionesApi.delete(itemToDelete.value.id)
        
        if (response.success) {
          // Cerrar modal
          const modal = bootstrap.Modal.getInstance(document.getElementById('deleteModal'))
          modal.hide()
          
          // Recargar datos
          await loadPresentaciones()
          
          alert(response.message)
        }
      } catch (error) {
        console.error('Error eliminando presentación:', error)
        if (error.response?.data?.message) {
          alert(error.response.data.message)
        }
      } finally {
        formLoading.value = false
      }
    }
    
    onMounted(() => {
      loadPresentaciones()
    })
    
    return {
      presentaciones,
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
      loadPresentaciones,
      debouncedSearch,
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

