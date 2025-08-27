<template>
  <div :class="messageContainerClass" class="group">
    <!-- Bot Avatar with enhanced styling -->
    <div v-if="message.sender === 'bot'" class="flex-shrink-0 mr-4">
      <div class="relative">
        <div class="w-12 h-12 bg-gradient-to-br from-emerald-500 via-blue-500 to-purple-600 rounded-xl flex items-center justify-center shadow-xl transition-all duration-300 group-hover:scale-105 group-hover:shadow-2xl">
          <svg class="w-6 h-6 text-white" fill="currentColor" viewBox="0 0 24 24">
            <path d="M12 2C6.48 2 2 6.48 2 12c0 5.52 4.48 10 10 10s10-4.48 10-10S17.52 2 12 2zm-1 17.93c-3.94-.49-7-3.85-7-7.93 0-.62.08-1.21.21-1.79L9 15v1c0 1.1.9 2 2 2v1.93zm6.9-2.54c-.26-.81-1-1.39-1.9-1.39h-1v-3c0-.55-.45-1-1-1H8v-2h2c.55 0 1-.45 1-1V7h2c1.1 0 2-.9 2-2v-.41c2.93 1.19 5 4.06 5 7.41 0 2.08-.8 3.97-2.1 5.39z"/>
          </svg>
        </div>
        <!-- Active indicator for bot messages -->
        <div v-if="message.isThinking" class="absolute -bottom-1 -right-1 w-5 h-5 bg-green-500 rounded-full border-3 border-white flex items-center justify-center shadow-lg">
          <div class="w-2 h-2 bg-white rounded-full animate-pulse"></div>
        </div>
      </div>
    </div>

    <!-- Enhanced Message Bubble -->
    <div :class="messageBubbleClass" class="group-hover:shadow-xl transition-all duration-300">
      <!-- Message header for bot messages -->
      <div v-if="message.sender === 'bot' && !message.isThinking" class="flex items-center justify-between mb-4 pb-3 border-b border-gray-100">
        <div class="flex items-center space-x-3">
          <div class="flex items-center space-x-2">
            <span class="text-sm font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
              AI Research Assistant
            </span>
            <div class="w-2 h-2 bg-green-500 rounded-full animate-pulse shadow-sm"></div>
          </div>
          <div v-if="message.isFollowup" class="px-3 py-1 bg-gradient-to-r from-amber-100 to-amber-200 text-amber-800 rounded-full text-xs font-semibold border border-amber-300">
            Follow-up Question
          </div>
        </div>
        <div class="flex items-center space-x-2 text-xs text-gray-400 opacity-0 group-hover:opacity-100 transition-all duration-300">
          <svg class="w-3 h-3" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-12a1 1 0 10-2 0v4a1 1 0 00.293.707l2.828 2.829a1 1 0 101.415-1.415L11 9.586V6z" clip-rule="evenodd"/>
          </svg>
          {{ formattedTime }}
        </div>
      </div>

      <!-- Message Content with enhanced formatting -->
      <div class="message-content">
        <!-- Thinking state -->
        <div v-if="message.isThinking" class="flex items-center space-x-3 text-blue-600 py-4">
          <div class="flex space-x-1">
            <div class="w-3 h-3 bg-current rounded-full animate-bounce"></div>
            <div class="w-3 h-3 bg-current rounded-full animate-bounce" style="animation-delay: 0.1s"></div>
            <div class="w-3 h-3 bg-current rounded-full animate-bounce" style="animation-delay: 0.2s"></div>
          </div>
          <span class="text-base font-medium">{{ message.text }}</span>
        </div>
        
        <!-- Regular message content -->
        <div v-else class="prose prose-gray max-w-none">
          <!-- Check if it's a long report (more than 500 characters) -->
          <div v-if="isLongReport" class="space-y-4">
            <!-- Report header with download button -->
            <div class="flex items-center justify-between p-4 bg-gradient-to-r from-blue-50 to-purple-50 rounded-lg border border-blue-200">
              <div class="flex items-center space-x-3">
                <div class="w-8 h-8 bg-gradient-to-r from-blue-500 to-purple-600 rounded-lg flex items-center justify-center">
                  <svg class="w-4 h-4 text-white" fill="currentColor" viewBox="0 0 20 20">
                    <path d="M9 2a1 1 0 000 2h2a1 1 0 100-2H9z"/>
                    <path fill-rule="evenodd" d="M4 5a2 2 0 012-2v1a2 2 0 00-2 2v6a2 2 0 002 2h8a2 2 0 002-2V6a2 2 0 00-2-2v1a2 2 0 012-2H6a2 2 0 00-2 2z" clip-rule="evenodd"/>
                  </svg>
                </div>
                <div>
                  <h3 class="font-semibold text-gray-800">Research Report</h3>
                  <p class="text-sm text-gray-600">{{ getWordCount(message.text) }} words • {{ getReadTime(message.text) }} min read</p>
                </div>
              </div>
              <button
                @click="downloadAsPDF"
                class="flex items-center space-x-2 px-4 py-2 bg-gradient-to-r from-blue-500 to-purple-600 text-white rounded-lg hover:from-blue-600 hover:to-purple-700 transition-all duration-200 shadow-md hover:shadow-lg transform hover:scale-105"
              >
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
                </svg>
                <span class="font-medium">Download PDF</span>
              </button>
            </div>
            
            <!-- Scrollable report content -->
            <div class="relative">
              <div 
                class="max-h-96 overflow-y-auto bg-white border border-gray-200 rounded-lg shadow-inner scrollbar-thin scrollbar-thumb-gray-300 scrollbar-track-gray-100"
                :class="{ 'max-h-none': isExpanded }"
              >
                <div class="p-6">
                  <div v-html="formattedText" class="prose prose-sm max-w-none prose-headings:text-gray-800 prose-headings:font-semibold prose-p:text-gray-700 prose-p:leading-relaxed prose-ul:text-gray-700 prose-ol:text-gray-700 prose-strong:text-gray-800 prose-em:text-gray-600"></div>
                </div>
              </div>
              
              <!-- Expand/Collapse button -->
              <div v-if="!isExpanded" class="absolute bottom-0 left-0 right-0 h-16 bg-gradient-to-t from-white via-white/90 to-transparent flex items-end justify-center pb-2">
                <button
                  @click="toggleExpanded"
                  class="flex items-center space-x-2 px-4 py-2 bg-white border border-gray-300 rounded-full shadow-md hover:shadow-lg transition-all duration-200 text-gray-700 hover:text-gray-900"
                >
                  <span class="text-sm font-medium">Show Full Report</span>
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/>
                  </svg>
                </button>
              </div>
              
              <!-- Collapse button when expanded -->
              <div v-if="isExpanded" class="flex justify-center mt-4">
                <button
                  @click="toggleExpanded"
                  class="flex items-center space-x-2 px-4 py-2 bg-gray-100 border border-gray-300 rounded-full hover:bg-gray-200 transition-all duration-200 text-gray-700 hover:text-gray-900"
                >
                  <span class="text-sm font-medium">Show Less</span>
                  <svg class="w-4 h-4 transform rotate-180" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/>
                  </svg>
                </button>
              </div>
            </div>
          </div>
          
          <!-- Short message content -->
          <div v-else>
            <div v-html="formattedText" class="text-sm leading-relaxed prose prose-sm max-w-none prose-headings:text-gray-800 prose-p:text-gray-700"></div>
          </div>
        </div>
      </div>

      <!-- Timestamp for user messages -->
      <div v-if="message.sender === 'user' || message.isThinking" :class="timestampClass" class="mt-3">
        {{ formattedTime }}
      </div>

      <!-- Enhanced message actions -->
      <div v-if="!message.isThinking" class="flex items-center justify-between mt-4 pt-3 border-t border-gray-100 opacity-0 group-hover:opacity-100 transition-all duration-200">
        <div class="flex space-x-2">
          <!-- Copy button -->
          <button 
            @click="copyMessage" 
            class="flex items-center space-x-1 p-2 rounded-lg hover:bg-gray-100 text-gray-500 hover:text-gray-700 transition-all duration-200 group/btn"
            title="Copy message"
          >
            <svg class="w-4 h-4 group-hover/btn:scale-110 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z"/>
            </svg>
            <span class="text-xs font-medium">Copy</span>
          </button>
          
          <!-- Regenerate button for bot messages -->
          <button 
            v-if="message.sender === 'bot' && !isError"
            @click="regenerateMessage"
            class="flex items-center space-x-1 p-2 rounded-lg hover:bg-gray-100 text-gray-500 hover:text-gray-700 transition-all duration-200 group/btn"
            title="Regenerate response"
          >
            <svg class="w-4 h-4 group-hover/btn:rotate-180 transition-transform duration-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"/>
            </svg>
            <span class="text-xs font-medium">Regenerate</span>
          </button>
        </div>
        
        <!-- Word count for long messages -->
        <div v-if="isLongReport" class="text-xs text-gray-400 font-medium">
          {{ getWordCount(message.text) }} words
        </div>
      </div>
    </div>

    <!-- User Avatar with enhanced styling -->
    <div v-if="message.sender === 'user'" class="flex-shrink-0 ml-4">
      <div class="w-12 h-12 bg-gradient-to-br from-gray-500 to-gray-700 rounded-xl flex items-center justify-center shadow-xl transition-all duration-300 group-hover:scale-105">
        <svg class="w-6 h-6 text-white" fill="currentColor" viewBox="0 0 24 24">
          <path d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z"/>
        </svg>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, ref } from 'vue'

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

