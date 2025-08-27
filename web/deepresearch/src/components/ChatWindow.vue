<template>
  <div class="flex-1 flex flex-col bg-gradient-to-br from-gray-50 via-white to-blue-50/30 backdrop-blur-sm">
    <!-- Enhanced Chat Header with Stats and Controls -->
    <div class="px-6 py-4 bg-white/80 backdrop-blur-xl border-b border-gray-200/60 shadow-sm">
      <div class="flex justify-between items-center">
        <div class="flex items-center space-x-4">
          <div class="flex items-center space-x-3">
            <h2 class="text-xl font-bold bg-gradient-to-r from-gray-800 via-blue-600 to-purple-600 bg-clip-text text-transparent">
              Research Console
            </h2>
            <div class="h-6 w-px bg-gradient-to-b from-transparent via-gray-300 to-transparent"></div>
            <div class="flex items-center space-x-2 text-sm text-gray-600">
              <svg class="w-4 h-4 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"/>
              </svg>
              <span class="font-medium">{{ messageStats.total }} messages</span>
            </div>
          </div>
        </div>
        
        <div class="flex items-center space-x-3">
          <!-- Message Statistics -->
          <div v-if="messages.length > 0" class="hidden md:flex items-center space-x-4 bg-gradient-to-r from-blue-50 to-purple-50 px-4 py-2 rounded-xl border border-blue-200">
            <div class="text-xs text-center">
              <div class="font-semibold text-blue-700">{{ messageStats.research }}</div>
              <div class="text-blue-600">Research</div>
            </div>
            <div class="h-8 w-px bg-blue-200"></div>
            <div class="text-xs text-center">
              <div class="font-semibold text-purple-700">{{ getTotalWords() }}</div>
              <div class="text-purple-600">Words</div>
            </div>
          </div>
          
          <!-- Export Options -->
          <div v-if="messages.length > 0" class="relative">
            <button
              @click="toggleExportMenu"
              class="flex items-center space-x-2 px-3 py-2 bg-gradient-to-r from-green-50 to-emerald-50 hover:from-green-100 hover:to-emerald-100 text-green-700 rounded-xl border border-green-200 hover:border-green-300 transition-all duration-200 shadow-sm hover:shadow-md"
              title="Export conversation"
            >
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
              </svg>
              <span class="text-sm font-medium">Export</span>
            </button>
            
            <!-- Export Dropdown -->
            <div v-if="showExportMenu" class="absolute right-0 top-full mt-2 w-56 bg-white/95 backdrop-blur-lg rounded-xl shadow-2xl border border-gray-200 py-2 z-50">
              <div class="px-4 py-2 border-b border-gray-100">
                <h3 class="text-sm font-semibold text-gray-800">Export Options</h3>
                <p class="text-xs text-gray-600">Download your research session</p>
              </div>
              <div class="py-1">
                <button
                  @click="exportAsPDF"
                  class="w-full flex items-center space-x-3 px-4 py-2 text-sm text-gray-700 hover:bg-gray-50 transition-colors"
                >
                  <svg class="w-4 h-4 text-red-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 21h10a2 2 0 002-2V9.414a1 1 0 00-.293-.707l-5.414-5.414A1 1 0 0012.586 3H7a2 2 0 00-2 2v14a2 2 0 002 2z"/>
                  </svg>
                  <span>Complete Research Report (PDF)</span>
                </button>
                <button
                  @click="exportAsText"
                  class="w-full flex items-center space-x-3 px-4 py-2 text-sm text-gray-700 hover:bg-gray-50 transition-colors"
                >
                  <svg class="w-4 h-4 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
                  </svg>
                  <span>Text Format (.txt)</span>
                </button>
                <button
                  @click="exportAsMarkdown"
                  class="w-full flex items-center space-x-3 px-4 py-2 text-sm text-gray-700 hover:bg-gray-50 transition-colors"
                >
                  <svg class="w-4 h-4 text-purple-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4"/>
                  </svg>
                  <span>Markdown (.md)</span>
                </button>
              </div>
            </div>
          </div>
          
          <!-- Clear Chat Button -->
          <button
            @click="confirmClearChat"
            class="flex items-center space-x-2 px-3 py-2 text-gray-600 hover:text-red-600 hover:bg-red-50 rounded-xl border border-gray-200 hover:border-red-200 transition-all duration-200 shadow-sm hover:shadow-md"
            v-if="messages.length > 0"
            title="Clear conversation"
          >
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/>
            </svg>
            <span class="text-sm font-medium">Clear</span>
          </button>
        </div>
      </div>
    </div>

    <!-- Enhanced Messages Container -->
    <div class="flex-1 relative overflow-hidden">
      <div 
        ref="messagesContainer"
        class="absolute inset-0 overflow-y-auto px-6 py-6 space-y-6 scroll-smooth"
        :class="{'pb-32': isLoading}"
        @scroll="handleScroll"
      >
        <!-- Enhanced Empty State -->
        <div v-if="messages.length === 0" class="flex flex-col items-center justify-center h-full min-h-[500px]">
          <div class="text-center max-w-md">
            <!-- Animated Icon -->
            <div class="relative mb-8">
              <div class="w-24 h-24 bg-gradient-to-br from-blue-500 via-purple-500 to-indigo-600 rounded-3xl flex items-center justify-center shadow-2xl transform transition-all duration-500 hover:scale-110 hover:rotate-3">
                <svg class="w-12 h-12 text-white" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M12 2C6.48 2 2 6.48 2 12c0 5.52 4.48 10 10 10s10-4.48 10-10S17.52 2 12 2zm-1 17.93c-3.94-.49-7-3.85-7-7.93 0-.62.08-1.21.21-1.79L9 15v1c0 1.1.9 2 2 2v1.93zm6.9-2.54c-.26-.81-1-1.39-1.9-1.39h-1v-3c0-.55-.45-1-1-1H8v-2h2c.55 0 1-.45 1-1V7h2c1.1 0 2-.9 2-2v-.41c2.93 1.19 5 4.06 5 7.41 0 2.08-.8 3.97-2.1 5.39z"/>
                </svg>
              </div>
              <!-- Floating particles -->
              <div class="absolute -inset-4">
                <div class="w-3 h-3 bg-blue-400 rounded-full opacity-60 animate-float-1"></div>
                <div class="w-2 h-2 bg-purple-400 rounded-full opacity-60 animate-float-2"></div>
                <div class="w-4 h-4 bg-indigo-400 rounded-full opacity-40 animate-float-3"></div>
              </div>
            </div>
            
            <h3 class="text-2xl font-bold bg-gradient-to-r from-gray-800 via-blue-600 to-purple-600 bg-clip-text text-transparent mb-4">
              Welcome to AI Research Assistant
            </h3>
            <p class="text-gray-600 mb-8 leading-relaxed">
              Start your research journey by asking any question. I'll provide comprehensive analysis, 
              market insights, and detailed reports tailored to your needs.
            </p>
            
            <!-- Suggested Research Topics -->
            <div class="grid grid-cols-1 md:grid-cols-2 gap-3 max-w-2xl mx-auto">
              <div
                v-for="suggestion in welcomeSuggestions"
                :key="suggestion.title"
                @click="sendSuggestion(suggestion.query)"
                class="group p-4 bg-white/80 backdrop-blur-sm border border-gray-200 rounded-2xl hover:border-blue-300 hover:shadow-lg transition-all duration-300 cursor-pointer transform hover:scale-105"
              >
                <div class="flex items-start space-x-3">
                  <div class="w-10 h-10 bg-gradient-to-br from-blue-100 to-purple-100 rounded-xl flex items-center justify-center group-hover:from-blue-200 group-hover:to-purple-200 transition-colors">
                    <svg class="w-5 h-5 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" :d="suggestion.icon"/>
                    </svg>
                  </div>
                  <div class="flex-1 text-left">
                    <h4 class="font-semibold text-gray-800 group-hover:text-blue-800 transition-colors text-sm">
                      {{ suggestion.title }}
                    </h4>
                    <p class="text-xs text-gray-600 mt-1 line-clamp-2">
                      {{ suggestion.description }}
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Messages with Enhanced Styling -->
        <div v-else class="space-y-8">
          <ChatMessage
            v-for="message in messages"
            :key="message.id"
            :message="message"
            @copy-message="handleCopyMessage"
            @regenerate-message="handleRegenerateMessage"
            class="transform transition-all duration-300 hover:scale-[1.01]"
          />
        </div>

        <!-- Enhanced Loading Indicator -->
        <div v-if="isLoading" class="flex justify-start animate-fadeIn">
          <div class="max-w-4xl">
            <div class="flex items-start space-x-4">
              <!-- Bot Avatar -->
              <div class="flex-shrink-0">
                <div class="relative">
                  <div class="w-12 h-12 bg-gradient-to-br from-emerald-500 via-blue-500 to-purple-600 rounded-xl flex items-center justify-center shadow-xl">
                    <svg class="w-6 h-6 text-white animate-pulse" fill="currentColor" viewBox="0 0 24 24">
                      <path d="M12 2C6.48 2 2 6.48 2 12c0 5.52 4.48 10 10 10s10-4.48 10-10S17.52 2 12 2zm-1 17.93c-3.94-.49-7-3.85-7-7.93 0-.62.08-1.21.21-1.79L9 15v1c0 1.1.9 2 2 2v1.93zm6.9-2.54c-.26-.81-1-1.39-1.9-1.39h-1v-3c0-.55-.45-1-1-1H8v-2h2c.55 0 1-.45 1-1V7h2c1.1 0 2-.9 2-2v-.41c2.93 1.19 5 4.06 5 7.41 0 2.08-.8 3.97-2.1 5.39z"/>
                    </svg>
                  </div>
                  <div class="absolute -inset-1 bg-gradient-to-r from-green-400 to-emerald-400 rounded-xl opacity-20 animate-ping"></div>
                </div>
              </div>
              
              <!-- Loading Content -->
              <div class="bg-white/95 backdrop-blur-sm rounded-2xl p-6 shadow-xl border border-gray-200 flex-1">
                <div class="flex items-center justify-between mb-4 pb-3 border-b border-gray-100">
                  <div class="flex items-center space-x-3">
                    <span class="text-sm font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
                      AI Research Assistant
                    </span>
                    <div class="flex space-x-1">
                      <div class="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
                      <div class="w-2 h-2 bg-blue-500 rounded-full animate-pulse" style="animation-delay: 0.1s"></div>
                      <div class="w-2 h-2 bg-purple-500 rounded-full animate-pulse" style="animation-delay: 0.2s"></div>
                    </div>
                  </div>
                </div>
                
                <div class="space-y-4">
                  <div class="flex items-center space-x-3 text-blue-600">
                    <div class="flex space-x-1">
                      <div class="w-3 h-3 bg-current rounded-full animate-bounce"></div>
                      <div class="w-3 h-3 bg-current rounded-full animate-bounce" style="animation-delay: 0.1s"></div>
                      <div class="w-3 h-3 bg-current rounded-full animate-bounce" style="animation-delay: 0.2s"></div>
                    </div>
                    <span class="text-base font-medium">{{ loadingText }}</span>
                  </div>
                  
                  <!-- Research Progress Steps -->
                  <div class="space-y-3 mt-6">
                    <div
                      v-for="(step, index) in researchSteps"
                      :key="index"
                      class="flex items-center space-x-3 transition-all duration-500"
                      :class="step.completed ? 'opacity-100' : 'opacity-50'"
                    >
                      <div class="relative">
                        <div 
                          class="w-6 h-6 rounded-full flex items-center justify-center transition-all duration-300"
                          :class="step.completed ? 'bg-green-500' : step.active ? 'bg-blue-500 animate-pulse' : 'bg-gray-300'"
                        >
                          <svg v-if="step.completed" class="w-3 h-3 text-white" fill="currentColor" viewBox="0 0 20 20">
                            <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/>
                          </svg>
                          <div v-else-if="step.active" class="w-2 h-2 bg-white rounded-full animate-pulse"></div>
                        </div>
                      </div>
                      <span class="text-sm font-medium" :class="step.completed ? 'text-green-700' : step.active ? 'text-blue-700' : 'text-gray-500'">
                        {{ step.text }}
                      </span>
                    </div>
                  </div>
                  
                  <!-- Estimated time remaining -->
                  <div class="mt-6 p-3 bg-gradient-to-r from-blue-50 to-purple-50 rounded-xl border border-blue-200">
                    <div class="flex items-center justify-between text-xs">
                      <span class="text-blue-700 font-medium">Research Progress</span>
                      <span class="text-blue-600">{{ Math.round(loadingProgress) }}% complete</span>
                    </div>
                    <div class="mt-2 w-full bg-blue-100 rounded-full h-2">
                      <div 
                        class="bg-gradient-to-r from-blue-500 to-purple-600 h-2 rounded-full transition-all duration-1000 ease-out relative"
                        :style="{ width: loadingProgress + '%' }"
                      >
                        <div class="absolute inset-0 bg-gradient-to-r from-white/20 to-white/40 animate-pulse rounded-full"></div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <!-- Scroll to Bottom Button -->
      <div 
        v-if="showScrollButton"
        class="absolute bottom-6 right-6 z-10"
      >
        <button
          @click="scrollToBottom"
          class="p-3 bg-white/90 backdrop-blur-lg border border-gray-200 rounded-full shadow-xl hover:shadow-2xl transform hover:scale-110 transition-all duration-300 group"
          title="Scroll to bottom"
        >
          <svg class="w-5 h-5 text-gray-600 group-hover:text-blue-600 transition-colors" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 14l-7 7m0 0l-7-7m7 7V3"/>
          </svg>
        </button>
      </div>
    </div>
    
    <!-- Clear Chat Confirmation Modal -->
    <div v-if="showClearConfirmation" class="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50" @click="showClearConfirmation = false">
      <div class="bg-white rounded-2xl p-6 max-w-md mx-4 shadow-2xl" @click.stop>
        <div class="flex items-center space-x-3 mb-4">
          <div class="w-10 h-10 bg-red-100 rounded-xl flex items-center justify-center">
            <svg class="w-5 h-5 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/>
            </svg>
          </div>
          <div>
            <h3 class="text-lg font-semibold text-gray-800">Clear Conversation</h3>
            <p class="text-sm text-gray-600">This action cannot be undone</p>
          </div>
        </div>
        <p class="text-gray-700 mb-6">
          Are you sure you want to clear all {{ messages.length }} messages? This will permanently delete your research session.
        </p>
        <div class="flex space-x-3">
          <button
            @click="showClearConfirmation = false"
            class="flex-1 px-4 py-2 text-gray-700 bg-gray-100 hover:bg-gray-200 rounded-xl transition-colors"
          >
            Cancel
          </button>
          <button
            @click="clearChat"
            class="flex-1 px-4 py-2 text-white bg-red-500 hover:bg-red-600 rounded-xl transition-colors"
          >
            Clear All
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, nextTick, onMounted, onUnmounted, watch } from 'vue'
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

