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
    <!-- Световые частицы -->
    <div class="light-particles">
      <div 
        v-for="n in 20" 
        :key="n" 
        class="light-particle"
        :style="{
          left: Math.random() * 100 + '%',
          animationDelay: Math.random() * 6 + 's',
          animationDuration: (Math.random() * 3 + 4) + 's'
        }"
      ></div>
    </div>

    <header class="header-glow">
      <div class="title-container">
        <h1 class="main-title">
          <span class="title-text">Li-Fi</span>
          <span class="title-subtitle">Data Transmitter</span>
        </h1>
        <div class="light-beam"></div>
      </div>
      <button class="theme-toggle" @click="toggleTheme">
        <div class="theme-icon">{{ themeIcon }}</div>
        <span class="theme-text">{{ themeText }}</span>
        <div class="theme-glow"></div>
      </button>
    </header>

    <section class="card glass-card">
      <div class="card-header">
        <h2 class="card-title">
          Отправка данных
        </h2>
        <div class="signal-waves">
          <div class="wave"></div>
          <div class="wave"></div>
          <div class="wave"></div>
        </div>
      </div>
      
      <div class="form-group">
        <label for="messageInput" class="form-label">
          Введите текст для отправки через Li-Fi:
        </label>
        <div class="textarea-container">
          <textarea 
            id="messageInput" 
            v-model="message"
            placeholder="Введите ваше сообщение здесь..."
            class="message-input"
          ></textarea>
          <div class="input-glow"></div>
        </div>
      </div>
      
      <button 
        class="btn send-btn" 
        @click="sendMessage"
        :disabled="isLoading || isMessageEmpty"
      >
        <span class="btn-text">
          Отправить через Li-Fi
        </span>
        <div class="btn-glow"></div>
        <div class="loading" v-show="isLoading">
          <div class="loading-spinner"></div>
        </div>
      </button>
      
      <div 
        class="status" 
        :class="statusType"
        v-if="statusMessage"
      >
        <div class="status-icon">
          <span v-if="statusType === 'success'">✅</span>
          <span v-else>❌</span>
        </div>
        <span class="status-text">{{ statusMessage }}</span>
      </div>
    </section>
  </div>

  <footer class="footer-glow">
    <div class="footer-content">
      <p class="footer-text">
        <span class="footer-icon">⚡</span>
        Li-Fi Data Transmitter &copy; 2025 | Технология будущего уже здесь
      </p>
      <div class="footer-lights">
        <div class="footer-light"></div>
        <div class="footer-light"></div>
        <div class="footer-light"></div>
      </div>
    </div>
  </footer>
</template>

<style scoped>
.container {
  max-width: 1000px;
  width: 100%;
  margin: 0 auto;

  position: relative;
  z-index: 2;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

/* Header Styles */
.header-glow {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
  padding: 1rem 0;
  position: relative;
}

.title-container {
  position: relative;
}

.main-title {
  font-size: 2.2rem;
  font-weight: 800;
  margin: 0;
  position: relative;
  z-index: 2;
}

.title-text {
  background: var(--gradient-primary);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  display: block;
  text-shadow: 0 0 30px rgba(0, 212, 255, 0.5);
  animation: titleGlow 3s ease-in-out infinite alternate;
}

.title-subtitle {
  display: block;
  font-size: 1rem;
  color: var(--text-secondary);
  margin-top: 0.25rem;
  font-weight: 400;
}

@keyframes titleGlow {
  0% { filter: brightness(1); }
  100% { filter: brightness(1.2); }
}

.light-beam {
  position: absolute;
  top: 50%;
  left: -20px;
  width: 4px;
  height: 60px;
  background: linear-gradient(to bottom, transparent, var(--primary-color), transparent);
  transform: translateY(-50%);
  animation: beamPulse 2s ease-in-out infinite;
  box-shadow: 0 0 20px var(--primary-color);
}

@keyframes beamPulse {
  0%, 100% { opacity: 0.3; transform: translateY(-50%) scaleY(0.8); }
  50% { opacity: 1; transform: translateY(-50%) scaleY(1.2); }
}

.theme-toggle {
  background: var(--glass-surface);
  backdrop-filter: blur(10px);
  border: 1px solid var(--border-color);
  color: var(--text-color);
  padding: 0.75rem 1.5rem;
  border-radius: 25px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.75rem;
  transition: var(--transition);
  position: relative;
  overflow: hidden;
  font-weight: 500;
}

.theme-toggle:hover {
  background: var(--primary-color);
  color: white;
  transform: translateY(-2px);
  box-shadow: var(--glow);
}

.theme-icon {
  font-size: 1.2rem;
  transition: var(--transition);
}

.theme-glow {
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
  transition: left 0.5s;
}

.theme-toggle:hover .theme-glow {
  left: 100%;
}

/* Intro Styles */
.intro-glow {
  margin-bottom: 1.5rem;
  position: relative;
}

.intro-content {
  background: var(--glass-surface);
  backdrop-filter: blur(15px);
  border: 1px solid var(--border-color);
  border-radius: 15px;
  padding: 1.25rem;
  position: relative;
  overflow: hidden;
}

.intro-content::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 2px;
  background: var(--gradient-primary);
  animation: borderGlow 3s ease-in-out infinite;
}

