<template>
  <div class="message-list">
    <div class="message-list__header">
      <h2 class="message-list__title">
        Сообщения ESP32
        <span class="message-list__count">({{ totalCount }})</span>
      </h2>
      <div class="message-list__controls">
        <button 
          @click="clearAllMessages" 
          class="btn btn--danger"
          :disabled="isLoading || messages.length === 0"
        >
          Очистить все
        </button>
      </div>
    </div>

    <div class="message-list__filters">
      <div class="search-box">
        <input 
          v-model="searchQuery" 
          @input="handleSearch"
          type="text" 
          placeholder="Поиск по сообщениям..."
          class="search-box__input"
        >
        <button 
          v-if="searchQuery" 
          @click="clearSearch" 
          class="search-box__clear"
        >
          ✕
        </button>
      </div>
      
      <div class="pagination-controls">
        <button 
          @click="loadPreviousPage" 
          :disabled="offset === 0 || isLoading"
          class="btn btn--secondary btn--small"
        >
          ← Предыдущая
        </button>
        <span class="pagination-info">
          {{ offset + 1 }}-{{ Math.min(offset + limit, totalCount) }} из {{ totalCount }}
        </span>
        <button 
          @click="loadNextPage" 
          :disabled="offset + limit >= totalCount || isLoading"
          class="btn btn--secondary btn--small"
        >
          Следующая →
        </button>
      </div>
    </div>

    <div class="message-list__content">
      <div v-if="isLoading" class="loading">
        <div class="loading__spinner"></div>
        <p>Загрузка сообщений...</p>
      </div>
      
      <div v-else-if="messages.length === 0" class="empty-state">
        <div class="empty-state__icon">
          <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
            <polyline points="14,2 14,8 20,8"/>
            <line x1="16" y1="13" x2="8" y2="13"/>
            <line x1="16" y1="17" x2="8" y2="17"/>
            <polyline points="10,9 9,9 8,9"/>
          </svg>
        </div>
        <h3>Нет сообщений</h3>
        <p>Сообщения от ESP32 будут отображаться здесь</p>
      </div>
      
      <div v-else class="messages">
        <MessageCard 
          v-for="message in messages" 
          :key="message.id"
          :message="message"
          :is-latest="message.id === latestMessageId"
          @message-deleted="handleMessageDeleted"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import MessageCard from './MessageCard.vue'
import apiService from '../services/api.js'

const messages = ref([])
const totalCount = ref(0)
const isLoading = ref(false)
const searchQuery = ref('')
const searchResults = ref([])
const isSearching = ref(false)
const offset = ref(0)
const limit = ref(10)
const latestMessageId = ref(null)

const loadMessages = async (resetOffset = false) => {
  if (resetOffset) {
    offset.value = 0
  }
  
  isLoading.value = true
  
  try {
    const response = await apiService.getMessages(limit.value, offset.value)
    messages.value = response.messages || []
    totalCount.value = response.total_count || 0
    
    // Update latest message ID
    if (messages.value.length > 0) {
      latestMessageId.value = messages.value[messages.value.length - 1].id
    }
  } catch (error) {
    console.error('Ошибка загрузки сообщений:', error)
    alert('Ошибка при загрузке сообщений: ' + error.message)
  } finally {
    isLoading.value = false
  }
}

const handleSearch = async () => {
  if (!searchQuery.value.trim()) {
    isSearching.value = false
    searchResults.value = []
    return
  }
  
  isSearching.value = true
  
  try {
    const response = await apiService.searchMessages(searchQuery.value, 50)
    searchResults.value = response.messages || []
  } catch (error) {
    console.error('Ошибка поиска:', error)
    alert('Ошибка при поиске: ' + error.message)
  }
}

const clearSearch = () => {
  searchQuery.value = ''
  isSearching.value = false
  searchResults.value = []
}


const clearAllMessages = async () => {
  if (!confirm('Удалить все сообщения? Это действие нельзя отменить.')) {
    return
  }
  
  isLoading.value = true
  
  try {
    await apiService.clearAllMessages()
    messages.value = []
    totalCount.value = 0
    latestMessageId.value = null
  } catch (error) {
    console.error('Ошибка очистки сообщений:', error)
    alert('Ошибка при очистке сообщений: ' + error.message)
  } finally {
    isLoading.value = false
  }
}

const loadNextPage = () => {
  if (offset.value + limit.value < totalCount.value) {
    offset.value += limit.value
    loadMessages()
  }
}

const loadPreviousPage = () => {
  if (offset.value > 0) {
    offset.value = Math.max(0, offset.value - limit.value)
    loadMessages()
  }
}

const handleMessageDeleted = (messageId) => {
  messages.value = messages.value.filter(msg => msg.id !== messageId)
  totalCount.value = Math.max(0, totalCount.value - 1)
}

// WebSocket connection and real-time updates
let unsubscribeWebSocket = null

