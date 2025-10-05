// API service for communicating with FastAPI backend
const API_BASE_URL = 'http://localhost:7999'
const WS_BASE_URL = 'ws://localhost:7999'

class ApiService {
  constructor() {
    this.baseURL = API_BASE_URL
    this.wsBaseURL = WS_BASE_URL
    this.wsConnection = null
    this.wsListeners = new Map()
  }

  async request(endpoint, options = {}) {
    const url = `${this.baseURL}${endpoint}`
    const config = {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers
      },
      ...options
    }

    try {
      const response = await fetch(url, config)
      
      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}))
        throw new Error(errorData.detail || `HTTP error! status: ${response.status}`)
      }
      
      return await response.json()
    } catch (error) {
      console.error('API request failed:', error)
      throw error
    }
  }

  // Get all messages with pagination
  async getMessages(limit = 50, offset = 0) {
    return this.request(`/api/data?limit=${limit}&offset=${offset}`)
  }

  // Get latest message
  async getLatestMessage() {
    return this.request('/api/data/latest')
  }

  // Get message by ID
  async getMessageById(id) {
    return this.request(`/api/data/${id}`)
  }

  // Get server statistics
  async getStats() {
    return this.request('/api/stats')
  }

  // Search messages
  async searchMessages(query, limit = 20) {
    const encodedQuery = encodeURIComponent(query)
    return this.request(`/api/search?query=${encodedQuery}&limit=${limit}`)
  }

  // Send a test message
  async sendMessage(message, source = 'frontend_test') {
    return this.request('/api/data', {
      method: 'POST',
      body: JSON.stringify({
        message,
        timestamp: new Date().toISOString(),
        source
      })
    })
  }

  // Delete all messages
  async clearAllMessages() {
    return this.request('/api/data', {
      method: 'DELETE'
    })
  }

  // Delete message by ID
  async deleteMessage(id) {
    return this.request(`/api/data/${id}`, {
      method: 'DELETE'
    })
  }

  // Health check
  async healthCheck() {
    return this.request('/health')
  }

  // Get server info
  async getServerInfo() {
    return this.request('/')
  }

  // WebSocket connection methods
  connectWebSocket() {
    if (this.wsConnection && this.wsConnection.readyState === WebSocket.OPEN) {
      return Promise.resolve()
    }

    return new Promise((resolve, reject) => {
      try {
        this.wsConnection = new WebSocket(`${this.wsBaseURL}/ws`)
        
        this.wsConnection.onopen = () => {
          console.log('WebSocket connected')
          resolve()
        }
        
        this.wsConnection.onmessage = (event) => {
          try {
            const data = JSON.parse(event.data)
            this.handleWebSocketMessage(data)
          } catch (error) {
            console.error('Error parsing WebSocket message:', error)
          }
        }
        
        this.wsConnection.onclose = () => {
          console.log('WebSocket disconnected')
          this.wsConnection = null
        }
        
        this.wsConnection.onerror = (error) => {
          console.error('WebSocket error:', error)
          reject(error)
        }
      } catch (error) {
        reject(error)
      }
    })
  }

  disconnectWebSocket() {
    if (this.wsConnection) {
      this.wsConnection.close()
      this.wsConnection = null
    }
  }

  handleWebSocketMessage(data) {
    // Notify all listeners about the new message
    this.wsListeners.forEach((callback) => {
      try {
        callback(data)
      } catch (error) {
        console.error('Error in WebSocket listener:', error)
      }
    })
  }

  // Subscribe to WebSocket messages
  subscribeToMessages(callback) {
    const id = Date.now() + Math.random()
    this.wsListeners.set(id, callback)
    
    // Return unsubscribe function
    return () => {
      this.wsListeners.delete(id)
    }
  }

  // Send message via WebSocket
  sendWebSocketMessage(message) {
    if (this.wsConnection && this.wsConnection.readyState === WebSocket.OPEN) {
      this.wsConnection.send(JSON.stringify(message))
    } else {
      console.warn('WebSocket not connected')
    }
  }
}

// Create and export a singleton instance
export const apiService = new ApiService()
export default apiService
