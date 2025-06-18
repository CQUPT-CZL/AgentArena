<template>
  <div class="chat-app">
    <!-- 头部 -->
    <header class="chat-header">
      <div class="header-content">
        <div class="logo">
          <span class="logo-icon">🤖</span>
          <h1>ChatGPT 助手</h1>
        </div>
        <button 
          @click="clearChat" 
          class="clear-btn"
          :disabled="messages.length === 0"
        >
          🗑️ 清空对话
        </button>
      </div>
    </header>

    <!-- 聊天区域 -->
    <main class="chat-main">
      <div class="messages-container" ref="messagesContainer">
        <!-- 欢迎消息 -->
        <div v-if="messages.length === 0" class="welcome-message">
          <div class="welcome-content">
            <span class="welcome-icon">👋</span>
            <h2>欢迎使用 ChatGPT 助手</h2>
            <p>我是你的AI助手，有什么可以帮助你的吗？</p>
          </div>
        </div>

        <!-- 消息列表 -->
        <div 
          v-for="(message, index) in messages" 
          :key="index" 
          class="message"
          :class="message.type"
        >
          <div class="message-avatar">
            <span v-if="message.type === 'user'">👤</span>
            <span v-else>🤖</span>
          </div>
          <div class="message-content">
            <div class="message-text" v-html="formatMessage(message.content)"></div>
            <div class="message-time">{{ formatTime(message.timestamp) }}</div>
          </div>
        </div>

        <!-- 加载状态 -->
        <div v-if="isLoading" class="message ai">
          <div class="message-avatar">
            <span>🤖</span>
          </div>
          <div class="message-content">
            <div class="typing-indicator">
              <span></span>
              <span></span>
              <span></span>
            </div>
          </div>
        </div>
      </div>
    </main>

    <!-- 输入区域 -->
    <footer class="chat-footer">
      <div class="input-container">
        <div class="input-wrapper">
          <textarea
            v-model="inputMessage"
            @keydown="handleKeydown"
            @input="adjustTextareaHeight"
            ref="messageInput"
            placeholder="输入你的消息..."
            class="message-input"
            :disabled="isLoading"
            rows="1"
          ></textarea>
          <button 
            @click="sendMessage" 
            class="send-btn"
            :disabled="!inputMessage.trim() || isLoading"
          >
            <span v-if="!isLoading">📤</span>
            <span v-else class="loading-spinner">⏳</span>
          </button>
        </div>
        <div class="input-hint">
          按 Enter 发送，Shift + Enter 换行
        </div>
      </div>
    </footer>

    <!-- 错误提示 -->
    <div v-if="error" class="error-toast" @click="error = ''">
      <span class="error-icon">⚠️</span>
      <span class="error-text">{{ error }}</span>
      <span class="error-close">✕</span>
    </div>
  </div>
</template>

<script>
import { ref, reactive, onMounted, nextTick } from 'vue'
import { marked } from 'marked'
import hljs from 'highlight.js'
import 'highlight.js/styles/github.css'
import { chatService } from './services/chatService.js'