const emit = defineEmits(['clear-chat', 'send-message', 'copy-message', 'regenerate-message'])

const messagesContainer = ref(null)
const showScrollButton = ref(false)
const showExportMenu = ref(false)
const showClearConfirmation = ref(false)
const loadingProgress = ref(0)
const currentStepIndex = ref(0)

// Loading states
const loadingTexts = [
  "Analyzing your research query...",
  "Gathering relevant information...",
  "Processing market data...",
  "Conducting deep analysis...",
  "Compiling comprehensive report...",
  "Finalizing research findings..."
]
const currentLoadingTextIndex = ref(0)

const loadingText = computed(() => loadingTexts[currentLoadingTextIndex.value])

const researchSteps = ref([
  { text: "Query Analysis", completed: false, active: true },
  { text: "Data Collection", completed: false, active: false },
  { text: "Market Research", completed: false, active: false },
  { text: "Competitive Analysis", completed: false, active: false },
  { text: "Report Generation", completed: false, active: false },
  { text: "Final Review", completed: false, active: false }
])

// Welcome suggestions
const welcomeSuggestions = [
  {
    title: "Market Analysis",
    description: "Comprehensive market research and trends analysis",
    query: "Provide a detailed market analysis for",
    icon: "M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"
  },
  {
    title: "Competitive Intelligence",
    description: "Deep dive into competitor strategies and positioning",
    query: "Analyze the competitive landscape for",
    icon: "M13 10V3L4 14h7v7l9-11h-7z"
  },
  {
    title: "Industry Trends",
    description: "Latest developments and future outlook",
    query: "What are the current trends and future outlook for",
    icon: "M7 12l3-3 3 3 4-4M8 21l4-4 4 4M3 4h18M4 4h16v12a1 1 0 01-1 1H5a1 1 0 01-1-1V4z"
  },
  {
    title: "Investment Analysis",
    description: "Financial performance and investment opportunities",
    query: "Provide an investment analysis and financial overview for",
    icon: "M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
  }
]

