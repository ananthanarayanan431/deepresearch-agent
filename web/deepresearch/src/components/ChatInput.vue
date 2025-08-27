<template>
  <div class="p-6 bg-gradient-to-r from-white/90 via-white/95 to-white/90 backdrop-blur-xl border-t border-gray-200/60 sticky bottom-0 shadow-2xl">
    <div class="max-w-5xl mx-auto">
      <!-- Enhanced Research Status Bar -->
      <div v-if="disabled" class="mb-4 p-4 bg-gradient-to-r from-blue-50 via-purple-50 to-indigo-50 rounded-2xl border border-blue-200 shadow-sm">
        <div class="flex items-center justify-between">
          <div class="flex items-center space-x-3">
            <div class="relative">
              <div class="w-10 h-10 bg-gradient-to-r from-blue-500 to-purple-600 rounded-xl flex items-center justify-center shadow-lg">
                <svg class="w-5 h-5 text-white animate-spin" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"/>
                </svg>
              </div>
              <div class="absolute -inset-1 bg-gradient-to-r from-blue-400 to-purple-500 rounded-xl opacity-20 animate-ping"></div>
            </div>
            <div>
              <h3 class="text-sm font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
                AI Research in Progress
              </h3>
              <p class="text-xs text-gray-600">Deep analysis and comprehensive report generation</p>
            </div>
          </div>
          <div class="flex items-center space-x-4">
            <div class="flex items-center space-x-2">
              <div class="flex space-x-1">
                <div class="w-2 h-2 bg-blue-500 rounded-full animate-bounce"></div>
                <div class="w-2 h-2 bg-purple-500 rounded-full animate-bounce" style="animation-delay: 0.1s"></div>
                <div class="w-2 h-2 bg-indigo-500 rounded-full animate-bounce" style="animation-delay: 0.2s"></div>
              </div>
              <span class="text-xs font-medium text-blue-700">Processing...</span>
            </div>
            <div class="hidden sm:block text-xs text-gray-500 bg-white/60 px-3 py-1 rounded-full border">
              Est. 3-8 minutes
            </div>
          </div>
        </div>
        
        <!-- Progress Bar -->
        <div class="mt-3">
          <div class="flex justify-between text-xs text-gray-600 mb-1">
            <span>Research Progress</span>
            <span>{{ researchProgress }}%</span>
          </div>
          <div class="w-full bg-gray-200 rounded-full h-2 overflow-hidden">
            <div 
              class="bg-gradient-to-r from-blue-500 via-purple-500 to-indigo-500 h-2 rounded-full transition-all duration-1000 ease-out relative"
              :style="{ width: researchProgress + '%' }"
            >
              <div class="absolute inset-0 bg-gradient-to-r from-white/20 to-white/40 animate-pulse"></div>
            </div>
          </div>
        </div>
      </div>

      <!-- Quick Actions Bar -->
      <div v-if="!disabled" class="mb-4 flex items-center justify-between">
        <div class="flex items-center space-x-3">
          <div class="text-sm text-gray-600 font-medium">Quick Actions:</div>
          <div class="flex space-x-2">
            <button
              v-for="action in quickActions"
              :key="action.text"
              @click="insertQuickAction(action.text)"
              class="px-3 py-1.5 text-xs font-medium bg-gradient-to-r from-gray-50 to-gray-100 hover:from-blue-50 hover:to-purple-50 text-gray-700 hover:text-blue-700 rounded-full border border-gray-200 hover:border-blue-200 transition-all duration-200 transform hover:scale-105 shadow-sm hover:shadow-md"
            >
              {{ action.label }}
            </button>
          </div>
        </div>
        
        <!-- Word Count Display -->
        <div v-if="messageText.trim().length > 0" class="text-xs text-gray-500 bg-gray-50 px-3 py-1 rounded-full border">
          {{ getWordCount(messageText) }} words
        </div>
      </div>

      <!-- Enhanced Input Container -->
      <div class="relative">
        <div class="flex space-x-4 items-end">
          <!-- Main Text Input with Advanced Features -->
          <div class="flex-1 relative group">
            <!-- Input Label -->
            <div v-if="!messageText && !disabled" class="absolute -top-6 left-0 text-xs font-medium text-gray-500 transition-all duration-200">
              Research Query
            </div>
            
            <div class="relative">
              <textarea
                ref="textareaRef"
                v-model="messageText"
                @keydown="handleKeyDown"
                @input="adjustHeight"
                @focus="onFocus"
                @blur="onBlur"
                :disabled="disabled"
                :placeholder="placeholder"
                class="w-full px-6 py-4 pr-16 border-2 rounded-3xl focus:outline-none resize-none transition-all duration-300 text-gray-800 placeholder-gray-400 shadow-lg hover:shadow-xl disabled:cursor-not-allowed backdrop-blur-sm"
                rows="1"
                :class="inputClasses"
                :maxlength="2000"
              ></textarea>
              
              <!-- Enhanced Character Count -->
              <div class="absolute bottom-3 right-6 flex items-center space-x-2">
                <div 
                  class="text-xs font-medium transition-all duration-200 px-2 py-1 rounded-full"
                  :class="characterCountClass"
                >
                  {{ messageText.length }}/2000
                </div>
              </div>
              
              <!-- Focus Ring Effect -->
              <div 
                class="absolute inset-0 rounded-3xl transition-all duration-300 pointer-events-none"
                :class="focusRingClass"
              ></div>
            </div>

            <!-- Input Suggestions -->
            <div v-if="showSuggestions && !disabled" class="absolute top-full left-0 right-0 mt-2 bg-white/95 backdrop-blur-lg border border-gray-200 rounded-2xl shadow-2xl z-50 max-h-64 overflow-y-auto">
              <div class="p-3 border-b border-gray-100">
                <h4 class="text-sm font-semibold text-gray-800">Research Suggestions</h4>
                <p class="text-xs text-gray-600">Click to use, or continue typing</p>
              </div>
              <div class="p-2">
                <button
                  v-for="(suggestion, index) in filteredSuggestions"
                  :key="index"
                  @click="useSuggestion(suggestion)"
                  class="w-full text-left p-3 rounded-xl hover:bg-gradient-to-r hover:from-blue-50 hover:to-purple-50 transition-all duration-200 group border border-transparent hover:border-blue-200"
                >
                  <div class="flex items-start space-x-3">
                    <div class="w-8 h-8 bg-gradient-to-r from-blue-100 to-purple-100 rounded-lg flex items-center justify-center group-hover:from-blue-200 group-hover:to-purple-200 transition-colors">
                      <svg class="w-4 h-4 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/>
                      </svg>
                    </div>
                    <div class="flex-1 min-w-0">
                      <p class="text-sm font-medium text-gray-800 group-hover:text-blue-800 transition-colors">
                        {{ suggestion.title }}
                      </p>
                      <p class="text-xs text-gray-600 mt-0.5 line-clamp-2">
                        {{ suggestion.description }}
                      </p>
                    </div>
                  </div>
                </button>
              </div>
            </div>
          </div>

          <!-- Enhanced Send Button with States -->
          <div class="flex flex-col space-y-2">
            <!-- Main Send Button -->
            <button
              @click="sendMessage"
              :disabled="disabled || !messageText.trim()"
              class="group relative px-8 py-4 rounded-3xl focus:outline-none focus:ring-4 focus:ring-blue-500/20 transition-all duration-300 transform hover:scale-105 disabled:transform-none shadow-2xl hover:shadow-3xl disabled:shadow-none overflow-hidden min-w-[120px]"
              :class="sendButtonClass"
            >
              <!-- Background Gradient Animation -->
              <div class="absolute inset-0 bg-gradient-to-r from-blue-500 via-purple-600 to-indigo-500 transition-all duration-300 group-hover:from-blue-600 group-hover:via-purple-700 group-hover:to-indigo-600 group-disabled:from-gray-300 group-disabled:to-gray-400"></div>
              <div class="absolute inset-0 bg-gradient-to-r from-transparent via-white/10 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300 animate-shimmer"></div>
              
              <!-- Button Content -->
              <div class="relative z-10 flex items-center justify-center space-x-2 text-white group-disabled:text-gray-600">
                <div v-if="disabled" class="flex items-center space-x-2">
                  <div class="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin"></div>
                  <span class="font-semibold text-sm">Researching</span>
                </div>
                <div v-else class="flex items-center space-x-2">
                  <svg class="w-5 h-5 transition-transform group-hover:translate-x-0.5 group-hover:scale-110" fill="currentColor" viewBox="0 0 24 24">
                    <path d="M3.4 20.4L20.85 12.92c.83-.4.83-1.44 0-1.84L3.4 3.6c-.66-.32-1.39.24-1.39.98v15.44c0 .74.73 1.3 1.39.98z"/>
                  </svg>
                  <span class="font-semibold text-sm">{{ sendButtonText }}</span>
                </div>
              </div>
            </button>
            
            <!-- Voice Input Button (Optional) -->
            <button
              v-if="!disabled"
              @click="toggleVoiceInput"
              class="p-3 bg-white/90 backdrop-blur-sm border-2 border-gray-200 rounded-2xl hover:border-purple-300 focus:outline-none focus:ring-4 focus:ring-purple-500/20 transition-all duration-300 group shadow-lg hover:shadow-xl"
              title="Voice input"
            >
              <svg class="w-5 h-5 text-gray-600 group-hover:text-purple-600 transition-colors" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 01-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z"/>
              </svg>
            </button>
          </div>
        </div>

        <!-- Enhanced Helper Text and Shortcuts -->
        <div class="flex justify-between items-center mt-4 px-2">
          <div class="flex items-center space-x-6 text-xs text-gray-500">
            <div class="flex items-center space-x-2 bg-gray-50/80 backdrop-blur-sm px-3 py-1.5 rounded-full border border-gray-200">
              <kbd class="px-2 py-0.5 bg-white border border-gray-300 rounded text-xs font-mono shadow-sm">Enter</kbd>
              <span>to send</span>
            </div>
            <div class="flex items-center space-x-2 bg-gray-50/80 backdrop-blur-sm px-3 py-1.5 rounded-full border border-gray-200">
              <kbd class="px-2 py-0.5 bg-white border border-gray-300 rounded text-xs font-mono shadow-sm">Shift</kbd>
              <span>+</span>
              <kbd class="px-2 py-0.5 bg-white border border-gray-300 rounded text-xs font-mono shadow-sm">Enter</kbd>
              <span>for new line</span>
            </div>
            <div v-if="!disabled" class="flex items-center space-x-2 bg-purple-50/80 backdrop-blur-sm px-3 py-1.5 rounded-full border border-purple-200">
              <kbd class="px-2 py-0.5 bg-white border border-purple-300 rounded text-xs font-mono shadow-sm text-purple-700">Ctrl</kbd>
              <span>+</span>
              <kbd class="px-2 py-0.5 bg-white border border-purple-300 rounded text-xs font-mono shadow-sm text-purple-700">/</kbd>
              <span class="text-purple-600">suggestions</span>
            </div>
          </div>
          
          <!-- Enhanced Status Indicator -->
          <div class="flex items-center space-x-3">
            <div v-if="disabled" class="flex items-center space-x-2 text-xs font-medium bg-gradient-to-r from-blue-50 to-purple-50 text-blue-700 px-4 py-2 rounded-full border border-blue-200 shadow-sm">
              <div class="w-2 h-2 bg-blue-500 rounded-full animate-pulse"></div>
              <span>AI conducting deep research analysis</span>
            </div>
            <div v-else-if="messageText.trim()" class="text-xs text-green-600 font-medium bg-green-50 px-3 py-1.5 rounded-full border border-green-200">
              Ready to send
            </div>
            <div v-else class="text-xs text-gray-400">
              Type your research question...
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, nextTick, computed, onMounted, onUnmounted } from 'vue'

