<template>
  <div class="container-fluid py-4">
    <div class="row">
      <div class="col-12">
        <div class="d-flex justify-content-between align-items-center mb-4">
          <h2 class="h3 mb-0">
            <i class="bi bi-basket me-2"></i>Productos
          </h2>
          <button 
            class="btn btn-warning"
            data-bs-toggle="modal" 
            data-bs-target="#productoModal"
            @click="openCreateModal"
          >
            <i class="bi bi-plus-circle me-2"></i>Nuevo Producto
          </button>
        </div>
        
        <!-- Filtros -->
        <div class="card mb-4">
          <div class="card-body">
            <div class="row g-3">
              <div class="col-md-4">
                <input 
                  type="text" 
                  class="form-control" 
                  placeholder="Buscar por nombre..."
                  v-model="searchTerm"
                  @input="debouncedSearch"
                >
              </div>
              <div class="col-md-2">
                <select class="form-select" v-model="selectedCategoria" @change="loadProductos">
                  <option value="">Todas las categorías</option>
                  <option v-for="categoria in categorias" :key="categoria.id" :value="categoria.id">
                    {{ categoria.nombre }}
                  </option>
                </select>
              </div>
              <div class="col-md-2">
                <select class="form-select" v-model="selectedPresentacion" @change="loadProductos">
                  <option value="">Todas las presentaciones</option>
                  <option v-for="presentacion in presentaciones" :key="presentacion.id" :value="presentacion.id">
                    {{ presentacion.nombre }}
                  </option>
                </select>
              </div>
              <div class="col-md-2">
                <select class="form-select" v-model="pageSize" @change="loadProductos">
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
              :items="productos"
              :columns="columns"
              :loading="loading"
              empty-message="No hay productos registrados"
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
      modal-id="productoModal"
      title="Producto"
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
            maxlength="200"
          >
          <div v-if="errors.nombre" class="invalid-feedback">
            {{ errors.nombre }}
          </div>
        </div>
        
        <div class="row">
          <div class="col-md-6">
            <div class="mb-3">
              <label for="precio" class="form-label">Precio *</label>
              <div class="input-group">
                <span class="input-group-text">$</span>
                <input 
                  type="number" 
                  class="form-control"
                  :class="{ 'is-invalid': errors.precio }"
                  id="precio"
                  v-model="formData.precio"
                  required
                  min="0.01"
                  step="0.01"
                >
              </div>
              <div v-if="errors.precio" class="invalid-feedback">
                {{ errors.precio }}
              </div>
            </div>
          </div>
          <div class="col-md-6">
            <div class="mb-3">
              <label for="activo" class="form-label">Estado</label>
              <select 
                class="form-select"
                id="activo"
                v-model="formData.activo"
              >
                <option :value="true">Activo</option>
                <option :value="false">Inactivo</option>
              </select>
            </div>
          </div>
        </div>
        
        <div class="row">
          <div class="col-md-6">
            <div class="mb-3">
              <label for="categoria_id" class="form-label">Categoría *</label>
              <select 
                class="form-select"
                :class="{ 'is-invalid': errors.categoria_id }"
                id="categoria_id"
                v-model="formData.categoria_id"
                required
              >
                <option value="">Seleccionar categoría</option>
                <option v-for="categoria in categorias" :key="categoria.id" :value="categoria.id">
                  {{ categoria.nombre }}
                </option>
              </select>
              <div v-if="errors.categoria_id" class="invalid-feedback">
                {{ errors.categoria_id }}
              </div>
            </div>
          </div>
          <div class="col-md-6">
            <div class="mb-3">
              <label for="presentacion_id" class="form-label">Presentación *</label>
              <select 
                class="form-select"
                :class="{ 'is-invalid': errors.presentacion_id }"
                id="presentacion_id"
                v-model="formData.presentacion_id"
                required
              >
                <option value="">Seleccionar presentación</option>
                <option v-for="presentacion in presentaciones" :key="presentacion.id" :value="presentacion.id">
                  {{ presentacion.nombre }}
                </option>
              </select>
              <div v-if="errors.presentacion_id" class="invalid-feedback">
                {{ errors.presentacion_id }}
              </div>
            </div>
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
            <p>¿Estás seguro de que deseas eliminar el producto <strong>{{ itemToDelete?.nombre }}</strong>?</p>
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
import { productosApi } from '../api/productos'
import { categoriasApi } from '../api/categorias'
import { presentacionesApi } from '../api/presentaciones'

