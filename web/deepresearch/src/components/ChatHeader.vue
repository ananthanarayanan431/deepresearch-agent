<template>
    <header class="bg-white shadow-sm border-b border-gray-200 px-6 py-4">
      <div class="max-w-4xl mx-auto flex items-center justify-between">
        <!-- Logo/Title -->
        <div class="flex items-center space-x-3">
          <div class="w-8 h-8 bg-blue-500 rounded-full flex items-center justify-center">
            <svg class="w-5 h-5 text-white" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M18 10c0 3.866-3.582 7-8 7a8.841 8.841 0 01-4.083-.98L2 17l1.338-3.123C2.493 12.767 2 11.434 2 10c0-3.866 3.582-7 8-7s8 3.134 8 7zM7 9H5v2h2V9zm8 0h-2v2h2V9zM9 9h2v2H9V9z" clip-rule="evenodd"></path>
            </svg>
          </div>
          <h1 class="text-xl font-semibold text-gray-800">AI Chatbot</h1>
        </div>
  
        <!-- Status Indicator -->
        <div class="flex items-center space-x-2">
          <div class="flex items-center space-x-1">
            <div :class="statusClass" class="w-2 h-2 rounded-full"></div>
            <span class="text-sm text-gray-600">{{ statusText }}</span>
          </div>
        </div>
      </div>
    </header>
  </template>
  
  <script setup>
  import { computed } from 'vue'
  
  const props = defineProps({
    isConnected: {
      type: Boolean,
      default: true
    }
  })
  
  const statusClass = computed(() => {
    return props.isConnected ? 'bg-green-500' : 'bg-red-500'
  })
  
  const statusText = computed(() => {
    return props.isConnected ? 'Online' : 'Offline'
  })
  </script>