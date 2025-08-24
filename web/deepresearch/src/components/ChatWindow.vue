<template>
    <div class="flex-1 flex flex-col p-6">
      <!-- Chat Controls -->
      <div class="flex justify-between items-center mb-4">
        <h2 class="text-lg font-medium text-gray-700">Chat Messages</h2>
        <button
          @click="$emit('clear-chat')"
          class="text-sm text-gray-500 hover:text-gray-700 px-3 py-1 rounded hover:bg-gray-100 transition-colors"
          v-if="messages.length > 0"
        >
          Clear Chat
        </button>
      </div>
  
      <!-- Messages Container -->
      <div 
        ref="messagesContainer"
        class="flex-1 overflow-y-auto space-y-4 bg-white rounded-lg p-4 border border-gray-200 min-h-[400px]"
      >
        <!-- Empty State -->
        <div v-if="messages.length === 0" class="flex flex-col items-center justify-center h-full text-gray-500">
          <svg class="w-16 h-16 mb-4 text-gray-300" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M18 10c0 3.866-3.582 7-8 7a8.841 8.841 0 01-4.083-.98L2 17l1.338-3.123C2.493 12.767 2 11.434 2 10c0-3.866 3.582-7 8-7s8 3.134 8 7zM7 9H5v2h2V9zm8 0h-2v2h2V9zM9 9h2v2H9V9z" clip-rule="evenodd"></path>
          </svg>
          <p class="text-lg font-medium">Start a conversation</p>
          <p class="text-sm">Send a message to begin chatting with the AI assistant</p>
        </div>
  
        <!-- Messages -->
        <ChatMessage
          v-for="message in messages"
          :key="message.id"
          :message="message"
        />
  
        <!-- Loading Indicator -->
        <div v-if="isLoading" class="flex justify-start">
          <div class="bg-gray-100 rounded-lg p-3 max-w-xs">
            <div class="flex space-x-1">
              <div class="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
              <div class="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style="animation-delay: 0.1s"></div>
              <div class="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style="animation-delay: 0.2s"></div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, watch, nextTick } from 'vue'
  import ChatMessage from './ChatMessage.vue'
  
  const props = defineProps({
    messages: {
      type: Array,
      required: true
    },
    isLoading: {
      type: Boolean,
      default: false
    }
  })
  
  defineEmits(['clear-chat'])
  
  const messagesContainer = ref(null)
  
  const scrollToBottom = () => {
    nextTick(() => {
      if (messagesContainer.value) {
        messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
      }
    })
  }
  
  // Watch for new messages and scroll to bottom
  watch(
    () => props.messages.length,
    () => scrollToBottom()
  )
  
  watch(
    () => props.isLoading,
    () => scrollToBottom()
  )
  </script>