export default {
  name: 'ProductoView',
  components: {
    CrudTable,
    CrudForm
  },
  setup() {
    const productos = ref([])
    const categorias = ref([])
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
    const selectedCategoria = ref('')
    const selectedPresentacion = ref('')
    let searchTimeout = null
    
    const columns = [
      { key: 'id', label: 'ID' },
      { key: 'nombre', label: 'Nombre' },
      { key: 'precio', label: 'Precio', type: 'currency' },
      { key: 'activo', label: 'Estado', type: 'boolean' },
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
    
    const loadCatalogos = async () => {
      try {
        const [categoriasRes, presentacionesRes] = await Promise.all([
          categoriasApi.getAll({ size: 100 }),
          presentacionesApi.getAll({ size: 100 })
        ])
        
        if (categoriasRes.success) {
          categorias.value = categoriasRes.data.items
        }
        if (presentacionesRes.success) {
          presentaciones.value = presentacionesRes.data.items
        }
      } catch (error) {
        console.error('Error cargando catálogos:', error)
      }
    }
    
    const loadProductos = async (page = currentPage.value) => {
      try {
        loading.value = true
        const params = {
          page,
          size: pageSize.value
        }
        
        if (searchTerm.value.trim()) {
          params.q = searchTerm.value.trim()
        }
        if (selectedCategoria.value) {
          params.categoria_id = selectedCategoria.value
        }
        if (selectedPresentacion.value) {
          params.presentacion_id = selectedPresentacion.value
        }
        
        const response = await productosApi.getAll(params)
        
        if (response.success) {
          productos.value = response.data.items
          totalItems.value = response.data.total
          currentPage.value = response.data.page
        }
      } catch (error) {
        console.error('Error cargando productos:', error)
      } finally {
        loading.value = false
      }
    }
    
    const debouncedSearch = () => {
      clearTimeout(searchTimeout)
      searchTimeout = setTimeout(() => {
        currentPage.value = 1
        loadProductos()
      }, 500)
    }
    
    const goToPage = (page) => {
      if (page >= 1 && page <= totalPages.value) {
        loadProductos(page)
      }
    }
    
    const openCreateModal = () => {
      selectedItem.value = {
        activo: true,
        precio: 0
      }
      formErrors.value = {}
    }
    
    const openEditModal = (item) => {
      // Configurar el item seleccionado para edición
      selectedItem.value = { ...item }
      formErrors.value = {}
      
      // Abrir el modal usando Bootstrap
      const modal = new bootstrap.Modal(document.getElementById('productoModal'))
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
        
        // Convertir valores
        const data = {
          ...formData,
          precio: parseFloat(formData.precio),
          categoria_id: parseInt(formData.categoria_id),
          presentacion_id: parseInt(formData.presentacion_id),
          activo: formData.activo === true || formData.activo === 'true'
        }
        
        let response
        if (selectedItem.value?.id) {
          // Modo edición: enviar solo los campos necesarios para actualización
          const updateData = {
            nombre: data.nombre,
            precio: data.precio,
            categoria_id: data.categoria_id,
            presentacion_id: data.presentacion_id,
            activo: data.activo
          }
          response = await productosApi.update(selectedItem.value.id, updateData)
        } else {
          // Modo creación: enviar todos los datos del formulario
          response = await productosApi.create(data)
        }
        
        if (response.success) {
          // Cerrar modal
          const modal = bootstrap.Modal.getInstance(document.getElementById('productoModal'))
          modal.hide()
          
          // Recargar datos
          await loadProductos()
          
          // Mostrar mensaje de éxito
          alert(response.message)
        }
      } catch (error) {
        console.error('Error guardando producto:', error)
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
        
        const response = await productosApi.delete(itemToDelete.value.id)
        
        if (response.success) {
          // Cerrar modal
          const modal = bootstrap.Modal.getInstance(document.getElementById('deleteModal'))
          modal.hide()
          
          // Recargar datos
          await loadProductos()
          
          alert(response.message)
        }
      } catch (error) {
        console.error('Error eliminando producto:', error)
        if (error.response?.data?.message) {
          alert(error.response.data.message)
        }
      } finally {
        formLoading.value = false
      }
    }
    
    onMounted(async () => {
      await loadCatalogos()
      await loadProductos()
    })
    
    return {
      productos,
      categorias,
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
      selectedCategoria,
      selectedPresentacion,
      loadProductos,
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

