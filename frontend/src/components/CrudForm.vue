<template>
  <div class="modal fade" :id="modalId" tabindex="-1" ref="modal">
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">
            {{ isEdit ? `Editar ${title}` : `Crear ${title}` }}
          </h5>
          <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
        </div>
        <div class="modal-body">
          <form @submit.prevent="handleSubmit">
            <slot :formData="formData" :errors="errors" :loading="loading">
              <!-- Contenido del formulario será proporcionado por el slot -->
            </slot>
          </form>
        </div>
        <div class="modal-footer">
          <button 
            type="button" 
            class="btn btn-secondary" 
            data-bs-dismiss="modal"
            :disabled="loading"
          >
            Cancelar
          </button>
          <button 
            type="button" 
            class="btn btn-primary" 
            @click="handleSubmit"
            :disabled="loading"
          >
            <span v-if="loading" class="loading-spinner me-2"></span>
            {{ isEdit ? 'Actualizar' : 'Crear' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, watch } from 'vue'

export default {
  name: 'CrudForm',
  props: {
    modalId: {
      type: String,
      required: true
    },
    title: {
      type: String,
      required: true
    },
    item: {
      type: Object,
      default: null
    },
    loading: {
      type: Boolean,
      default: false
    },
    errors: {
      type: Object,
      default: () => ({})
    }
  },
  emits: ['submit', 'close'],
  setup(props, { emit }) {
    const modal = ref(null)
    const formData = ref({})
    
    const isEdit = computed(() => !!props.item?.id)
    
            // Observar cambios en el item para actualizar formData automáticamente
        watch(() => props.item, (newItem) => {
          if (newItem) {
            // Si hay un item, copiar sus datos al formulario (modo edición)
            formData.value = { ...newItem }
          } else {
            // Si no hay item, limpiar el formulario (modo creación)
            formData.value = {}
          }
        }, { immediate: true, deep: true })
        
        const handleSubmit = () => {
          // Emitir evento de envío con los datos del formulario
          emit('submit', formData.value)
        }
    
    const resetForm = () => {
      formData.value = {}
      emit('close')
    }
    
    return {
      modal,
      formData,
      isEdit,
      handleSubmit,
      resetForm
    }
  }
}
</script>

