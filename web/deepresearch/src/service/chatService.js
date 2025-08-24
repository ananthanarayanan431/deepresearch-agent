// chatService.js - Service for communicating with Python backend

const API_BASE_URL = process.env.VUE_APP_API_URL || 'http://localhost:5173'

class ChatService {
  constructor() {
    this.baseURL = API_BASE_URL
  }

  // Send message to chatbot backend
  async sendMessage(message) {
    try {
      const response = await fetch(`${this.baseURL}/api/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message: message,
          timestamp: new Date().toISOString()
        })
      })

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }

      const data = await response.json()
      return data
    } catch (error) {
      console.error('Error sending message:', error)
      throw error
    }
  }

  // Get chat history (optional feature)
  async getChatHistory(sessionId = null) {
    try {
      const url = sessionId 
        ? `${this.baseURL}/api/chat/history?session_id=${sessionId}`
        : `${this.baseURL}/api/chat/history`

      const response = await fetch(url, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        }
      })

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }

      const data = await response.json()
      return data
    } catch (error) {
      console.error('Error fetching chat history:', error)
      throw error
    }
  }

  // Clear chat session (optional feature)
  async clearChatSession(sessionId = null) {
    try {
      const response = await fetch(`${this.baseURL}/api/chat/clear`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          session_id: sessionId
        })
      })

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }

      const data = await response.json()
      return data
    } catch (error) {
      console.error('Error clearing chat session:', error)
      throw error
    }
  }

  // Health check for backend connection
  async healthCheck() {
    try {
      const response = await fetch(`${this.baseURL}/api/health`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        }
      })

      return response.ok
    } catch (error) {
      console.error('Health check failed:', error)
      return false
    }
  }
}

// Export singleton instance
export const chatService = new ChatService()

// Export class for testing or multiple instances
export { ChatService }