const props = defineProps({
  disabled: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['send-message'])

const messageText = ref('')
const textareaRef = ref(null)
const isFocused = ref(false)
const showSuggestions = ref(false)
const researchProgress = ref(0)

// Enhanced placeholder text rotation
const placeholderTexts = [
  "Analyze market trends for electric vehicles in 2024...",
  "Research competitive landscape for AI startups...",
  "Deep dive into renewable energy investments...",
  "Investigate consumer behavior in e-commerce...",
  "Study the impact of remote work on productivity..."
]
const currentPlaceholderIndex = ref(0)

const placeholder = computed(() => {
  if (props.disabled) return "AI is analyzing your request..."
  return placeholderTexts[currentPlaceholderIndex.value]
})

// Quick actions for common research queries
const quickActions = [
  { label: "Market Analysis", text: "Provide a comprehensive market analysis for " },
  { label: "Competitor Research", text: "Research the top competitors in " },
  { label: "Industry Trends", text: "What are the latest trends in " },
  { label: "Financial Analysis", text: "Analyze the financial performance of " }
]

// Research suggestions
const researchSuggestions = [
  {
    title: "Market Size & Growth Analysis",
    description: "Get detailed market sizing, growth projections, and key drivers for any industry or product category."
  },
  {
    title: "Competitive Landscape Deep Dive",
    description: "Comprehensive analysis of competitors, their strategies, strengths, weaknesses, and market positioning."
  },
  {
    title: "Consumer Behavior & Trends",
    description: "Research consumer preferences, buying patterns, and emerging trends in your target market."
  },
  {
    title: "Industry Disruption Analysis",
    description: "Identify potential disruptors, emerging technologies, and market shifts that could impact your industry."
  },
  {
    title: "Investment & Funding Landscape",
    description: "Analysis of investment trends, funding patterns, and financial opportunities in specific sectors."
  },
  {
    title: "Regulatory & Policy Impact",
    description: "Research regulatory changes, policy implications, and compliance requirements affecting your business."
  }
]

const filteredSuggestions = computed(() => {
  if (!messageText.value) return researchSuggestions
  const query = messageText.value.toLowerCase()
  return researchSuggestions.filter(s => 
    s.title.toLowerCase().includes(query) || 
    s.description.toLowerCase().includes(query)
  )
})

// Computed classes for enhanced styling
const inputClasses = computed(() => {
  const base = [
    'bg-white/90',
    'backdrop-blur-sm',
    'placeholder:text-gray-400',
    'text-gray-800',
    'font-medium'
  ]
  
  if (props.disabled) {
    return [
      ...base,
      'border-gray-300',
      'bg-gray-50/90',
      'cursor-not-allowed',
      'opacity-70'
    ]
  }
  
  if (isFocused.value) {
    return [
      ...base,
      'border-blue-400',
      'bg-white/95',
      'shadow-2xl',
      'ring-4',
      'ring-blue-500/10'
    ]
  }
  
  if (messageText.value.length > 0) {
    return [
      ...base,
      'border-purple-300',
      'bg-white/95',
      'shadow-xl'
    ]
  }
  
  return [
    ...base,
    'border-gray-300',
    'hover:border-gray-400',
    'hover:bg-white/95'
  ]
})

const focusRingClass = computed(() => {
  if (!isFocused.value || props.disabled) return ''
  return 'ring-4 ring-blue-500/20 border-blue-500'
})

const characterCountClass = computed(() => {
  const length = messageText.value.length
  if (length > 1800) return 'text-red-600 bg-red-50 border border-red-200'
  if (length > 1500) return 'text-orange-600 bg-orange-50 border border-orange-200'
  if (length > 1000) return 'text-yellow-600 bg-yellow-50 border border-yellow-200'
  if (length > 0) return 'text-blue-600 bg-blue-50 border border-blue-200'
  return 'text-gray-400 bg-gray-50 border border-gray-200'
})

const sendButtonClass = computed(() => {
  if (props.disabled) return 'cursor-not-allowed'
  if (!messageText.value.trim()) return 'cursor-not-allowed opacity-50'
  return 'cursor-pointer hover:shadow-3xl active:scale-95'
})

const sendButtonText = computed(() => {
  const wordCount = getWordCount(messageText.value)
  if (wordCount > 100) return 'Research'
  if (wordCount > 20) return 'Analyze'
  return 'Send'
})

// Methods
const getWordCount = (text) => {
  return text.trim().split(/\s+/).filter(word => word.length > 0).length
}

const sendMessage = () => {
  if (!messageText.value.trim() || props.disabled) return
  
  emit('send-message', messageText.value)
  messageText.value = ''
  
  nextTick(() => {
    if (textareaRef.value) {
      textareaRef.value.style.height = 'auto'
    }
  })
}

const handleKeyDown = (event) => {
  // Ctrl+/ to show suggestions
  if (event.ctrlKey && event.key === '/') {
    event.preventDefault()
    showSuggestions.value = !showSuggestions.value
    return
  }
  
  // Enter to send (unless holding Shift)
  if (event.key === 'Enter' && !event.shiftKey) {
    event.preventDefault()
    sendMessage()
    return
  }
  
  // Escape to hide suggestions
  if (event.key === 'Escape') {
    showSuggestions.value = false
    return
  }
}

const adjustHeight = () => {
  nextTick(() => {
    if (textareaRef.value) {
      textareaRef.value.style.height = 'auto'
      const maxHeight = 160 // Max height in pixels
      const newHeight = Math.min(textareaRef.value.scrollHeight, maxHeight)
      textareaRef.value.style.height = newHeight + 'px'
    }
  })
}

const onFocus = () => {
  isFocused.value = true
}

const onBlur = () => {
  isFocused.value = false
  // Delay hiding suggestions to allow clicks
  setTimeout(() => {
    showSuggestions.value = false
  }, 200)
}

const insertQuickAction = (text) => {
  messageText.value = text
  nextTick(() => {
    if (textareaRef.value) {
      textareaRef.value.focus()
      textareaRef.value.setSelectionRange(text.length, text.length)
    }
  })
}

const useSuggestion = (suggestion) => {
  messageText.value = `Research: ${suggestion.title} - ${suggestion.description.split('.')[0]}`
  showSuggestions.value = false
  nextTick(() => {
    if (textareaRef.value) {
      textareaRef.value.focus()
      adjustHeight()
    }
  })
}

const toggleVoiceInput = () => {
  // Voice input functionality would be implemented here
  console.log('Voice input toggled')
}

// Enhanced progress simulation for research state
const simulateResearchProgress = () => {
  if (!props.disabled) return
  
  const interval = setInterval(() => {
    if (!props.disabled) {
      clearInterval(interval)
      researchProgress.value = 0
      return
    }
    
    if (researchProgress.value < 90) {
      const increment = Math.random() * 10 + 2
      researchProgress.value = Math.min(90, researchProgress.value + increment)
    }
  }, 1500)
}

// Placeholder text rotation
const rotatePlaceholder = () => {
  setInterval(() => {
    if (!props.disabled && !isFocused.value && !messageText.value) {
      currentPlaceholderIndex.value = (currentPlaceholderIndex.value + 1) % placeholderTexts.length
    }
  }, 4000)
}

// Lifecycle
onMounted(() => {
  rotatePlaceholder()
  
  // Click outside to hide suggestions
  const handleClickOutside = (event) => {
    if (!event.target.closest('.relative.group')) {
      showSuggestions.value = false
    }
  }
  document.addEventListener('click', handleClickOutside)
})

// Watch for disabled state changes
import { watch } from 'vue'
watch(() => props.disabled, (newVal) => {
  if (newVal) {
    researchProgress.value = 5
    simulateResearchProgress()
  } else {
    researchProgress.value = 0
  }
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
})
</script>

<style scoped>
/* Enhanced gradient text support */
.bg-clip-text {
  background-clip: text;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

/* Advanced animations */
@keyframes shimmer {
  0% { transform: translateX(-100%); }
  100% { transform: translateX(100%); }
}

.animate-shimmer {
  animation: shimmer 2s infinite;
}

/* Enhanced shadow utilities */
.shadow-3xl {
  box-shadow: 0 35px 60px -12px rgba(0, 0, 0, 0.25);
}

/* Custom scrollbar for suggestions */
.max-h-64::-webkit-scrollbar {
  width: 6px;
}

.max-h-64::-webkit-scrollbar-track {
  background: #f1f5f9;
  border-radius: 8px;
}

.max-h-64::-webkit-scrollbar-thumb {
  background: #cbd5e1;
  border-radius: 8px;
}

.max-h-64::-webkit-scrollbar-thumb:hover {
  background: #94a3b8;
}

/* Line clamp utility */
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

/* Focus ring animation */
@keyframes focusRing {
  0% {
    transform: scale(0.95);
    opacity: 0;
  }
  100% {
    transform: scale(1);
    opacity: 1;
  }
}

.focus\:ring-4 {
  animation: focusRing 0.2s ease-out;
}
</style>