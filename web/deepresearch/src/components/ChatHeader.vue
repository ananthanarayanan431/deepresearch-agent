<template>
  <header class="bg-white/95 backdrop-blur-xl shadow-xl border-b border-gray-200/50 px-6 py-5 sticky top-0 z-50">
    <div class="max-w-6xl mx-auto flex items-center justify-between">
      <!-- Logo/Title with enhanced styling -->
      <div class="flex items-center space-x-4">
        <div class="relative">
          <div class="w-12 h-12 bg-gradient-to-br from-emerald-500 via-blue-500 to-purple-600 rounded-xl flex items-center justify-center shadow-xl transform transition-all duration-300 hover:scale-110 hover:shadow-2xl">
            <svg class="w-7 h-7 text-white" fill="currentColor" viewBox="0 0 24 24">
              <path d="M12 2C6.48 2 2 6.48 2 12c0 5.52 4.48 10 10 10s10-4.48 10-10S17.52 2 12 2zm-1 17.93c-3.94-.49-7-3.85-7-7.93 0-.62.08-1.21.21-1.79L9 15v1c0 1.1.9 2 2 2v1.93zm6.9-2.54c-.26-.81-1-1.39-1.9-1.39h-1v-3c0-.55-.45-1-1-1H8v-2h2c.55 0 1-.45 1-1V7h2c1.1 0 2-.9 2-2v-.41c2.93 1.19 5 4.06 5 7.41 0 2.08-.8 3.97-2.1 5.39z"/>
            </svg>
          </div>
          <!-- Enhanced pulse animation for active state -->
          <div v-if="isConnected" class="absolute -inset-1 bg-gradient-to-br from-green-400 to-emerald-400 rounded-xl opacity-20 animate-ping"></div>
          <div v-if="isConnected" class="absolute -inset-0.5 bg-gradient-to-br from-green-400 to-emerald-400 rounded-xl opacity-30 animate-pulse"></div>
        </div>
        <div class="space-y-1">
          <h1 class="text-2xl font-bold bg-gradient-to-r from-gray-800 via-blue-600 to-purple-600 bg-clip-text text-transparent">
            AI Research Assistant
          </h1>
          <div class="flex items-center space-x-2">
            <p class="text-sm text-gray-600 font-medium">Deep Research & Analysis Platform</p>
            <div class="px-2 py-0.5 bg-gradient-to-r from-blue-100 to-purple-100 text-blue-700 rounded-full text-xs font-semibold border border-blue-200">
              v2.0
            </div>
          </div>
        </div>
      </div>

      <!-- Enhanced Status and Controls -->
      <div class="flex items-center space-x-6">
        <!-- Enhanced Status Indicator with more info -->
        <div class="flex items-center space-x-3 px-4 py-2 rounded-full bg-gradient-to-r from-gray-50 to-blue-50 border border-gray-200 shadow-sm">
          <div class="relative">
            <div :class="statusClass" class="w-3 h-3 rounded-full transition-all duration-300 shadow-sm"></div>
            <!-- Enhanced pulse animation for connected state -->
            <div v-if="isConnected" :class="statusClass" class="absolute inset-0 rounded-full animate-ping opacity-40"></div>
          </div>
          <div class="flex items-center space-x-2">
            <span class="text-sm font-semibold transition-colors duration-300" :class="statusTextClass">
              {{ statusText }}
            </span>
            <div v-if="isConnected" class="flex items-center space-x-1 text-xs text-green-600">
              <svg class="w-3 h-3" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"/>
              </svg>
              <span class="font-medium">Ready</span>
            </div>
          </div>
        </div>

        <!-- Research capabilities indicator -->
        <div class="hidden md:flex items-center space-x-2 px-3 py-2 bg-gradient-to-r from-purple-50 to-blue-50 rounded-lg border border-purple-200">
          <div class="w-5 h-5 bg-gradient-to-r from-purple-500 to-blue-500 rounded-md flex items-center justify-center">
            <svg class="w-3 h-3 text-white" fill="currentColor" viewBox="0 0 20 20">
              <path d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
            </svg>
          </div>
          <div class="text-xs">
            <div class="font-semibold text-purple-700">AI Powered</div>
            <div class="text-purple-600">Research Engine</div>
          </div>
        </div>

        <!-- Settings/Menu with enhanced dropdown -->
        <div class="relative">
          <button 
            @click="toggleMenu"
            class="p-2.5 rounded-xl hover:bg-gray-100 transition-all duration-200 group relative"
            :class="{ 'bg-gray-100': showMenu }"
          >
            <svg class="w-5 h-5 text-gray-600 group-hover:text-gray-800 transition-colors" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 5v.01M12 12v.01M12 19v.01M12 6a1 1 0 110-2 1 1 0 010 2zm0 7a1 1 0 110-2 1 1 0 010 2zm0 7a1 1 0 110-2 1 1 0 010 2z"/>
            </svg>
            
            <!-- Dropdown Menu -->
            <div v-if="showMenu" class="absolute right-0 top-full mt-2 w-64 bg-white rounded-xl shadow-2xl border border-gray-200 py-2 z-50" @click.stop>
              <div class="px-4 py-2 border-b border-gray-100">
                <h3 class="text-sm font-semibold text-gray-800">Research Tools</h3>
                <p class="text-xs text-gray-600">Advanced AI capabilities</p>
              </div>
              
              <div class="py-1">
                <button class="w-full flex items-center space-x-3 px-4 py-2 text-sm text-gray-700 hover:bg-gray-50 transition-colors">
                  <svg class="w-4 h-4 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"/>
                  </svg>
                  <div class="flex-1 text-left">
                    <div class="font-medium">Market Analysis</div>
                    <div class="text-xs text-gray-500">Industry trends & insights</div>
                  </div>
                </button>
                
                <button class="w-full flex items-center space-x-3 px-4 py-2 text-sm text-gray-700 hover:bg-gray-50 transition-colors">
                  <svg class="w-4 h-4 text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"/>
                  </svg>
                  <div class="flex-1 text-left">
                    <div class="font-medium">Company Research</div>
                    <div class="text-xs text-gray-500">Deep business analysis</div>
                  </div>
                </button>
                
                <button class="w-full flex items-center space-x-3 px-4 py-2 text-sm text-gray-700 hover:bg-gray-50 transition-colors">
                  <svg class="w-4 h-4 text-purple-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"/>
                  </svg>
                  <div class="flex-1 text-left">
                    <div class="font-medium">Competitive Intelligence</div>
                    <div class="text-xs text-gray-500">Competitor analysis</div>
                  </div>
                </button>
              </div>
              
              <div class="border-t border-gray-100 mt-2 pt-2">
                <button class="w-full flex items-center space-x-3 px-4 py-2 text-sm text-gray-700 hover:bg-gray-50 transition-colors">
                  <svg class="w-4 h-4 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z"/>
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/>
                  </svg>
                  <span>Settings</span>
                </button>
                
                <button class="w-full flex items-center space-x-3 px-4 py-2 text-sm text-gray-700 hover:bg-gray-50 transition-colors">
                  <svg class="w-4 h-4 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8.228 9c.549-1.165 2.03-2 3.772-2 2.21 0 4 1.343 4 3 0 1.4-1.278 2.575-3.006 2.907-.542.104-.994.54-.994 1.093m0 3h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
                  </svg>
                  <span>Help & Support</span>
                </button>
              </div>
            </div>
          </button>
        </div>
      </div>
    </div>
  </header>
</template>

<script setup>
import { computed, ref, onMounted, onUnmounted } from 'vue'

const props = defineProps({
  isConnected: {
    type: Boolean,
    default: true
  }
})

const showMenu = ref(false)

const statusClass = computed(() => {
  return props.isConnected 
    ? 'bg-green-500 shadow-green-500/50 shadow-md' 
    : 'bg-red-500 shadow-red-500/50 shadow-md'
})

const statusText = computed(() => {
  return props.isConnected ? 'Online' : 'Offline'
})

const statusTextClass = computed(() => {
  return props.isConnected ? 'text-green-700' : 'text-red-700'
})

const toggleMenu = () => {
  showMenu.value = !showMenu.value
}

const closeMenu = (event) => {
  if (showMenu.value) {
    showMenu.value = false
  }
}

onMounted(() => {
  document.addEventListener('click', closeMenu)
})

onUnmounted(() => {
  document.removeEventListener('click', closeMenu)
})
</script>

<style scoped>
/* Enhanced gradient text support */
.bg-clip-text {
  background-clip: text;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

/* Smooth dropdown animation */
@keyframes slideDown {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.absolute.right-0 {
  animation: slideDown 0.2s ease-out;
}
</style>