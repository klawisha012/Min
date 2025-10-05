<template>
  <div class="message-card" :class="{ 'message-card--latest': isLatest }">
    <div class="message-card__header">
      <div class="message-card__id">#{{ message.id }}</div>
      <div class="message-card__source">{{ message.source }}</div>
      <div class="message-card__actions">
        <button 
          @click="deleteMessage" 
          class="btn btn--danger btn--small"
          :disabled="isDeleting"
        >
          {{ isDeleting ? 'Удаление...' : 'Удалить' }}
        </button>
      </div>
    </div>
    
    <div class="message-card__content">
      <p class="message-card__text">{{ message.message }}</p>
    </div>
    
    <div class="message-card__footer">
      <div class="message-card__timestamps">
        <div class="timestamp" v-if="message.client_timestamp">
          <span class="timestamp__label">Клиент:</span>
          <span class="timestamp__value">{{ formatTimestamp(message.client_timestamp) }}</span>
        </div>
        <div class="timestamp">
          <span class="timestamp__label">Сервер:</span>
          <span class="timestamp__value">{{ formatTimestamp(message.server_timestamp) }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import apiService from '../services/api.js'

const props = defineProps({
  message: {
    type: Object,
    required: true
  },
  isLatest: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['message-deleted'])

const isDeleting = ref(false)

const formatTimestamp = (timestamp) => {
  if (!timestamp) return 'N/A'
  const date = new Date(timestamp)
  return date.toLocaleString('ru-RU', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit'
  })
}

const deleteMessage = async () => {
  if (!confirm(`Удалить сообщение #${props.message.id}?`)) {
    return
  }
  
  isDeleting.value = true
  
  try {
    await apiService.deleteMessage(props.message.id)
    emit('message-deleted', props.message.id)
  } catch (error) {
    console.error('Ошибка удаления сообщения:', error)
    alert('Ошибка при удалении сообщения: ' + error.message)
  } finally {
    isDeleting.value = false
  }
}
</script>

<style scoped>
.message-card {
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  padding: var(--space-md);
  margin-bottom: var(--space-sm);
  box-shadow: var(--shadow-sm);
  transition: all 0.2s ease;
}

.message-card:hover {
  box-shadow: var(--shadow-md);
  transform: translateY(-1px);
  border-color: var(--color-text-muted);
}

.message-card--latest {
  border-left: 4px solid var(--color-success);
  background: var(--color-success-light);
}

.message-card__header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.message-card__id {
  font-weight: 600;
  color: var(--color-text-primary);
  font-size: 14px;
}

.message-card__source {
  background: var(--color-surface-hover);
  color: var(--color-text-secondary);
  padding: 4px 8px;
  border-radius: var(--radius-sm);
  font-size: 12px;
  font-weight: 500;
}

.message-card__actions {
  display: flex;
  gap: 8px;
}

.message-card__content {
  margin-bottom: 12px;
}

.message-card__text {
  margin: 0;
  color: var(--color-text);
  line-height: 1.6;
  font-size: 15px;
}

.message-card__footer {
  border-top: 1px solid var(--color-border);
  padding-top: 12px;
}

.message-card__timestamps {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.timestamp {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 12px;
}

.timestamp__label {
  color: var(--color-text-secondary);
  font-weight: 500;
  min-width: 60px;
}

.timestamp__value {
  color: var(--color-text);
  font-family: 'Courier New', monospace;
}

.btn {
  padding: 6px 12px;
  border: none;
  border-radius: var(--radius-sm);
  font-size: 12px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn--danger {
  background: var(--color-error);
  color: white;
  box-shadow: var(--shadow-sm);
}

.btn--danger:hover:not(:disabled) {
  background: var(--color-error);
  transform: translateY(-1px);
  box-shadow: var(--shadow-md);
}

.btn--small {
  padding: 4px 8px;
  font-size: 11px;
}

.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

@media (max-width: 640px) {
  .message-card__header {
    flex-direction: column;
    align-items: flex-start;
    gap: 8px;
  }
  
  .message-card__actions {
    width: 100%;
    justify-content: flex-end;
  }
  
  .message-card__timestamps {
    flex-direction: column;
  }
}
</style>
