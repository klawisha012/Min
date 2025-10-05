<script setup>
import { onMounted, onUnmounted } from 'vue'
import MessageList from './components/MessageList.vue'
import ServerStatus from './components/ServerStatus.vue'
import ThemeToggle from './components/ThemeToggle.vue'
import apiService from './services/api.js'

// Check server connection on app start
onMounted(async () => {
  try {
    await apiService.healthCheck()
    console.log('✅ Сервер доступен')
    
    // Initialize WebSocket connection for real-time updates
    try {
      await apiService.connectWebSocket()
      console.log('✅ WebSocket соединение установлено')
    } catch (wsError) {
      console.warn('⚠️ WebSocket недоступен, будут использоваться только ручные обновления:', wsError.message)
    }
  } catch (error) {
    console.warn('⚠️ Сервер недоступен:', error.message)
  }
})

// Cleanup WebSocket connection on app unmount
onUnmounted(() => {
  apiService.disconnectWebSocket()
})
</script>

<template>
  <div class="app">
    <header class="app-header">
      <div class="app-header__content">
        <div class="app-header__title">
          <h1>ESP32 Message Dashboard</h1>
          <p>Мониторинг сообщений от ESP32 устройства</p>
        </div>
        <div class="app-header__actions">
          <div class="app-header__logo">
            <div class="logo-icon">ESP32</div>
          </div>
          <ThemeToggle />
        </div>
      </div>
    </header>

    <main class="app-main">
      <div class="app-container">
        <ServerStatus />
        <MessageList />
      </div>
    </main>
  </div>
</template>

<style scoped>
.app {
  min-height: 100vh;
  background: var(--color-background);
  color: var(--color-text);
  transition: background-color 0.3s ease, color 0.3s ease;
}

.app-header {
  background: var(--color-surface);
  border-bottom: 1px solid var(--color-border);
  padding: 24px 0;
  box-shadow: var(--shadow-sm);
  backdrop-filter: blur(10px);
}

.app-header__content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 24px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.app-header__title h1 {
  margin: 0 0 8px 0;
  color: var(--color-text-primary);
  font-size: 32px;
  font-weight: 700;
  line-height: 1.2;
  letter-spacing: -0.025em;
}

.app-header__title p {
  margin: 0;
  color: var(--color-text-secondary);
  font-size: 16px;
  line-height: 1.5;
}

.app-header__actions {
  display: flex;
  align-items: center;
  gap: 16px;
}

.app-header__logo {
  display: flex;
  align-items: center;
}

.logo-icon {
  font-size: 20px;
  font-weight: 600;
  color: var(--color-primary);
  padding: 8px 12px;
  background: var(--color-primary-light);
  border-radius: 8px;
  border: 1px solid var(--color-primary-border);
}

.app-main {
  padding: 32px 0;
}

.app-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 24px;
}

@media (max-width: 768px) {
  .app-header__content {
    flex-direction: column;
    gap: 20px;
    text-align: center;
  }
  
  .app-header__actions {
    justify-content: center;
  }
  
  .app-header__title h1 {
    font-size: 28px;
  }
  
  .app-header__title p {
    font-size: 15px;
  }
  
  .logo-icon {
    font-size: 18px;
  }
}
</style>
