// chatService.js - Service for communicating with Python backend

const API_BASE_URL = 'http://localhost:8000'
const REQUEST_TIMEOUT = 600000 // 10 minutes timeout for deep research
const HEALTH_CHECK_TIMEOUT = 5000 // 5 seconds for health checks

class ChatService {
  constructor() {
    this.baseURL = API_BASE_URL
    this.currentThreadId = null // Track current conversation thread
    console.log('ChatService initialized with URL:', this.baseURL)
  }

  // Helper method for fetch with timeout and better error handling
  async fetchWithTimeout(url, options, timeout = REQUEST_TIMEOUT) {
    const controller = new AbortController()
    const timeoutId = setTimeout(() => controller.abort(), timeout)
    
    // Ensure headers are properly set
    const defaultOptions = {
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
      },
      mode: 'cors', // Explicitly set CORS mode
      credentials: 'omit', // Don't send credentials for now
    }
    
    const mergedOptions = {
      ...defaultOptions,
      ...options,
      headers: {
        ...defaultOptions.headers,
        ...options.headers
      },
      signal: controller.signal
    }
    
    console.log('Making request to:', url, 'with options:', mergedOptions)
    
    try {
      const response = await fetch(url, mergedOptions)
      clearTimeout(timeoutId)
      
      console.log('Response status:', response.status, 'OK:', response.ok)
      
      if (!response.ok) {
        const errorText = await response.text()
        console.error('Response error:', errorText)
        throw new Error(`HTTP ${response.status}: ${errorText || 'Request failed'}`)
      }
      
      return response
    } catch (error) {
      clearTimeout(timeoutId)
      console.error('Fetch error:', error)
      
      if (error.name === 'AbortError') {
        throw new Error('Request timeout - server took too long to respond')
      }
      
      if (error.message.includes('Failed to fetch') || error.message.includes('NetworkError')) {
        throw new Error('Network error - unable to connect to server. Please check if the server is running.')
      }
      
      throw error
    }
  }

  // Validate input parameters
  validateMessage(message) {
    if (!message || typeof message !== 'string' || message.trim().length === 0) {
      throw new Error('Message must be a non-empty string')
    }
  }

  validateThreadId(threadId) {
    if (threadId !== null && (typeof threadId !== 'string' || threadId.trim().length === 0)) {
      throw new Error('Thread ID must be null or a non-empty string')
    }
  }

  // Send message to chatbot backend with extended timeout for research
  async sendMessage(message, threadId = null) {
    try {
      // Validate inputs
      this.validateMessage(message)
      this.validateThreadId(threadId)

      // Use provided threadId or current one
      const requestThreadId = threadId || this.currentThreadId

      console.log('Sending message:', message, 'with threadId:', requestThreadId)

      // Create payload matching backend expectations
      const requestBody = {
        message: message.trim()
      }

      // Only include thread_id if it exists (not null/undefined)
      if (requestThreadId) {
        requestBody.thread_id = requestThreadId
      }

      console.log('Request body:', requestBody)
      console.log('Starting research request... This may take up to 10 minutes.')

      // Use extended timeout for chat requests (10 minutes)
      const response = await this.fetchWithTimeout(`${this.baseURL}/chat`, {
        method: 'POST',
        body: JSON.stringify(requestBody)
      }, REQUEST_TIMEOUT) // 10 minutes timeout

      const data = await response.json()
      console.log('Research completed! Response data:', data)
      
      // Update current thread ID from response
      if (data.thread_id) {
        this.currentThreadId = data.thread_id
      }
      
      return {
        message: data.response,
        response: data.response, // Ensure both fields are available
        threadId: data.thread_id,
        isFollowup: data.is_followup || false,
        report: data.report
      }
    } catch (error) {
      console.error('Error sending message:', error)
      
      // Provide more specific error messages
      if (error.message.includes('timeout')) {
        throw new Error('Research request timed out. The analysis may be taking longer than expected. Please try a more specific question or try again.')
      }
      
      throw error
    }
  }

  // Get current thread ID
  getCurrentThreadId() {
    return this.currentThreadId
  }

  // Set thread ID (useful for resuming conversations)
  setThreadId(threadId) {
    this.validateThreadId(threadId)
    this.currentThreadId = threadId
  }

  // Start new conversation (reset thread)
  startNewConversation() {
    this.currentThreadId = null
    console.log('Started new conversation')
  }

  // Health check for backend connection
  async healthCheck() {
    try {
      console.log('Performing health check...')
      
      const response = await this.fetchWithTimeout(`${this.baseURL}/health`, {
        method: 'GET'
      }, HEALTH_CHECK_TIMEOUT) // Use shorter timeout for health checks

      console.log('Health check response:', response.ok)
      return response.ok
    } catch (error) {
      console.error('Health check failed:', error)
      return false
    }
  }

  // Alternative health check using test endpoint
  async testConnection() {
    try {
      console.log('Testing connection...')
      
      const response = await this.fetchWithTimeout(`${this.baseURL}/test`, {
        method: 'GET'
      }, HEALTH_CHECK_TIMEOUT)

      console.log('Connection test response:', response.ok)
      return response.ok
    } catch (error) {
      console.error('Connection test failed:', error)
      return false
    }
  }

  // Alternative health check using chat endpoint with a simple message
  async healthCheckWithChat() {
    try {
      console.log('Health check with chat...')
      
      const response = await this.fetchWithTimeout(`${this.baseURL}/chat`, {
        method: 'POST',
        body: JSON.stringify({
          message: "health check",
          thread_id: null
        })
      }, HEALTH_CHECK_TIMEOUT)

      console.log('Health check with chat response:', response.ok)
      return response.ok
    } catch (error) {
      console.error('Health check with chat failed:', error)
      return false
    }
  }

  // Get chat history (if your backend supports it in the future)
  async getChatHistory(sessionId = null) {
    try {
      const url = sessionId 
        ? `${this.baseURL}/chat/history?session_id=${encodeURIComponent(sessionId)}`
        : `${this.baseURL}/chat/history`

      const response = await this.fetchWithTimeout(url, {
        method: 'GET'
      })

      const data = await response.json()
      return data
    } catch (error) {
      console.error('Error fetching chat history:', error)
      throw error
    }
  }

  // Clear chat session
  async clearChatSession() {
    try {
      // Reset local thread ID
      this.startNewConversation()
      
      // If you add a clear endpoint to your backend later, use it here
      // For now, just reset the local state
      return { success: true, message: "Chat session cleared locally" }
    } catch (error) {
      console.error('Error clearing chat session:', error)
      throw error
    }
  }

  // Test method to verify payload structure
  async testPayload() {
    console.log('Testing payload structure...')
    
    // Test 1: New conversation (no thread_id)
    const newConversationPayload = {
      message: "Test message for new conversation"
    }
    console.log('New conversation payload:', newConversationPayload)
    
    // Test 2: Continuing conversation (with thread_id)
    const continuingPayload = {
      thread_id: "test-thread-id",
      message: "Test message for continuing conversation"
    }
    console.log('Continuing conversation payload:', continuingPayload)
    
    return {
      newConversation: newConversationPayload,
      continuing: continuingPayload
    }
  }
}

// Export singleton instance
export const chatService = new ChatService()

// Export class for testing or multiple instances
export { ChatService }