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
  --primary-color: #4a6fa5;
  --secondary-color: #166088;
  --background-color: #f5f7fa;
  --surface-color: #ffffff;
  --text-color: #333333;
  --text-secondary: #666666;
  --border-color: #dddddd;
  --success-color: #28a745;
  --error-color: #dc3545;
  --shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  --transition: all 0.3s ease;
}

[data-theme="dark"] {
  --primary-color: #6b9bd9;
  --secondary-color: #4a7bb8;
  --background-color: #121212;
  --surface-color: #1e1e1e;
  --text-color: #e0e0e0;
  --text-secondary: #a0a0a0;
  --border-color: #333333;
  --shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
}

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

body {
  background-color: var(--background-color);
  color: var(--text-color);
  transition: var(--transition);
  min-height: 100vh;
}

#app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}
</style>