// Message statistics
const messageStats = computed(() => {
  const botMessages = props.messages.filter(m => m.sender === 'bot' && !m.isThinking).length
  return {
    total: props.messages.length,
    user: props.messages.filter(m => m.sender === 'user').length,
    research: botMessages
  }
})

// Methods
const getTotalWords = () => {
  return props.messages.reduce((total, message) => {
    if (message.text && !message.isThinking) {
      return total + message.text.split(/\s+/).filter(word => word.length > 0).length
    }
    return total
  }, 0)
}

const scrollToBottom = (smooth = true) => {
  nextTick(() => {
    if (messagesContainer.value) {
      messagesContainer.value.scrollTo({
        top: messagesContainer.value.scrollHeight,
        behavior: smooth ? 'smooth' : 'auto'
      })
    }
  })
}

const handleScroll = () => {
  if (!messagesContainer.value) return
  
  const { scrollTop, scrollHeight, clientHeight } = messagesContainer.value
  const isNearBottom = scrollHeight - scrollTop - clientHeight < 100
  showScrollButton.value = !isNearBottom && props.messages.length > 0
}

const sendSuggestion = (query) => {
  emit('send-message', query)
}

const handleCopyMessage = (message) => {
  emit('copy-message', message)
}

const handleRegenerateMessage = (message) => {
  emit('regenerate-message', message)
}

