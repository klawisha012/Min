<template>
  <button 
    @click="toggleTheme" 
    class="theme-toggle"
    :title="isDark ? 'Переключить на светлую тему' : 'Переключить на темную тему'"
  >
    <svg v-if="isDark" class="theme-toggle__icon" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
      <circle cx="12" cy="12" r="5"/>
      <line x1="12" y1="1" x2="12" y2="3"/>
      <line x1="12" y1="21" x2="12" y2="23"/>
      <line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/>
      <line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/>
      <line x1="1" y1="12" x2="3" y2="12"/>
      <line x1="21" y1="12" x2="23" y2="12"/>
      <line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/>
      <line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/>
    </svg>
    <svg v-else class="theme-toggle__icon" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
      <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/>
    </svg>
  </button>
</template>

<script setup>
import { useTheme } from '../composables/useTheme.js'

const { isDark, toggleTheme } = useTheme()
</script>

<style scoped>
.theme-toggle {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  border: none;
  border-radius: 8px;
  background: var(--color-surface);
  color: var(--color-text);
  cursor: pointer;
  transition: all 0.2s ease;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.theme-toggle:hover {
  background: var(--color-surface-hover);
  transform: translateY(-1px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
}

.theme-toggle:active {
  transform: translateY(0);
}

.theme-toggle__icon {
  transition: transform 0.3s ease;
}

.theme-toggle:hover .theme-toggle__icon {
  transform: rotate(15deg);
}
</style>
