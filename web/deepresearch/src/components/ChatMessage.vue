
<template>
  <div :class="messageContainerClass">
    <!-- Avatar (for bot messages) - placed before message -->
    <div v-if="message.sender === 'bot'" class="flex-shrink-0 mr-2">
      <div class="w-8 h-8 bg-blue-500 rounded-full flex items-center justify-center">
        <svg class="w-4 h-4 text-white" fill="currentColor" viewBox="0 0 20 20">
          <path d="M2 5a2 2 0 012-2h7a2 2 0 012 2v4a2 2 0 01-2 2H9l-3 3v-3H4a2 2 0 01-2-2V5z"></path>
        </svg>
      </div>
    </div>

    <!-- Message Bubble -->
    <div :class="messageBubbleClass">
      <!-- Message Content -->
      <p class="text-sm whitespace-pre-wrap break-words">{{ message.text }}</p>
      
      <!-- Timestamp -->
      <div :class="timestampClass">
        {{ formattedTime }}
      </div>
    </div>

    <!-- User Avatar (for user messages) -->
    <div v-if="message.sender === 'user'" class="flex-shrink-0 ml-2">
      <div class="w-8 h-8 bg-gray-400 rounded-full flex items-center justify-center">
        <svg class="w-4 h-4 text-white" fill="currentColor" viewBox="0 0 20 20">
          <path fill-rule="evenodd" d="M10 9a3 3 0 100-6 3 3 0 000 6zm-7 9a7 7 0 1114 0H3z" clip-rule="evenodd"></path>
        </svg>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  message: {
    type: Object,
    required: true,
    validator: (value) => {
      return value && 
             typeof value.text === 'string' && 
             typeof value.sender === 'string' &&
             ['user', 'bot'].includes(value.sender)
    }
  }
})

const isUser = computed(() => props.message.sender === 'user')
const isError = computed(() => props.message.isError === true)

const messageContainerClass = computed(() => {
  return [
    'flex',
    'items-end',
    'space-x-2',
    'mb-4',
    isUser.value ? 'justify-end' : 'justify-start'
  ]
})

const messageBubbleClass = computed(() => {
  const baseClasses = [
    'rounded-lg', 
    'p-3', 
    'max-w-xs', 
    'lg:max-w-md', 
    'shadow-sm',
    'relative'
  ]
  
  if (isError.value) {
    return [
      ...baseClasses, 
      'bg-red-100', 
      'text-red-800', 
      'border', 
      'border-red-200'
    ]
  }
  
  if (isUser.value) {
    return [
      ...baseClasses, 
      'bg-blue-500', 
      'text-white'
    ]
  } else {
    return [
      ...baseClasses, 
      'bg-gray-100', 
      'text-gray-800',
      'border',
      'border-gray-200'
    ]
  }
})

const timestampClass = computed(() => {
  const baseClasses = ['text-xs', 'mt-1', 'opacity-70']
  
  if (isError.value) {
    return [...baseClasses, 'text-red-600']
  }
  
  if (isUser.value) {
    return [...baseClasses, 'text-blue-100']
  } else {
    return [...baseClasses, 'text-gray-500']
  }
})

const formattedTime = computed(() => {
  if (!props.message.timestamp) return ''
  
  try {
    const date = new Date(props.message.timestamp)
    if (isNaN(date.getTime())) return ''
    
    return date.toLocaleTimeString('en-US', {
      hour: '2-digit',
      minute: '2-digit',
      hour12: true
    })
  } catch (error) {
    console.warn('Error formatting timestamp:', error)
    return ''
  }
})
</script>