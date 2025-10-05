<template>
  <div class="server-status">
    <div class="server-status__header">
      <h3>Статус сервера</h3>
      <div class="server-status__indicator" :class="statusClass">
        <div class="indicator-dot"></div>
        <span>{{ statusText }}</span>
      </div>
    </div>
    
    <div class="server-status__info" v-if="serverInfo">
      <div class="info-item">
        <span class="info-label">Всего сообщений:</span>
        <span class="info-value">{{ serverInfo.total_messages || 0 }}</span>
      </div>
      <div class="info-item" v-if="serverInfo.first_message_time">
        <span class="info-label">Первое сообщение:</span>
        <span class="info-value">{{ formatTimestamp(serverInfo.first_message_time) }}</span>
      </div>
      <div class="info-item" v-if="serverInfo.last_message_time">
        <span class="info-label">Последнее сообщение:</span>
        <span class="info-value">{{ formatTimestamp(serverInfo.last_message_time) }}</span>
      </div>
      <div class="info-item">
        <span class="info-label">Время работы:</span>
        <span class="info-value">{{ serverInfo.server_uptime || 'running' }}</span>
      </div>
    </div>
    
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import apiService from '../services/api.js'

const serverInfo = ref(null)
const isLoading = ref(false)
const isConnected = ref(false)
const lastCheck = ref(null)

const statusClass = computed(() => ({
  'server-status__indicator--online': isConnected.value,
  'server-status__indicator--offline': !isConnected.value
}))

const statusText = computed(() => {
  if (isLoading.value) return 'Проверка...'
  return isConnected.value ? 'Подключен' : 'Отключен'
})

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

const checkServerStatus = async () => {
  isLoading.value = true
  
  try {
    const [healthResponse, statsResponse] = await Promise.all([
      apiService.healthCheck(),
      apiService.getStats()
    ])
    
    isConnected.value = true
    serverInfo.value = {
      total_messages: statsResponse.statistics.total_messages,
      first_message_time: statsResponse.statistics.first_message_time,
      last_message_time: statsResponse.statistics.last_message_time,
      server_uptime: statsResponse.statistics.server_uptime
    }
    lastCheck.value = new Date()
  } catch (error) {
    console.error('Ошибка проверки статуса сервера:', error)
    isConnected.value = false
    serverInfo.value = null
  } finally {
    isLoading.value = false
  }
}


// Auto-refresh status every 30 seconds
let statusInterval = null

const startStatusRefresh = () => {
  statusInterval = setInterval(checkServerStatus, 30000)
}

const stopStatusRefresh = () => {
  if (statusInterval) {
    clearInterval(statusInterval)
    statusInterval = null
  }
}

onMounted(() => {
  checkServerStatus()
  startStatusRefresh()
})

onUnmounted(() => {
  stopStatusRefresh()
})
</script>

<style scoped>
.server-status {
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  padding: var(--space-lg);
  margin-bottom: var(--space-lg);
  box-shadow: var(--shadow-sm);
}

.server-status__header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.server-status__header h3 {
  margin: 0;
  color: var(--color-text-primary);
  font-size: 20px;
  font-weight: 600;
  line-height: 1.2;
}

.server-status__indicator {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 6px 12px;
  border-radius: 20px;
  font-size: 14px;
  font-weight: 500;
}

.server-status__indicator--online {
  background: var(--color-success-light);
  color: var(--color-success);
}

.server-status__indicator--offline {
  background: var(--color-error-light);
  color: var(--color-error);
}

.indicator-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: currentColor;
}

.server-status__info {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 12px;
  margin-bottom: 16px;
}

.info-item {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.info-label {
  font-size: 12px;
  color: var(--color-text-secondary);
  font-weight: 500;
}

.info-value {
  font-size: 14px;
  color: var(--color-text);
  font-family: 'Courier New', monospace;
}


@media (max-width: 640px) {
  .server-status__header {
    flex-direction: column;
    align-items: flex-start;
    gap: 12px;
  }
  
  .server-status__info {
    grid-template-columns: 1fr;
  }
}
</style>