@keyframes borderGlow {
  0%, 100% { opacity: 0.5; }
  50% { opacity: 1; }
}

.light-bulb {
  font-size: 1.5rem;
  display: inline-block;
  margin-right: 0.75rem;
  animation: bulbFlicker 4s ease-in-out infinite;
}

@keyframes bulbFlicker {
  0%, 90%, 100% { opacity: 1; }
  5%, 85% { opacity: 0.8; }
}

.intro-content p {
  line-height: 1.6;
  font-size: 1rem;
  margin: 0;
}

/* Card Styles */
.glass-card {
  background: var(--glass-surface);
  backdrop-filter: blur(20px);
  border: 1px solid var(--border-color);
  border-radius: 15px;
  padding: 1.5rem;
  box-shadow: var(--shadow);
  margin-bottom: 1.5rem;
  position: relative;
  overflow: hidden;
}

.glass-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(135deg, rgba(0, 212, 255, 0.1) 0%, rgba(255, 107, 53, 0.05) 100%);
  pointer-events: none;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.25rem;
  position: relative;
  z-index: 2;
  min-height: 30px;
}

.card-title {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 1.3rem;
  font-weight: 700;
  color: var(--text-color);
  margin: 0;
}

.title-icon {
  font-size: 1.5rem;
  animation: iconPulse 2s ease-in-out infinite;
}

@keyframes iconPulse {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.1); }
}

.signal-waves {
  display: flex;
  gap: 0.5rem;
}

.wave {
  width: 4px;
  height: 20px;
  background: var(--primary-color);
  border-radius: 2px;
  animation: waveAnimation 1.5s ease-in-out infinite;
}

.wave:nth-child(2) { animation-delay: 0.2s; }
.wave:nth-child(3) { animation-delay: 0.4s; }

@keyframes waveAnimation {
  0%, 100% { height: 10px; opacity: 0.5; }
  50% { height: 30px; opacity: 1; }
}

/* Form Styles */
.form-group {
  margin-bottom: 1.25rem;
  position: relative;
  z-index: 2;
}

.form-label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 1rem;
  font-weight: 600;
  color: var(--text-color);
  font-size: 1.1rem;
}

.label-icon {
  font-size: 1.2rem;
}

.textarea-container {
  position: relative;
}

.message-input {
  width: 100%;
  padding: 1rem;
  border: 2px solid var(--border-color);
  border-radius: 12px;
    
  background-color: var(--input-bg);
  color: var(--text-color);

  resize: vertical;
  min-height: 100px;
  font-size: 0.95rem;
  transition: var(--transition);
  position: relative;
  z-index: 2;
}

.message-input:focus {
  outline: none;
  border-color: var(--primary-color);
  box-shadow: 0 0 0 4px rgba(0, 212, 255, 0.2);
}

.input-glow {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  border-radius: 15px;
  background: linear-gradient(45deg, var(--primary-color), var(--accent-color));
  opacity: 0;
  transition: opacity 0.3s;
  z-index: 1;
}

.message-input:focus + .input-glow {
  opacity: 0.1;
}

/* Button Styles */
.send-btn {
  background: var(--gradient-primary);
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 12px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: var(--transition);
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  position: relative;
  overflow: hidden;
  box-shadow: var(--shadow);
}

.send-btn:hover:not(:disabled) {
  transform: translateY(-3px);
  box-shadow: var(--glow);
}

.send-btn:disabled {
  background: var(--text-secondary);
  cursor: not-allowed;
  transform: none;
  opacity: 0.6;
}

.btn-text {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  position: relative;
  z-index: 2;
}

.btn-icon {
  font-size: 1.2rem;
  animation: rocketPulse 2s ease-in-out infinite;
}

@keyframes rocketPulse {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.1); }
}

.btn-glow {
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
  transition: left 0.6s;
}

.send-btn:hover:not(:disabled) .btn-glow {
  left: 100%;
}

/* Status Styles */
.status {
  margin-top: 1.25rem;
  padding: 1rem;
  border-radius: 12px;
  display: flex;
  align-items: center;
  gap: 0.75rem;
  position: relative;
  z-index: 2;
  backdrop-filter: blur(10px);
}

.status.success {
  background: rgba(0, 255, 136, 0.1);
  border: 2px solid var(--success-color);
  color: var(--success-color);
}

.status.error {
  background: rgba(255, 71, 87, 0.1);
  border: 2px solid var(--error-color);
  color: var(--error-color);
}

.status-icon {
  font-size: 1.5rem;
}

.status-text {
  font-weight: 500;
}

/* Info Section */
.info-section {
  margin-top: 1.5rem;
  position: relative;
  z-index: 2;
}