export default {
  name: 'ChatApp',
  setup() {
    const messages = ref([])
    const inputMessage = ref('')
    const isLoading = ref(false)
    const error = ref('')
    const messagesContainer = ref(null)
    const messageInput = ref(null)
    const conversationId = ref('default')

    // 配置marked
    marked.setOptions({
      highlight: function(code, lang) {
        if (lang && hljs.getLanguage(lang)) {
          return hljs.highlight(code, { language: lang }).value
        }
        return hljs.highlightAuto(code).value
      },
      breaks: true
    })

    // 格式化消息内容
    const formatMessage = (content) => {
      return marked(content)
    }

    // 格式化时间
    const formatTime = (timestamp) => {
      return new Date(timestamp).toLocaleTimeString('zh-CN', {
        hour: '2-digit',
        minute: '2-digit'
      })
    }

    // 滚动到底部
    const scrollToBottom = () => {
      nextTick(() => {
        if (messagesContainer.value) {
          messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
        }
      })
    }

    // 调整文本框高度
    const adjustTextareaHeight = () => {
      nextTick(() => {
        const textarea = messageInput.value
        if (textarea) {
          textarea.style.height = 'auto'
          textarea.style.height = Math.min(textarea.scrollHeight, 120) + 'px'
        }
      })
    }

    // 发送消息
    const sendMessage = async () => {
      const message = inputMessage.value.trim()
      if (!message || isLoading.value) return

      // 添加用户消息
      messages.value.push({
        type: 'user',
        content: message,
        timestamp: Date.now()
      })

      inputMessage.value = ''
      isLoading.value = true
      error.value = ''
      scrollToBottom()

      try {
        const response = await chatService.sendMessage(message, conversationId.value)
        
        // 添加AI回复
        messages.value.push({
          type: 'ai',
          content: response.response,
          timestamp: Date.now()
        })
      } catch (err) {
        console.error('发送消息失败:', err)
        error.value = err.message || '发送消息失败，请重试'
      } finally {
        isLoading.value = false
        scrollToBottom()
        nextTick(() => {
          messageInput.value?.focus()
        })
      }
    }

    // 清空对话
    const clearChat = async () => {
      if (messages.value.length === 0) return
      
      if (confirm('确定要清空所有对话吗？')) {
        try {
          await chatService.clearConversation(conversationId.value)
          messages.value = []
          error.value = ''
        } catch (err) {
          console.error('清空对话失败:', err)
          error.value = '清空对话失败'
        }
      }
    }

    // 处理键盘事件
    const handleKeydown = (event) => {
      if (event.key === 'Enter' && !event.shiftKey) {
        event.preventDefault()
        sendMessage()
      }
    }

    // 组件挂载后聚焦输入框
    onMounted(() => {
      messageInput.value?.focus()
    })

    return {
      messages,
      inputMessage,
      isLoading,
      error,
      messagesContainer,
      messageInput,
      formatMessage,
      formatTime,
      sendMessage,
      clearChat,
      handleKeydown,
      adjustTextareaHeight
    }
  }
}
</script>

<style scoped>
.chat-app {
  height: 100vh;
  display: flex;
  flex-direction: column;
  background: white;
  max-width: 1200px;
  margin: 0 auto;
  box-shadow: 0 0 20px rgba(0, 0, 0, 0.1);
}

/* 头部样式 */
.chat-header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 1rem 1.5rem;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.logo {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.logo-icon {
  font-size: 2rem;
}

.logo h1 {
  font-size: 1.5rem;
  font-weight: 600;
}

.clear-btn {
  background: rgba(255, 255, 255, 0.2);
  border: 1px solid rgba(255, 255, 255, 0.3);
  color: white;
  padding: 0.5rem 1rem;
  border-radius: 0.5rem;
  cursor: pointer;
  transition: all 0.3s ease;
  font-size: 0.9rem;
}

.clear-btn:hover:not(:disabled) {
  background: rgba(255, 255, 255, 0.3);
}

.clear-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* 主聊天区域 */
.chat-main {
  flex: 1;
  overflow: hidden;
  background: #f8fafc;
}

.messages-container {
  height: 100%;
  overflow-y: auto;
  padding: 1rem;
  scroll-behavior: smooth;
}

/* 欢迎消息 */
.welcome-message {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100%;
  text-align: center;
}

.welcome-content {
  background: white;
  padding: 3rem 2rem;
  border-radius: 1rem;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  max-width: 400px;
}

.welcome-icon {
  font-size: 3rem;
  display: block;
  margin-bottom: 1rem;
}

.welcome-content h2 {
  color: #1f2937;
  margin-bottom: 0.5rem;
  font-size: 1.5rem;
}

.welcome-content p {
  color: #6b7280;
  font-size: 1rem;
}

/* 消息样式 */
.message {
  display: flex;
  margin-bottom: 1.5rem;
  animation: slideUp 0.3s ease;
}

.message.user {
  justify-content: flex-end;
}

.message-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.2rem;
  flex-shrink: 0;
}

.message.user .message-avatar {
  background: #667eea;
  color: white;
  order: 2;
  margin-left: 0.75rem;
}

