import axios from 'axios'
import WebApp from '@twa-dev/sdk'

const apiClient = axios.create({
  baseURL: '/api/v1/',
})

apiClient.interceptors.request.use((config) => {
  const { initData } = WebApp
  if (initData) {
    config.headers['Telegram-Init-Data'] = initData
  }
  return config
})

export default apiClient
