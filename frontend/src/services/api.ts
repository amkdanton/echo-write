import axios from 'axios'

// API base configuration
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1'

export const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Request interceptor for auth tokens
api.interceptors.request.use(
  (config) => {
    // Add auth token from Supabase session
    const supabaseAuth = localStorage.getItem('sb-peakhkwxuahhpovehijt-auth-token')
    if (supabaseAuth) {
      try {
        const authData = JSON.parse(supabaseAuth)
        if (authData.access_token) {
          config.headers.Authorization = `Bearer ${authData.access_token}`
        }
      } catch (e) {
        console.warn('Failed to parse Supabase auth token:', e)
      }
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Handle unauthorized access
      localStorage.removeItem('auth_token')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

// API endpoints
export const endpoints = {
  // Health
  health: '/health',
  healthDetailed: '/health/detailed',
  
  // Ingestion
  processFeeds: '/ingestion/process',
  getSources: '/ingestion/sources',
  createSource: '/ingestion/sources',
  deleteSource: (id: string) => `/ingestion/sources/${id}`,
  updateSource: (id: string) => `/ingestion/sources/${id}`,
  getSourceItems: (id: string) => `/ingestion/sources/${id}/items`,
  testSource: (id: string) => `/ingestion/test/${id}`,
  ingestionStatus: '/ingestion/status',
  
  // Trends
  getTrendingItems: '/trends/analysis',
  
  // Style
  trainVoice: '/style/train',
  getVoiceProfile: '/style/profile',
  
  // Generation
  generateNewsletter: '/generation/newsletter',
  getDrafts: '/generation/drafts',
  deleteDraft: (draftId: string) => `/generation/drafts/${draftId}`,
  
  // Delivery
  sendNewsletter: '/delivery/send',
  
  // Feedback
  submitFeedback: '/feedback',
}

// API service functions
export const apiService = {
  // Health checks
  async getHealth() {
    const response = await api.get(endpoints.health)
    return response.data
  },

  async getDetailedHealth() {
    const response = await api.get(endpoints.healthDetailed)
    return response.data
  },

  // Ingestion
  async processFeeds(sourceIds: string[], forceRefresh = false) {
    const response = await api.post(endpoints.processFeeds, {
      source_ids: sourceIds,
      force_refresh: forceRefresh
    })
    return response.data
  },

  async getSources() {
    const response = await api.get(endpoints.getSources)
    return response.data
  },

  async createSource(sourceData: any) {
    const response = await api.post(endpoints.createSource, sourceData)
    return response.data
  },

  async deleteSource(sourceId: string) {
    const response = await api.delete(endpoints.deleteSource(sourceId))
    return response.data
  },

  async updateSource(sourceId: string, updates: any) {
    const response = await api.put(endpoints.updateSource(sourceId), updates)
    return response.data
  },

  async getSourceItems(sourceId: string, limit = 10) {
    const response = await api.get(endpoints.getSourceItems(sourceId), {
      params: { limit }
    })
    return response.data
  },

  async testSource(sourceId: string) {
    const response = await api.post(endpoints.testSource(sourceId))
    return response.data
  },

  async getIngestionStatus() {
    const response = await api.get(endpoints.ingestionStatus)
    return response.data
  },

  // Trends
  async getTrendingItems(timeWindow = 48, limit = 20) {
    const response = await api.post(endpoints.getTrendingItems, {
      time_window_hours: timeWindow,
      limit
    })
    return response.data
  },

  // Style
  async trainVoice(userId: string, samples: any[]) {
    const response = await api.post(endpoints.trainVoice, {
      user_id: userId,
      samples
    })
    return response.data
  },

  async getVoiceProfile(userId: string) {
    const response = await api.get(endpoints.getVoiceProfile, {
      params: { user_id: userId }
    })
    return response.data
  },

  // Generation
  async generateNewsletter(trendingItems: string[], customPrompt?: string) {
    const response = await api.post(endpoints.generateNewsletter, {
      trending_items: trendingItems,
      custom_prompt: customPrompt
    })
    return response.data
  },

  async getDrafts() {
    const response = await api.get(endpoints.getDrafts)
    return response.data
  },

  async deleteDraft(draftId: string) {
    const response = await api.delete(endpoints.deleteDraft(draftId))
    return response.data
  },

  // Delivery
  async sendNewsletter(draftId: string, recipientEmail: string, sendImmediately = true) {
    const response = await api.post(endpoints.sendNewsletter, {
      draft_id: draftId,
      recipient_email: recipientEmail,
      send_immediately: sendImmediately
    })
    return response.data
  },

  async sendTestEmail(email: string) {
    const response = await api.post('/api/v1/delivery/test', {
      email
    })
    return response.data
  },

  // Feedback
  async submitFeedback(draftId: string, reaction: '👍' | '👎', notes?: string) {
    const response = await api.post(endpoints.submitFeedback, {
      draft_id: draftId,
      reaction,
      notes
    })
    return response.data
  },
}

export default api
