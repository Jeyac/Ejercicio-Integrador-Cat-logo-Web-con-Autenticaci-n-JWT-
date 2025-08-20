<template>
  <div class="modern-table-wrapper">
    <div class="table-responsive">
      <table class="table modern-table">
        <thead class="modern-thead">
          <tr>
            <th v-for="column in columns" :key="column.key" class="modern-th">
              <i v-if="column.icon" :class="column.icon + ' me-2'"></i>
              {{ column.label }}
            </th>
            <th class="modern-th text-center">Acciones</th>
          </tr>
        </thead>
        <tbody>
          <tr v-if="loading" class="loading-row">
            <td :colspan="columns.length + 1" class="text-center py-5">
              <div class="modern-loading">
                <div class="loading-spinner-modern"></div>
                <div class="loading-text">Cargando datos...</div>
                <div class="loading-dots">
                  <span></span>
                  <span></span>
                  <span></span>
                </div>
              </div>
            </td>
          </tr>
          <tr v-else-if="items.length === 0" class="empty-row">
            <td :colspan="columns.length + 1" class="text-center py-5">
              <div class="empty-state">
                <i class="bi bi-inbox empty-icon"></i>
                <div class="empty-text">{{ emptyMessage || 'No hay datos para mostrar' }}</div>
                <div class="empty-subtitle">Los datos aparecerán aquí cuando estén disponibles</div>
              </div>
            </td>
          </tr>
          <tr v-else v-for="(item, index) in items" :key="item.id" class="modern-row" :style="{ animationDelay: (index * 0.1) + 's' }">
          <td v-for="column in columns" :key="column.key">
            <span v-if="column.type === 'boolean'">
              <span v-if="item[column.key]" class="badge bg-success">Activo</span>
              <span v-else class="badge bg-secondary">Inactivo</span>
            </span>
            <span v-else-if="column.type === 'currency'">
              ${{ formatCurrency(item[column.key]) }}
            </span>
            <span v-else-if="column.type === 'date'">
              {{ formatDate(item[column.key]) }}
            </span>
            <span v-else>
              {{ item[column.key] || '-' }}
            </span>
          </td>
            <td>
              <div class="action-buttons">
                <button 
                  class="btn btn-modern btn-edit" 
                  @click="handleEdit(item)"
                  title="Editar"
                >
                  <i class="bi bi-pencil"></i>
                </button>
                <button 
                  class="btn btn-modern btn-delete" 
                  @click="handleDelete(item)"
                  title="Eliminar"
                >
                  <i class="bi bi-trash"></i>
                </button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
export default {
  name: 'CrudTable',
  props: {
    items: {
      type: Array,
      default: () => []
    },
    columns: {
      type: Array,
      required: true
    },
    loading: {
      type: Boolean,
      default: false
    },
    emptyMessage: {
      type: String,
      default: ''
    }
  },
  emits: ['edit', 'delete'],
  methods: {
    formatCurrency(value) {
      if (!value) return '0.00'
      return parseFloat(value).toFixed(2)
    },
    formatDate(value) {
      if (!value) return '-'
      return new Date(value).toLocaleDateString('es-ES')
    },
            handleEdit(item) {
          // Emitir evento de edición con el item seleccionado
          this.$emit('edit', item)
        },
        handleDelete(item) {
          // Emitir evento de eliminación con el item seleccionado
          this.$emit('delete', item)
        }
  }
}
</script>

<style scoped>
.modern-table-wrapper {
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.95), rgba(255, 255, 255, 0.9));
  backdrop-filter: blur(10px);
}

.modern-table {
  margin-bottom: 0;
  background: transparent;
}

.modern-thead {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.modern-th {
  border: none;
  padding: 1.2rem 1rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  font-size: 0.85rem;
  color: white !important;
  position: relative;
}

.modern-th::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 2px;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
}

.modern-row {
  animation: slideInUp 0.6s ease-out both;
  transition: all 0.3s ease;
  border: none;
}

.modern-row:hover {
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.05), rgba(118, 75, 162, 0.05));
  transform: translateY(-2px);
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
}

@keyframes slideInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.modern-row td {
  padding: 1rem;
  border: none;
  border-bottom: 1px solid rgba(0, 0, 0, 0.05);
  vertical-align: middle;
}

/* Estados de carga modernos */
.modern-loading {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
}

.loading-spinner-modern {
  width: 50px;
  height: 50px;
  border: 4px solid rgba(102, 126, 234, 0.2);
  border-top: 4px solid #667eea;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.loading-text {
  color: #6c757d;
  font-weight: 500;
  font-size: 1.1rem;
}

.loading-dots {
  display: flex;
  gap: 0.5rem;
}

.loading-dots span {
  width: 8px;
  height: 8px;
  background: #667eea;
  border-radius: 50%;
  animation: bounce 1.4s ease-in-out infinite both;
}

.loading-dots span:nth-child(1) { animation-delay: -0.32s; }
.loading-dots span:nth-child(2) { animation-delay: -0.16s; }

@keyframes bounce {
  0%, 80%, 100% {
    transform: scale(0);
  } 40% {
    transform: scale(1);
  }
}

/* Estado vacío */
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
  padding: 2rem;
}

.empty-icon {
  font-size: 4rem;
  color: #dee2e6;
  margin-bottom: 1rem;
}

.empty-text {
  color: #6c757d;
  font-size: 1.2rem;
  font-weight: 600;
}

.empty-subtitle {
  color: #adb5bd;
  font-size: 0.9rem;
}

/* Botones de acción modernos */
.action-buttons {
  display: flex;
  gap: 0.5rem;
  justify-content: center;
}

.btn-modern {
  border: none;
  padding: 0.5rem 0.75rem;
  border-radius: 8px;
  transition: all 0.3s ease;
  font-size: 0.9rem;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 36px;
  height: 36px;
}

.btn-edit {
  background: linear-gradient(135deg, #28a745, #20c997);
  color: white;
  box-shadow: 0 2px 8px rgba(40, 167, 69, 0.3);
}

.btn-edit:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(40, 167, 69, 0.4);
  background: linear-gradient(135deg, #20c997, #28a745);
}

.btn-delete {
  background: linear-gradient(135deg, #dc3545, #e74c3c);
  color: white;
  box-shadow: 0 2px 8px rgba(220, 53, 69, 0.3);
}

.btn-delete:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(220, 53, 69, 0.4);
  background: linear-gradient(135deg, #e74c3c, #dc3545);
}

/* Badges mejorados */
.badge {
  font-size: 0.75rem;
  padding: 0.4rem 0.8rem;
  border-radius: 12px;
  font-weight: 600;
}

.bg-success {
  background: linear-gradient(135deg, #28a745, #20c997) !important;
}

.bg-secondary {
  background: linear-gradient(135deg, #6c757d, #adb5bd) !important;
}

/* Responsive */
@media (max-width: 768px) {
  .modern-th,
  .modern-row td {
    padding: 0.75rem 0.5rem;
    font-size: 0.85rem;
  }
  
  .action-buttons {
    flex-direction: column;
    gap: 0.25rem;
  }
  
  .btn-modern {
    font-size: 0.8rem;
    padding: 0.4rem 0.6rem;
    min-width: 32px;
    height: 32px;
  }
  
  .empty-icon {
    font-size: 3rem;
  }
  
  .loading-spinner-modern {
    width: 40px;
    height: 40px;
  }
}
</style>