const confirmClearChat = () => {
  showClearConfirmation.value = true
}

const clearChat = () => {
  emit('clear-chat')
  showClearConfirmation.value = false
}

const toggleExportMenu = () => {
  showExportMenu.value = !showExportMenu.value
}

// Export functions
const exportAsPDF = async () => {
  try {
    const printWindow = window.open('', '_blank')
    if (!printWindow) {
      alert('Please allow popups to download the PDF')
      return
    }
    
    const timestamp = new Date().toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    })
    
    // Compile all bot messages into one report
    const researchContent = props.messages
      .filter(m => m.sender === 'bot' && !m.isThinking && m.text)
      .map(m => m.text)
      .join('\n\n---\n\n')
    
    const htmlContent = `
      <!DOCTYPE html>
      <html>
      <head>
        <title>Complete Research Report - ${timestamp}</title>
        <meta charset="utf-8">
        <style>
          body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.7;
            color: #333;
            max-width: 800px;
            margin: 0 auto;
            padding: 40px 20px;
            background: white;
          }
          .header {
            text-align: center;
            border-bottom: 4px solid #3B82F6;
            padding-bottom: 30px;
            margin-bottom: 40px;
            background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
            padding: 30px;
            border-radius: 15px;
          }
          .header h1 {
            color: #1F2937;
            margin: 0;
            font-size: 28px;
            font-weight: 800;
            background: linear-gradient(135deg, #1F2937 0%, #3B82F6 50%, #8B5CF6 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
          }
          .header .subtitle {
            color: #6B7280;
            margin: 10px 0 0 0;
            font-size: 16px;
            font-weight: 500;
          }
          .header .stats {
            margin-top: 20px;
            display: flex;
            justify-content: center;
            gap: 30px;
            font-size: 14px;
          }
          .stat-item {
            text-align: center;
            padding: 10px 20px;
            background: white;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
          }
          .stat-number {
            font-size: 20px;
            font-weight: bold;
            color: #3B82F6;
          }
          .stat-label {
            color: #6B7280;
            font-size: 12px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
          }
          .content {
            font-size: 15px;
            line-height: 1.8;
          }
                    h1, h2, h3 {
            color: #1F2937;
            margin-top: 35px;
            margin-bottom: 20px;
            font-weight: 700;
          }
          p {
            margin: 10px 0;
            color: #374151;
          }
          pre {
            background: #f3f4f6;
            padding: 15px;
            border-radius: 8px;
            overflow-x: auto;
            font-size: 13px;
          }
          hr {
            margin: 30px 0;
            border: 0;
            height: 1px;
            background: #e5e7eb;
          }
        </style>
      </head>
      <body>
        <div class="header">
          <h1>Complete Research Report</h1>
          <p class="subtitle">Generated on ${timestamp}</p>
          <div class="stats">
            <div class="stat-item">
              <div class="stat-number">${messageStats.value.research}</div>
              <div class="stat-label">Research Points</div>
            </div>
            <div class="stat-item">
              <div class="stat-number">${getTotalWords()}</div>
              <div class="stat-label">Words</div>
            </div>
          </div>
        </div>
        <div class="content">
          ${researchContent.replace(/\n/g, '<br/>')}
        </div>
      </body>
      </html>
    `
    printWindow.document.write(htmlContent)
    printWindow.document.close()
    printWindow.focus()
    printWindow.print()
  } catch (error) {
    console.error('PDF export failed:', error)
    alert('Failed to export PDF. Check console for details.')
  }
}

