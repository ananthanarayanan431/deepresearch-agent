<template>
  <div id="app" class="min-h-screen bg-gray-50 flex flex-col">
    <!-- Header -->
    <ChatHeader />
    
    <!-- Main Chat Area -->
    <main class="flex-1 flex flex-col max-w-4xl mx-auto w-full">
      <ChatWindow 
        :messages="messages" 
        :is-loading="isLoading" 
        @clear-chat="clearChat"
      />
      
      <ChatInput 
        @send-message="handleSendMessage"
        :disabled="isLoading"
      />
    </main>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import ChatHeader from './components/ChatHeader.vue'
import ChatWindow from './components/ChatWindow.vue'
import ChatInput from './components/ChatInput.vue'
import { chatService } from './service/chatService.js'

const messages = ref([])
const isLoading = ref(false)

const handleSendMessage = async (messageText) => {
  if (!messageText.trim()) return

  // Add user message
  const userMessage = {
    id: Date.now(),
    text: messageText,
    sender: 'user',
    timestamp: new Date()
  }
  messages.value.push(userMessage)

  try {
    isLoading.value = true
    
    // Send to backend and get response
    const botResponse = await chatService.sendMessage(messageText)
    
    // Add bot response
    const botMessage = {
      id: Date.now() + 1,
      text: botResponse.message,
      sender: 'bot',
      timestamp: new Date()
    }
    messages.value.push(botMessage)
    
  } catch (error) {
    console.error('Error sending message:', error)
    
    // Add error message
    const errorMessage = {
      id: Date.now() + 1,
      text: 'Sorry, I encountered an error. Please try again.',
      sender: 'bot',
      timestamp: new Date(),
      isError: true
    }
    messages.value.push(errorMessage)
  } finally {
    isLoading.value = false
  }
}

const clearChat = () => {
  messages.value = []
}
</script>