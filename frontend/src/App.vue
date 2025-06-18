<template>
  <div class="chat-app">
    <!-- 头部 -->
    <header class="chat-header">
      <div class="header-content">
        <div class="logo">
          <span class="logo-icon">🤖</span>
          <h1>AgentArena</h1>
        </div>
        <div class="header-controls">
          <!-- Agent选择器 -->
          <div class="agent-selector">
            <label for="agent-select">选择助手:</label>
            <select 
              id="agent-select"
              v-model="selectedAgent" 
              @change="onAgentChange"
              class="agent-select"
            >
              <option 
                v-for="agent in availableAgents" 
                :key="agent.name" 
                :value="agent.name"
              >
                {{ agent.display_name }}
              </option>
            </select>
          </div>
          <button 
            @click="clearChat" 
            class="clear-btn"
            :disabled="messages.length === 0"
          >
            🗑️ 清空对话
          </button>
        </div>
      </div>
    </header>

    <!-- 聊天区域 -->
    <main class="chat-main">
      <div class="messages-container" ref="messagesContainer">
        <!-- 欢迎消息 -->
        <div v-if="messages.length === 0" class="welcome-message">
          <div class="welcome-content">
            <span class="welcome-icon">👋</span>
            <h2>欢迎使用 AgentArena</h2>
            <div class="current-agent-info">
              <h3>当前助手: {{ getCurrentAgentDisplayName() }}</h3>
              <p>{{ getCurrentAgentDescription() }}</p>
            </div>
            <p>选择不同的助手体验不同的AI能力！</p>
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
    const selectedAgent = ref('simple_chat')
    const availableAgents = ref([])

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

    // 获取可用的agents
    const loadAgents = async () => {
      try {
        const agents = await chatService.getAgents()
        availableAgents.value = agents
        // 如果当前选择的agent不在列表中，选择第一个
        if (agents.length > 0 && !agents.find(a => a.name === selectedAgent.value)) {
          selectedAgent.value = agents[0].name
        }
      } catch (err) {
        console.error('加载agents失败:', err)
        error.value = '加载助手列表失败'
      }
    }

    // 获取当前agent的显示名称
    const getCurrentAgentDisplayName = () => {
      const agent = availableAgents.value.find(a => a.name === selectedAgent.value)
      return agent ? agent.display_name : '未知助手'
    }

    // 获取当前agent的描述
    const getCurrentAgentDescription = () => {
      const agent = availableAgents.value.find(a => a.name === selectedAgent.value)
      return agent ? agent.description : ''
    }

    // agent切换处理
    const onAgentChange = () => {
      // 切换agent时清空当前对话
      messages.value = []
      error.value = ''
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
        const response = await chatService.sendMessage(message, selectedAgent.value, conversationId.value)
        
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
          await chatService.clearConversation(selectedAgent.value, conversationId.value)
          messages.value = []
          error.value = ''
          nextTick(() => {
            messageInput.value?.focus()
          })
        } catch (err) {
          console.error('清空对话失败:', err)
          // 即使清空失败，也清空前端显示
          messages.value = []
          error.value = ''
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

    // 组件挂载后聚焦输入框和加载agents
    onMounted(async () => {
      messageInput.value?.focus()
      await loadAgents()
    })

    return {
      messages,
      inputMessage,
      isLoading,
      error,
      messagesContainer,
      messageInput,
      selectedAgent,
      availableAgents,
      formatMessage,
      formatTime,
      sendMessage,
      clearChat,
      handleKeydown,
      adjustTextareaHeight,
      loadAgents,
      getCurrentAgentDisplayName,
      getCurrentAgentDescription,
      onAgentChange
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
  padding: 1rem 2rem;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  max-width: 1200px;
  margin: 0 auto;
}

.logo {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.logo-icon {
  font-size: 2rem;
}

.logo h1 {
  margin: 0;
  font-size: 1.5rem;
  font-weight: 600;
}

.header-controls {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.agent-selector {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.agent-selector label {
  font-size: 0.9rem;
  font-weight: 500;
}

.agent-select {
  padding: 0.5rem;
  border: none;
  border-radius: 6px;
  background: rgba(255, 255, 255, 0.9);
  color: #333;
  font-size: 0.9rem;
  min-width: 120px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.agent-select:hover {
  background: white;
}

.agent-select:focus {
  outline: none;
  box-shadow: 0 0 0 2px rgba(255, 255, 255, 0.5);
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

.current-agent-info {
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
  color: white;
  padding: 1rem;
  border-radius: 12px;
  margin: 1rem 0;
}

.current-agent-info h3 {
  margin: 0 0 0.5rem 0;
  font-size: 1.2rem;
  font-weight: 600;
}

.current-agent-info p {
  margin: 0;
  font-size: 0.9rem;
  opacity: 0.9;
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