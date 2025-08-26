<template>
  <div class="min-h-screen bg-gray-50 flex flex-col">
    <!-- Header -->
    <ChatHeader :isConnected="isConnected" />
    
    <!-- Main Chat Container -->
    <div class="flex-1 flex flex-col max-w-4xl mx-auto w-full">
      <!-- Chat Window -->
      <ChatWindow 
        :messages="messages" 
        :isLoading="isLoading"
        @clear-chat="clearChat"
      />
      
      <!-- Chat Input -->
      <ChatInput 
        :disabled="isLoading"
        @send-message="sendMessage"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import ChatHeader from './components/ChatHeader.vue'
import ChatWindow from './components/ChatWindow.vue'
import ChatInput from './components/ChatInput.vue'
// Import the chatService
import { chatService } from './services/chatService.js'

// Create a simple chat service fallback if needed
const createMockService = () => ({
  sendMessage: async (message) => {
    // Mock delay
    await new Promise(resolve => setTimeout(resolve, 1000))
    return {
      message: `Echo: ${message}`,
      response: `Echo: ${message}`,
      threadId: 'mock-thread',
      isFollowup: false
    }
  },
  healthCheck: async () => false,
  startNewConversation: () => {}
})

// Use chatService or fallback to mock
const activeService = chatService || createMockService()

// State
const messages = ref([])
const isLoading = ref(false)
const isConnected = ref(false)

// Generate unique ID for messages
const generateId = () => {
  return Date.now().toString() + Math.random().toString(36).substr(2, 9)
}

// Send message function
const sendMessage = async (messageText) => {
  if (!messageText.trim()) return

  console.log('Sending message:', messageText)

  // Add user message
  const userMessage = {
    id: generateId(),
    text: messageText,
    sender: 'user',
    timestamp: new Date().toISOString()
  }
  
  messages.value.push(userMessage)
  isLoading.value = true

  // Add a thinking message to show the bot is working
  const thinkingMessage = {
    id: generateId(),
    text: 'I\'m conducting deep research on your question. This may take up to 10 minutes to provide you with a comprehensive analysis...',
    sender: 'bot',
    timestamp: new Date().toISOString(),
    isThinking: true
  }
  messages.value.push(thinkingMessage)

  try {
    const response = await activeService.sendMessage(messageText)
    console.log('Response received:', response)
    
    // Remove the thinking message
    const thinkingIndex = messages.value.findIndex(msg => msg.isThinking)
    if (thinkingIndex !== -1) {
      messages.value.splice(thinkingIndex, 1)
    }
    
    let responseText = response.response || response.message || 'No response received'
    
    if (response.report) {
      responseText = response.report
    }
    
    const botMessage = {
      id: generateId(),
      text: responseText,
      sender: 'bot',
      timestamp: new Date().toISOString(),
      isFollowup: response.isFollowup,
      threadId: response.threadId
    }
    
    messages.value.push(botMessage)
    
  } catch (error) {
    console.error('Error sending message:', error)
    
    // Remove the thinking message
    const thinkingIndex = messages.value.findIndex(msg => msg.isThinking)
    if (thinkingIndex !== -1) {
      messages.value.splice(thinkingIndex, 1)
    }
    
    let errorText = 'Sorry, there was an error. Please try again.'
    
    if (error.message.includes('Failed to fetch')) {
      errorText = 'Unable to connect to server. Check your connection and ensure the server is running.'
    } else if (error.message.includes('timeout')) {
      errorText = 'The research request took too long. Please try a more specific question or check your connection.'
    } else if (error.message.includes('Research request timed out')) {
      errorText = error.message // Use the specific timeout message from chatService
    }
    
    const errorMessage = {
      id: generateId(),
      text: errorText,
      sender: 'bot',
      timestamp: new Date().toISOString(),
      isError: true
    }
    
    messages.value.push(errorMessage)
  } finally {
    isLoading.value = false
  }
}

// Clear chat function
const clearChat = () => {
  messages.value = []
  if (activeService?.startNewConversation) {
    activeService.startNewConversation()
  }
  
  const welcomeMessage = {
    id: generateId(),
    text: 'Hello! I\'m your AI research assistant. How can I help you today?',
    sender: 'bot',
    timestamp: new Date().toISOString()
  }
  
  messages.value.push(welcomeMessage)
}

// Check connection status
const checkConnection = async () => {
  try {
    isConnected.value = await activeService.healthCheck()
    console.log('Connection status:', isConnected.value)
  } catch (error) {
    console.error('Connection check failed:', error)
    isConnected.value = false
  }
}

// Initialize on mount
onMounted(async () => {
  console.log('App mounted')
  
  await checkConnection()
  
  const welcomeMessage = {
    id: generateId(),
    text: 'Hello! I\'m your AI research assistant. I can help you conduct deep research on any topic. What would you like to explore today?',
    sender: 'bot',
    timestamp: new Date().toISOString()
  }
  
  messages.value.push(welcomeMessage)
})
</script>