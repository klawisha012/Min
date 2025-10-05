<script setup>
import { ref, onMounted } from 'vue'
import LiFiTransmitter from './components/LiFiTransmitter.vue'

// Theme management
const isDarkTheme = ref(false)

const toggleTheme = () => {
  isDarkTheme.value = !isDarkTheme.value
  document.body.setAttribute('data-theme', isDarkTheme.value ? 'dark' : 'light')
  localStorage.setItem('theme', isDarkTheme.value ? 'dark' : 'light')
}

onMounted(() => {
  const savedTheme = localStorage.getItem('theme')
  if (savedTheme === 'dark') {
    isDarkTheme.value = true
    document.body.setAttribute('data-theme', 'dark')
  }
})
</script>

<template>
  <div id="app">
    <LiFiTransmitter :is-dark-theme="isDarkTheme" @toggle-theme="toggleTheme" />
  </div>
</template>

<style>
:root {
  --primary-color: #00d4ff;
  --secondary-color: #0099cc;
  --accent-color: #ff6b35;
  --light-blue: #87ceeb;
  --electric-blue: #00bfff;

  --input-bg: rgba(0, 0, 0, 0.27);
  
  --surface-color: rgba(255, 255, 255, 0.05);
  --glass-surface: rgba(255, 255, 255, 0.1);
  --text-color: #ffffff;
  --text-secondary: #b0b0b0;
  --border-color: rgba(0, 212, 255, 0.3);
  --success-color: #00ff88;
  --error-color: #ff4757;
  --shadow: 0 8px 32px rgba(0, 212, 255, 0.2);
  --glow: 0 0 20px rgba(0, 212, 255, 0.5);
  --transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  --gradient-primary: linear-gradient(135deg, #00d4ff 0%, #0099cc 50%, #ff6b35 100%);
  --gradient-bg: radial-gradient(ellipse at center, rgba(32, 32, 32, 0.66) 0%, rgba(0, 0, 0, 0.9) 90%);
}

[data-theme="light"] {
  --primary-color: #0066cc;
  --secondary-color: #004499;
  --accent-color: #ff4500;
  --light-blue: #4a90e2;
  --electric-blue: #007acc;
  /*--background-color: #f8fafc;*/
  --input-bg: #f8fafc;
  --surface-color: rgba(255, 255, 255, 0.8);
  --glass-surface: rgba(255, 255, 255, 0.9);
  --text-color: #1a1a1a;
  --text-secondary: #4a5568;
  --border-color: rgba(0, 102, 204, 0.3);
  --success-color: #00aa44;
  --error-color: #cc0000;
  --shadow: 0 8px 32px rgba(0, 102, 204, 0.15);
  --glow: 0 0 20px rgba(0, 102, 204, 0.3);
  --gradient-primary: linear-gradient(135deg, #0066cc 0%, #004499 50%, #ff4500 100%);
  --gradient-bg: radial-gradient(ellipse at center, rgba(0, 102, 204, 0.05) 0%, rgba(248, 250, 252, 0.9) 70%);
}

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
  font-family: 'Inter', 'Segoe UI', system-ui, -apple-system, sans-serif;
}

body {
  background: var(--gradient-bg);
  color: var(--text-color);
  transition: var(--transition);
  min-height: 100vh;
  overflow-x: hidden;
  position: relative;
}

body::before {
  content: '';
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: 
    radial-gradient(circle at 20% 80%, rgba(0, 212, 255, 0.1) 0%, transparent 50%),
    radial-gradient(circle at 80% 20%, rgba(255, 107, 53, 0.1) 0%, transparent 50%),
    radial-gradient(circle at 40% 40%, rgba(0, 153, 204, 0.05) 0%, transparent 50%);
  pointer-events: none;
  z-index: -1;
  animation: lightPulse 8s ease-in-out infinite alternate;
}

@keyframes lightPulse {
  0% { opacity: 0.3; }
  100% { opacity: 0.7; }
}

#app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  position: relative;
  z-index: 1;
}

/* Световые частицы */
.light-particles {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  z-index: 0;
}

.light-particle {
  position: absolute;
  width: 3px;
  height: 3px;
  background: var(--primary-color);
  border-radius: 50%;
  animation: float 6s linear infinite;
  box-shadow: 0 0 8px var(--primary-color);
  opacity: 0.8;
}

[data-theme="light"] .light-particle {
  background: var(--primary-color);
  box-shadow: 0 0 10px var(--primary-color);
  opacity: 0.9;
}

@keyframes float {
  0% {
    transform: translateY(100vh) translateX(0);
    opacity: 0;
  }
  10% {
    opacity: 1;
  }
  90% {
    opacity: 1;
  }
  100% {
    transform: translateY(-100vh) translateX(100px);
    opacity: 0;
  }
}
</style>