const emit = defineEmits(['copy-message', 'regenerate-message'])

const isExpanded = ref(false)
const isUser = computed(() => props.message.sender === 'user')
const isError = computed(() => props.message.isError === true)
const isLongReport = computed(() => props.message.text.length > 500)

const toggleExpanded = () => {
  isExpanded.value = !isExpanded.value
}

const messageContainerClass = computed(() => {
  return [
    'flex',
    'items-start',
    'space-x-4',
    'mb-8',
    'animate-fadeIn',
    isUser.value ? 'justify-end' : 'justify-start'
  ]
})

const messageBubbleClass = computed(() => {
  const baseClasses = [
    'rounded-2xl', 
    'p-6', 
    'max-w-4xl',
    'shadow-lg',
    'relative',
    'backdrop-blur-sm',
    'transition-all',
    'duration-300',
    'border'
  ]
  
  if (isError.value) {
    return [
      ...baseClasses, 
      'bg-red-50', 
      'text-red-800', 
      'border-red-200',
      'shadow-red-100'
    ]
  }
  
  if (isUser.value) {
    return [
      ...baseClasses, 
      'bg-gradient-to-br',
      'from-blue-500',
      'to-purple-600',
      'text-white',
      'border-blue-300',
      'shadow-blue-200/50'
    ]
  } else {
    return [
      ...baseClasses, 
      'bg-white/95',
      'text-gray-800',
      'border-gray-200',
      'shadow-gray-200/50'
    ]
  }
})