.info-title {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 1.25rem;
  font-size: 1.4rem;
  font-weight: 700;
  color: var(--text-color);
}

.info-icon {
  font-size: 1.5rem;
  animation: iconRotate 4s ease-in-out infinite;
}

@keyframes iconRotate {
  0%, 100% { transform: rotate(0deg); }
  50% { transform: rotate(10deg); }
}

.info-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
  max-width: 100%;
}

.info-grid .info-item:nth-child(1),
.info-grid .info-item:nth-child(2) {
  justify-self: start;
}

.info-grid .info-item:nth-child(3),
.info-grid .info-item:nth-child(4) {
  justify-self: end;
}

.info-item {
  background: var(--glass-surface);
  backdrop-filter: blur(15px);
  border: 1px solid var(--border-color);
  border-radius: 12px;
  padding: 1.25rem;
  position: relative;
  overflow: hidden;
  transition: var(--transition);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
}

.info-item:hover {
  transform: translateY(-5px);
  box-shadow: var(--glow);
}

.info-item .info-icon {
  font-size: 2rem;
  display: block;
  margin-bottom: 1rem;
  animation: iconFloat 3s ease-in-out infinite;
}

@keyframes iconFloat {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-5px); }
}

.info-item-title {
  font-size: 1.1rem;
  font-weight: 700;
  margin-bottom: 0.75rem;
  color: var(--text-color);
  line-height: 1.3;
}

.info-item-text {
  font-size: 0.95rem;
  color: var(--text-color);
  line-height: 1.5;
  font-weight: 400;
  opacity: 0.9;
}

.info-glow {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(135deg, rgba(0, 212, 255, 0.05) 0%, rgba(255, 107, 53, 0.05) 100%);
  opacity: 0;
  transition: opacity 0.3s;
  pointer-events: none;
}

.info-item:hover .info-glow {
  opacity: 1;
}

/* Улучшенная читаемость для светлой темы */
[data-theme="light"] .info-item {
  background: rgba(255, 255, 255, 0.95);
  border: 1px solid rgba(0, 102, 204, 0.2);
  box-shadow: 0 4px 25px rgba(0, 102, 204, 0.1);
}

[data-theme="light"] .info-item-title {
  color: #1a1a1a;
  font-weight: 800;
}

[data-theme="light"] .info-item-text {
  color: #2d3748;
  font-weight: 500;
  opacity: 1;
}

[data-theme="light"] .info-item:hover {
  box-shadow: 0 8px 35px rgba(0, 102, 204, 0.2);
  border-color: rgba(0, 102, 204, 0.3);
}

/* Footer */
.footer-glow {
  margin-top: auto;
  text-align: center;
  padding: 1rem;
  position: relative;
  z-index: 2;
}

.footer-content {
  position: relative;
}

.footer-text {
  color: var(--text-secondary);
  font-size: 1rem;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  margin: 0;
}

.footer-icon {
  font-size: 1.2rem;
  animation: lightning 2s ease-in-out infinite;
}

@keyframes lightning {
  0%, 90%, 100% { opacity: 1; }
  5%, 85% { opacity: 0.3; }
}

.footer-lights {
  display: flex;
  justify-content: center;
  gap: 1rem;
  margin-top: 1rem;
}

.footer-light {
  width: 6px;
  height: 6px;
  background: var(--primary-color);
  border-radius: 50%;
  animation: lightBlink 2s ease-in-out infinite;
}

.footer-light:nth-child(2) { animation-delay: 0.5s; }
.footer-light:nth-child(3) { animation-delay: 1s; }

@keyframes lightBlink {
  0%, 50%, 100% { opacity: 0.3; }
  25%, 75% { opacity: 1; }
}

/* Loading Animation */
.loading {
  position: absolute;
  top: 50%;
  right: 1rem;
  transform: translateY(-50%);
}

.loading-spinner {
  width: 20px;
  height: 20px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-radius: 50%;
  border-top-color: white;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* Responsive Design */
@media (max-width: 768px) {
  .container {
    padding: 1rem;
  }
  
  .main-title {
    font-size: 2rem;
  }
  
  .title-subtitle {
    font-size: 1rem;
  }
  
  .glass-card {
    padding: 1.5rem;
  }
  
  .info-grid {
    grid-template-columns: 1fr;
  }
  
  .info-grid .info-item:nth-child(1),
  .info-grid .info-item:nth-child(2),
  .info-grid .info-item:nth-child(3),
  .info-grid .info-item:nth-child(4) {
    justify-self: stretch;
  }
  
  .header-glow {
    flex-direction: column;
    gap: 1rem;
    text-align: center;
  }
}

@media (max-width: 480px) {
  .main-title {
    font-size: 1.5rem;
  }
  
  .card-title {
    font-size: 1.2rem;
  }
  
  .send-btn {
    padding: 0.75rem 1.5rem;
    font-size: 1rem;
  }
}
</style>