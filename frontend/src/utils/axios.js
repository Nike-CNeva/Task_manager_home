// src/utils/axios.js
import axios from 'axios';
import store from '@/store';
// Создание экземпляра axios с базовыми настройками
const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
  headers: {
    'Content-Type': 'application/json', // Стандартный заголовок
  }
  
});
console.log('💡 API Base URL =', import.meta.env.VITE_API_URL);
// Добавление интерсептора для добавления токена в заголовки
api.interceptors.request.use(config => {
  const token = store.getters.getToken;
  if (token) {
    config.headers['Authorization'] = `Bearer ${token}`;
  }
  return config;
}, error => Promise.reject(error));

// Добавление интерсептора для обработки ошибок 401
api.interceptors.response.use(
  response => response,
  error => {
    if (error.response && error.response.status === 401) {
      // Например, редирект на страницу логина
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);
export default api;