const exportAsText = () => {
  try {
    const content = props.messages
      .map(m => `${m.sender.toUpperCase()}: ${m.text || ''}`)
      .join('\n\n')
    const blob = new Blob([content], { type: 'text/plain' })
    const link = document.createElement('a')
    link.href = URL.createObjectURL(blob)
    link.download = 'research-session.txt'
    link.click()
  } catch (error) {
    console.error('Text export failed:', error)
    alert('Failed to export as text.')
  }
}

const exportAsMarkdown = () => {
  try {
    const content = props.messages
      .map(m => (m.sender === 'user' ? `**User:** ${m.text}` : `**Assistant:** ${m.text}`))
      .join('\n\n---\n\n')
    const blob = new Blob([content], { type: 'text/markdown' })
    const link = document.createElement('a')
    link.href = URL.createObjectURL(blob)
    link.download = 'research-session.md'
    link.click()
  } catch (error) {
    console.error('Markdown export failed:', error)
    alert('Failed to export as markdown.')
  }
}

// Scroll automatically when messages change
watch(
  () => props.messages.length,
  () => {
    scrollToBottom(false)
  }
)

// Handle loading animation progress
let loadingInterval = null
watch(
  () => props.isLoading,
  (newVal) => {
    if (newVal) {
      loadingProgress.value = 0
      currentLoadingTextIndex.value = 0
      currentStepIndex.value = 0
      researchSteps.value.forEach((step, i) => {
        step.completed = false
        step.active = i === 0
      })

      loadingInterval = setInterval(() => {
        if (loadingProgress.value < 100) {
          loadingProgress.value += 5
          if (loadingProgress.value % 20 === 0 && currentStepIndex.value < researchSteps.value.length - 1) {
            researchSteps.value[currentStepIndex.value].completed = true
            researchSteps.value[currentStepIndex.value].active = false
            currentStepIndex.value++
            researchSteps.value[currentStepIndex.value].active = true
          }
          currentLoadingTextIndex.value = Math.min(
            Math.floor((loadingProgress.value / 100) * loadingTexts.length),
            loadingTexts.length - 1
          )
        } else {
          clearInterval(loadingInterval)
        }
      }, 500)
    } else if (loadingInterval) {
      clearInterval(loadingInterval)
    }
  }
)

onUnmounted(() => {
  if (loadingInterval) clearInterval(loadingInterval)
})

onMounted(() => {
  scrollToBottom(false)
})
</script>