const handleNewMessage = (data) => {
  if (data.type === 'new_message' && data.message) {
    // Add new message to the beginning of the list
    messages.value.unshift(data.message)
    
    // Update total count
    totalCount.value += 1
    
    // Update latest message ID
    latestMessageId.value = data.message.id
    
    // If we have more messages than the limit, remove the last one
    if (messages.value.length > limit.value) {
      messages.value.pop()
    }
  }
}

onMounted(async () => {
  // Load initial messages
  await loadMessages()
  
  // Connect to WebSocket for real-time updates
  try {
    await apiService.connectWebSocket()
    unsubscribeWebSocket = apiService.subscribeToMessages(handleNewMessage)
    console.log('✅ WebSocket connected for real-time updates')
  } catch (error) {
    console.warn('⚠️ WebSocket connection failed, using manual refresh only:', error.message)
  }
})

onUnmounted(() => {
  // Cleanup WebSocket connection
  if (unsubscribeWebSocket) {
    unsubscribeWebSocket()
  }
  apiService.disconnectWebSocket()
})
</script>

<style scoped>
.message-list {
  max-width: 1200px;
  margin: 0 auto;
  padding: var(--space-lg);
}

.message-list__header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--space-lg);
  padding-bottom: var(--space-md);
  border-bottom: 2px solid var(--color-border);
}

.message-list__title {
  margin: 0;
  color: var(--color-text-primary);
  font-size: 28px;
  font-weight: 600;
  line-height: 1.2;
  letter-spacing: -0.025em;
}

.message-list__count {
  color: var(--color-text-secondary);
  font-weight: 400;
  font-size: 20px;
}

.message-list__controls {
  display: flex;
  gap: var(--space-sm);
}

.message-list__filters {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--space-lg);
  gap: var(--space-md);
}

.search-box {
  position: relative;
  flex: 1;
  max-width: 400px;
}

.search-box__input {
  width: 100%;
  padding: 12px 16px;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  font-size: 14px;
  background: var(--color-surface);
  color: var(--color-text);
  transition: all 0.2s ease;
}

.search-box__input:focus {
  outline: none;
  border-color: var(--color-primary);
  box-shadow: 0 0 0 3px var(--color-primary-light);
}

.search-box__clear {
  position: absolute;
  right: 8px;
  top: 50%;
  transform: translateY(-50%);
  background: none;
  border: none;
  color: var(--color-text-muted);
  cursor: pointer;
  padding: 4px;
  border-radius: var(--radius-sm);
  transition: all 0.2s ease;
}

.search-box__clear:hover {
  background: var(--color-surface-hover);
  color: var(--color-text);
}

.pagination-controls {
  display: flex;
  align-items: center;
  gap: var(--space-sm);
}

.pagination-info {
  color: var(--color-text-secondary);
  font-size: 14px;
  white-space: nowrap;
}

.message-list__content {
  min-height: 200px;
}

.loading {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 40px;
  color: var(--color-text-secondary);
}

.loading__spinner {
  width: 32px;
  height: 32px;
  border: 3px solid var(--color-border);
  border-top: 3px solid var(--color-primary);
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 16px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.empty-state {
  text-align: center;
  padding: 60px 20px;
  color: var(--color-text-secondary);
}

.empty-state__icon {
  color: var(--color-text-muted);
  margin-bottom: 16px;
}

.empty-state__icon svg {
  width: 48px;
  height: 48px;
}

.empty-state h3 {
  margin: 0 0 8px 0;
  color: var(--color-text-primary);
  font-size: 20px;
  font-weight: 600;
}

.empty-state p {
  margin: 0;
  font-size: 15px;
  color: var(--color-text-secondary);
}

.messages {
  display: flex;
  flex-direction: column;
  gap: var(--space-sm);
}

.btn {
  padding: 10px 18px;
  border: none;
  border-radius: var(--radius-md);
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  display: inline-flex;
  align-items: center;
  gap: 6px;
  text-decoration: none;
}

.btn--primary {
  background: var(--color-primary);
  color: white;
  box-shadow: var(--shadow-sm);
}

.btn--primary:hover:not(:disabled) {
  background: var(--color-primary);
  transform: translateY(-1px);
  box-shadow: var(--shadow-md);
}

.btn--secondary {
  background: var(--color-surface);
  color: var(--color-text);
  border: 1px solid var(--color-border);
}

.btn--secondary:hover:not(:disabled) {
  background: var(--color-surface-hover);
  border-color: var(--color-text-muted);
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
  padding: 8px 14px;
  font-size: 13px;
}

.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none !important;
}

@media (max-width: 768px) {
  .message-list__header {
    flex-direction: column;
    align-items: flex-start;
    gap: 16px;
  }
  
  .message-list__filters {
    flex-direction: column;
    align-items: stretch;
  }
  
  .pagination-controls {
    justify-content: center;
  }
}
</style>