const timestampClass = computed(() => {
  const baseClasses = ['text-xs', 'opacity-70', 'font-medium']
  
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

const formattedText = computed(() => {
  if (!props.message.text) return ''
  
  let text = props.message.text
  
  // Convert markdown-style formatting to HTML
  text = text
    // Headers
    .replace(/^### (.+$)/gm, '<h3>$1</h3>')
    .replace(/^## (.+$)/gm, '<h2>$1</h2>')
    .replace(/^# (.+$)/gm, '<h1>$1</h1>')
    // Bold text
    .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
    // Italic text
    .replace(/\*(.+?)\*/g, '<em>$1</em>')
    // Line breaks and paragraphs
    .replace(/\n\n/g, '</p><p>')
    .replace(/\n/g, '<br>')
    // Wrap in paragraph tags
    .replace(/^(.+)/, '<p>$1')
    .replace(/(.+)$/, '$1</p>')
    // Lists
    .replace(/^- (.+$)/gm, '<li>$1</li>')
    .replace(/(<li>.*<\/li>)/gs, '<ul>$1</ul>')
    // Clean up empty paragraphs
    .replace(/<p><\/p>/g, '')
    .replace(/<p><br><\/p>/g, '')
  
  return text
})

const getWordCount = (text) => {
  return text.split(/\s+/).filter(word => word.length > 0).length
}

const getReadTime = (text) => {
  const wordsPerMinute = 200
  const wordCount = getWordCount(text)
  return Math.max(1, Math.ceil(wordCount / wordsPerMinute))
}

const copyMessage = () => {
  navigator.clipboard.writeText(props.message.text)
  emit('copy-message', props.message)
}

const regenerateMessage = () => {
  emit('regenerate-message', props.message)
}

const downloadAsPDF = async () => {
  try {
    // Create a new window for the PDF content
    const printWindow = window.open('', '_blank')
    if (!printWindow) {
      alert('Please allow popups to download the PDF')
      return
    }
    
    // Get formatted content
    const content = formattedText.value
    const timestamp = new Date().toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    })
    
    // Create HTML for PDF
    const htmlContent = `
      <!DOCTYPE html>
      <html>
      <head>
        <title>Research Report - ${timestamp}</title>
        <meta charset="utf-8">
        <style>
          body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 800px;
            margin: 0 auto;
            padding: 40px 20px;
            background: white;
          }
          .header {
            text-align: center;
            border-bottom: 3px solid #3B82F6;
            padding-bottom: 20px;
            margin-bottom: 30px;
          }
          .header h1 {
            color: #1F2937;
            margin: 0;
            font-size: 24px;
            font-weight: 700;
          }
          .header p {
            color: #6B7280;
            margin: 5px 0 0 0;
            font-size: 14px;
          }
          .content {
            font-size: 14px;
            line-height: 1.7;
          }
          h1, h2, h3 {
            color: #1F2937;
            margin-top: 30px;
            margin-bottom: 15px;
            font-weight: 600;
          }
          h1 { font-size: 20px; border-bottom: 2px solid #E5E7EB; padding-bottom: 8px; }
          h2 { font-size: 18px; color: #374151; }
          h3 { font-size: 16px; color: #4B5563; }
          p {
            margin-bottom: 15px;
            text-align: justify;
          }
          ul, ol {
            margin-bottom: 15px;
            padding-left: 25px;
          }
          li {
            margin-bottom: 5px;
          }
          strong {
            color: #1F2937;
            font-weight: 600;
          }
          em {
            color: #4B5563;
          }
          .footer {
            margin-top: 50px;
            padding-top: 20px;
            border-top: 1px solid #E5E7EB;
            text-align: center;
            font-size: 12px;
            color: #9CA3AF;
          }
          @media print {
            body { margin: 0; padding: 20px; }
            .header { break-after: avoid; }
          }
        </style>
      </head>
      <body>
        <div class="header">
          <h1>AI Research Report</h1>
          <p>Generated on ${timestamp}</p>
        </div>
        <div class="content">
          ${content}
        </div>
        <div class="footer">
          <p>Generated by AI Research Assistant</p>
        </div>
      </body>
      </html>
    `
    
    // Write content to the new window
    printWindow.document.write(htmlContent)
    printWindow.document.close()
    
    // Wait for content to load, then print
    printWindow.onload = () => {
      setTimeout(() => {
        printWindow.print()
        printWindow.close()
      }, 250)
    }
  } catch (error) {
    console.error('Error generating PDF:', error)
    alert('Error generating PDF. Please try again.')
  }
}
</script>

<style scoped>
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.animate-fadeIn {
  animation: fadeIn 0.4s ease-out;
}

.prose h1:first-child,
.prose h2:first-child,
.prose h3:first-child {
  margin-top: 0;
}

.prose p:last-child {
  margin-bottom: 0;
}

/* Custom scrollbar styles */
.scrollbar-thin {
  scrollbar-width: thin;
}

.scrollbar-thumb-gray-300::-webkit-scrollbar-thumb {
  background-color: #D1D5DB;
  border-radius: 6px;
}

.scrollbar-track-gray-100::-webkit-scrollbar-track {
  background-color: #F3F4F6;
}

.scrollbar-thin::-webkit-scrollbar {
  width: 6px;
  height: 6px;
}

/* Gradient text support */
.bg-clip-text {
  background-clip: text;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}
</style>