.message.ai .message-avatar {
  background: #f3f4f6;
  color: #374151;
  margin-right: 0.75rem;
}

.message-content {
  max-width: 70%;
  min-width: 100px;
}

.message-text {
  padding: 1rem 1.25rem;
  border-radius: 1rem;
  line-height: 1.6;
  word-wrap: break-word;
}

.message.user .message-text {
  background: #667eea;
  color: white;
  border-bottom-right-radius: 0.25rem;
}

.message.ai .message-text {
  background: white;
  color: #1f2937;
  border: 1px solid #e5e7eb;
  border-bottom-left-radius: 0.25rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.message-time {
  font-size: 0.75rem;
  color: #9ca3af;
  margin-top: 0.25rem;
  text-align: right;
}

.message.ai .message-time {
  text-align: left;
}

/* 打字指示器 */
.typing-indicator {
  display: flex;
  align-items: center;
  gap: 0.25rem;
  padding: 1rem 1.25rem;
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 1rem;
  border-bottom-left-radius: 0.25rem;
}

.typing-indicator span {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #9ca3af;
  animation: typing 1.4s infinite ease-in-out;
}

.typing-indicator span:nth-child(2) {
  animation-delay: 0.2s;
}

.typing-indicator span:nth-child(3) {
  animation-delay: 0.4s;
}

/* 底部输入区域 */
.chat-footer {
  background: white;
  border-top: 1px solid #e5e7eb;
  padding: 1rem 1.5rem;
}

.input-container {
  max-width: 100%;
}

.input-wrapper {
  display: flex;
  align-items: flex-end;
  gap: 0.75rem;
  background: #f9fafb;
  border: 2px solid #e5e7eb;
  border-radius: 1rem;
  padding: 0.75rem;
  transition: border-color 0.3s ease;
}

.input-wrapper:focus-within {
  border-color: #667eea;
}

.message-input {
  flex: 1;
  border: none;
  background: transparent;
  resize: none;
  outline: none;
  font-size: 1rem;
  line-height: 1.5;
  min-height: 24px;
  max-height: 120px;
  font-family: inherit;
}

.message-input::placeholder {
  color: #9ca3af;
}

.send-btn {
  background: #667eea;
  color: white;
  border: none;
  border-radius: 0.5rem;
  padding: 0.5rem;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  min-width: 40px;
  height: 40px;
  font-size: 1.1rem;
}

.send-btn:hover:not(:disabled) {
  background: #5a67d8;
  transform: translateY(-1px);
}

.send-btn:disabled {
  background: #d1d5db;
  cursor: not-allowed;
  transform: none;
}

.input-hint {
  font-size: 0.75rem;
  color: #9ca3af;
  margin-top: 0.5rem;
  text-align: center;
}

/* 错误提示 */
.error-toast {
  position: fixed;
  top: 1rem;
  right: 1rem;
  background: #fee2e2;
  border: 1px solid #fecaca;
  color: #dc2626;
  padding: 1rem 1.5rem;
  border-radius: 0.5rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  cursor: pointer;
  animation: slideIn 0.3s ease;
  z-index: 1000;
  max-width: 400px;
}

.error-icon {
  font-size: 1.2rem;
}

.error-close {
  margin-left: auto;
  opacity: 0.7;
}

/* 动画 */
@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes typing {
  0%, 60%, 100% {
    transform: translateY(0);
  }
  30% {
    transform: translateY(-10px);
  }
}

@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateX(100%);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

.loading-spinner {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

/* 响应式设计 */
@media (max-width: 768px) {
  .chat-header {
    padding: 1rem;
  }
  
  .logo h1 {
    font-size: 1.25rem;
  }
  
  .clear-btn {
    padding: 0.4rem 0.8rem;
    font-size: 0.8rem;
  }
  
  .messages-container {
    padding: 0.75rem;
  }
  
  .message-content {
    max-width: 85%;
  }
  
  .chat-footer {
    padding: 1rem;
  }
  
  .welcome-content {
    padding: 2rem 1.5rem;
    margin: 0 1rem;
  }
}
</style>