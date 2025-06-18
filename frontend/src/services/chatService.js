import axios from 'axios'

// 创建axios实例
const api = axios.create({
  baseURL: '/api',
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// 请求拦截器
api.interceptors.request.use(
  (config) => {
    console.log('发送请求:', config.method?.toUpperCase(), config.url)
    return config
  },
  (error) => {
    console.error('请求错误:', error)
    return Promise.reject(error)
  }
)

// 响应拦截器
api.interceptors.response.use(
  (response) => {
    console.log('收到响应:', response.status, response.config.url)
    return response
  },
  (error) => {
    console.error('响应错误:', error)
    
    // 处理不同类型的错误
    let errorMessage = '网络错误，请检查连接'
    
    if (error.response) {
      // 服务器返回错误状态码
      const { status, data } = error.response
      switch (status) {
        case 400:
          errorMessage = data.detail || '请求参数错误'
          break
        case 401:
          errorMessage = '未授权访问'
          break
        case 403:
          errorMessage = '访问被禁止'
          break
        case 404:
          errorMessage = '服务不存在'
          break
        case 500:
          errorMessage = data.detail || '服务器内部错误'
          break
        case 502:
          errorMessage = '网关错误'
          break
        case 503:
          errorMessage = '服务暂时不可用'
          break
        default:
          errorMessage = data.detail || `服务器错误 (${status})`
      }
    } else if (error.request) {
      // 请求发出但没有收到响应
      if (error.code === 'ECONNABORTED') {
        errorMessage = '请求超时，请重试'
      } else {
        errorMessage = '无法连接到服务器，请检查网络'
      }
    } else {
      // 其他错误
      errorMessage = error.message || '未知错误'
    }
    
    return Promise.reject(new Error(errorMessage))
  }
)

/**
 * 聊天服务类
 */
export class ChatService {
  /**
   * 发送聊天消息
   * @param {string} message - 用户消息
   * @param {string} conversationId - 对话ID
   * @returns {Promise<Object>} 响应数据
   */
  async sendMessage(message, conversationId = 'default') {
    try {
      const response = await api.post('/chat', {
        message: message.trim(),
        conversation_id: conversationId
      })
      
      return response.data
    } catch (error) {
      console.error('发送消息失败:', error)
      throw error
    }
  }

  /**
   * 清除对话历史
   * @param {string} conversationId - 对话ID
   * @returns {Promise<Object>} 响应数据
   */
  async clearConversation(conversationId = 'default') {
    try {
      const response = await api.delete(`/chat/${conversationId}`)
      return response.data
    } catch (error) {
      console.error('清除对话失败:', error)
      throw error
    }
  }

  /**
   * 健康检查
   * @returns {Promise<Object>} 健康状态
   */
  async healthCheck() {
    try {
      const response = await api.get('/health')
      return response.data
    } catch (error) {
      console.error('健康检查失败:', error)
      throw error
    }
  }

  /**
   * 测试连接
   * @returns {Promise<boolean>} 连接状态
   */
  async testConnection() {
    try {
      await this.healthCheck()
      return true
    } catch (error) {
      return false
    }
  }
}

// 导出单例实例
export const chatService = new ChatService()

// 默认导出
export default chatService