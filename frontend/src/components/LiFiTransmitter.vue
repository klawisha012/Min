<script setup>
import { ref, computed } from 'vue'

// Props
const props = defineProps({
  isDarkTheme: {
    type: Boolean,
    default: false
  }
})

// Emits
const emit = defineEmits(['toggle-theme'])

// Reactive data
const message = ref('')
const isLoading = ref(false)
const statusMessage = ref('')
const statusType = ref('')

// Computed properties
const themeIcon = computed(() => props.isDarkTheme ? '☀️' : '🌙')
const themeText = computed(() => props.isDarkTheme ? 'Светлая тема' : 'Темная тема')
const isMessageEmpty = computed(() => !message.value.trim())

// Methods
const toggleTheme = () => {
  emit('toggle-theme')
}

const showStatus = (message, type) => {
  statusMessage.value = message
  statusType.value = type
}

const sendMessage = async () => {
  if (isMessageEmpty.value) {
    showStatus('Пожалуйста, введите сообщение для отправки', 'error')
    return
  }
  
  isLoading.value = true
  statusMessage.value = ''
  
  try {
    const response = await fetch('http://localhost:8000/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        text: message.value
      })
    })
    
    if (response.ok) {
      const result = await response.json()
      showStatus(`Сообщение успешно отправлено! Отправлено байт: ${result.sent_bytes.length}`, 'success')
      message.value = '' // Очищаем поле ввода
    } else {
      throw new Error(`Ошибка сервера: ${response.status}`)
    }
  } catch (error) {
    console.error('Ошибка при отправке:', error)
    showStatus(`Не удалось отправить сообщение: ${error.message}`, 'error')
  } finally {
    isLoading.value = false
  }
}
</script>

<template>
  <div class="container">
    <header>
      <h1>Li-Fi Data Transmitter</h1>
      <button class="theme-toggle" @click="toggleTheme">
        <span>{{ themeIcon }}</span>
        <span>{{ themeText }}</span>
      </button>
    </header>

    <section class="intro">
      <p>Li-Fi (Light Fidelity) — это технология беспроводной связи, использующая видимый свет для передачи данных. Отправьте сообщение ниже, и оно будет преобразовано в световые импульсы и передано на Arduino через COM-порт.</p>
    </section>

    <section class="card">
      <h2>Отправка данных</h2>
      <div class="form-group">
        <label for="messageInput">Введите текст для отправки через Li-Fi:</label>
        <textarea 
          id="messageInput" 
          v-model="message"
          placeholder="Введите ваше сообщение здесь..."
        ></textarea>
      </div>
      <button 
        class="btn" 
        @click="sendMessage"
        :disabled="isLoading || isMessageEmpty"
      >
        <span>Отправить через Li-Fi</span>
        <div class="loading" v-show="isLoading"></div>
      </button>
      
      <div 
        class="status" 
        :class="statusType"
        v-if="statusMessage"
      >
        {{ statusMessage }}
      </div>
    </section>

    <section class="info-section">
      <h3>О технологии Li-Fi</h3>
      <div class="info-grid">
        <div class="info-item">
          <h4>Скорость передачи</h4>
          <p>Li-Fi может достигать скорости до 100 Гбит/с, что значительно быстрее Wi-Fi.</p>
        </div>
        <div class="info-item">
          <h4>Безопасность</h4>
          <p>Свет не проникает через стены, что делает Li-Fi более безопасным для передачи данных.</p>
        </div>
        <div class="info-item">
          <h4>Применение</h4>
          <p>Используется в больницах, самолетах, подводных лодках и других чувствительных к радиоволнам средах.</p>
        </div>
        <div class="info-item">
          <h4>Энергоэффективность</h4>
          <p>Li-Fi использует существующие светодиодные лампы, что делает его энергоэффективным.</p>
        </div>
      </div>
    </section>
  </div>

  <footer>
    <p>Li-Fi Data Transmitter &copy; 2025 | Технология будущего уже здесь</p>
  </footer>
</template>

<style scoped>
.container {
  max-width: 800px;
  margin: 0 auto;
  padding: 2rem;
}

header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid var(--border-color);
}

h1 {
  color: var(--primary-color);
  font-size: 2rem;
}

.theme-toggle {
  background: var(--surface-color);
  border: 1px solid var(--border-color);
  color: var(--text-color);
  padding: 0.5rem 1rem;
  border-radius: 20px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  transition: var(--transition);
}

.theme-toggle:hover {
  background: var(--primary-color);
  color: white;
}

.intro {
  margin-bottom: 2rem;
  line-height: 1.6;
}

.card {
  background: var(--surface-color);
  border-radius: 10px;
  padding: 2rem;
  box-shadow: var(--shadow);
  margin-bottom: 2rem;
}

.form-group {
  margin-bottom: 1.5rem;
}

label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
}

textarea {
  width: 100%;
  padding: 1rem;
  border: 1px solid var(--border-color);
  border-radius: 8px;
  background: var(--background-color);
  color: var(--text-color);
  resize: vertical;
  min-height: 120px;
  font-size: 1rem;
  transition: var(--transition);
}

textarea:focus {
  outline: none;
  border-color: var(--primary-color);
  box-shadow: 0 0 0 2px rgba(74, 111, 165, 0.2);
}

.btn {
  background: var(--primary-color);
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
  font-size: 1rem;
  cursor: pointer;
  transition: var(--transition);
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
}

.btn:hover {
  background: var(--secondary-color);
  transform: translateY(-2px);
}

.btn:disabled {
  background: var(--text-secondary);
  cursor: not-allowed;
  transform: none;
}

.status {
  margin-top: 1.5rem;
  padding: 1rem;
  border-radius: 8px;
  display: none;
}

.status.success {
  background: rgba(40, 167, 69, 0.1);
  border: 1px solid var(--success-color);
  color: var(--success-color);
  display: block;
}

.status.error {
  background: rgba(220, 53, 69, 0.1);
  border: 1px solid var(--error-color);
  color: var(--error-color);
  display: block;
}

.info-section {
  margin-top: 2rem;
}

.info-section h3 {
  margin-bottom: 1rem;
  color: var(--primary-color);
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 1rem;
}

.info-item {
  background: var(--surface-color);
  padding: 1rem;
  border-radius: 8px;
  border-left: 4px solid var(--primary-color);
}

.info-item h4 {
  margin-bottom: 0.5rem;
}

.info-item p {
  font-size: 0.9rem;
  color: var(--text-secondary);
}

footer {
  margin-top: auto;
  text-align: center;
  padding: 1.5rem;
  color: var(--text-secondary);
  font-size: 0.9rem;
  border-top: 1px solid var(--border-color);
}

.loading {
  display: none;
  width: 20px;
  height: 20px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-radius: 50%;
  border-top-color: white;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

@media (max-width: 600px) {
  .container {
    padding: 1rem;
  }
  
  h1 {
    font-size: 1.5rem;
  }
  
  .info-grid {
    grid-template-columns: 1fr;
  }
}
</style>
