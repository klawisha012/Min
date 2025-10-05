import { ref, computed, watch } from 'vue'

const THEME_KEY = 'app-theme'
const DARK_THEME = 'dark'
const LIGHT_THEME = 'light'

// Reactive theme state
const currentTheme = ref(localStorage.getItem(THEME_KEY) || LIGHT_THEME)

// Computed properties
const isDark = computed(() => currentTheme.value === DARK_THEME)
const isLight = computed(() => currentTheme.value === LIGHT_THEME)

// Theme toggle function
const toggleTheme = () => {
  currentTheme.value = isDark.value ? LIGHT_THEME : DARK_THEME
}

// Set specific theme
const setTheme = (theme) => {
  if (theme === DARK_THEME || theme === LIGHT_THEME) {
    currentTheme.value = theme
  }
}

// Watch for theme changes and update localStorage and document
watch(currentTheme, (newTheme) => {
  localStorage.setItem(THEME_KEY, newTheme)
  document.documentElement.setAttribute('data-theme', newTheme)
}, { immediate: true })

// Initialize theme on load
document.documentElement.setAttribute('data-theme', currentTheme.value)

export function useTheme() {
  return {
    currentTheme: computed(() => currentTheme.value),
    isDark,
    isLight,
    toggleTheme,
    setTheme
  }
}
