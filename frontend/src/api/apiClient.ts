import axios from 'axios';
import WebApp from '@twa-dev/sdk';

const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
});

apiClient.interceptors.request.use(config => {
  const { initData } = WebApp;
  initData && (config.headers['Authorization'] = initData);
  return config;
});

apiClient.interceptors.response.use(
  (response) => response,

  (error) => {
    if (error.response && error.response.status === 401) {
      const responseData = error.response.data;
      
      if (responseData && responseData.redirect_url) {
        console.log(`Требуется авторизация. Перенаправляем на: ${responseData.redirect_url}`);
        
        WebApp.openTelegramLink(responseData.redirect_url);
      }
    }
    
    return Promise.reject(error);
  }
);

export default apiClient;
