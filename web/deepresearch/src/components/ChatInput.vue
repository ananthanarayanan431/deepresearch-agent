<template>
    <div class="p-6 bg-white border-t border-gray-200">
      <div class="max-w-4xl mx-auto">
        <div class="flex space-x-4">
          <!-- Text Input -->
          <div class="flex-1">
            <textarea
              ref="textareaRef"
              v-model="messageText"
              @keydown="handleKeyDown"
              @input="adjustHeight"
              :disabled="disabled"
              placeholder="Type your message here..."
              class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 resize-none transition-colors disabled:bg-gray-100 disabled:cursor-not-allowed"
              rows="1"
              :class="{ 'bg-gray-100': disabled }"
            ></textarea>
          </div>
  
          <!-- Send Button -->
          <button
            @click="sendMessage"
            :disabled="disabled || !messageText.trim()"
            class="px-6 py-3 bg-blue-500 text-white rounded-lg hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:bg-gray-300 disabled:cursor-not-allowed transition-colors"
          >
            <svg
              v-if="disabled"
              class="w-5 h-5 animate-spin"
              fill="none"
              viewBox="0 0 24 24"
            >
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 0 1 8-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 0 1 4 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            <svg v-else class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
              <path d="M10.894 2.553a1 1 0 00-1.788 0l-7 14a1 1 0 001.169 1.409l5-1.429A1 1 0 009 15.571V11a1 1 0 112 0v4.571a1 1 0 00.725.962l5 1.428a1 1 0 001.17-1.408l-7-14z"></path>
            </svg>
          </button>
        </div>
  
        <!-- Character Count (optional) -->
        <div class="flex justify-between items-center mt-2">
          <div class="text-xs text-gray-500">
            Press Enter to send, Shift+Enter for new line
          </div>
          <div class="text-xs text-gray-400">
            {{ messageText.length }}/1000
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, nextTick } from 'vue'
  
  const props = defineProps({
    disabled: {
      type: Boolean,
      default: false
    }
  })
  
  const emit = defineEmits(['send-message'])
  
  const messageText = ref('')
  const textareaRef = ref(null)
  
  const sendMessage = () => {
    if (!messageText.value.trim() || props.disabled) return
    
    emit('send-message', messageText.value)
    messageText.value = ''
    
    // Reset textarea height
    nextTick(() => {
      if (textareaRef.value) {
        textareaRef.value.style.height = 'auto'
      }
    })
  }
  
  const handleKeyDown = (event) => {
    if (event.key === 'Enter' && !event.shiftKey) {
      event.preventDefault()
      sendMessage()
    }
  }
  
  const adjustHeight = () => {
    nextTick(() => {
      if (textareaRef.value) {
        textareaRef.value.style.height = 'auto'
        const maxHeight = 120 // Max height in pixels
        const newHeight = Math.min(textareaRef.value.scrollHeight, maxHeight)
        textareaRef.value.style.height = newHeight + 'px'
      }
    })
  }
  </script>