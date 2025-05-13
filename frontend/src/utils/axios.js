// src/utils/axios.js
import axios from 'axios';

// Создание экземпляра axios с базовыми настройками
const api = axios.create({
  baseURL: '/api', // Устанавливаем базовый URL для всех запросов
  headers: {
    'Content-Type': 'application/json', // Стандартный заголовок
  }
});

// Добавление интерсептора для добавления токена в заголовки
api.interceptors.request.use(
  config => {
    const token = localStorage.getItem('auth_token'); // Получаем токен из localStorage
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`; // Добавляем токен в заголовок
    }
    return config;
  },
  error => {
    return Promise.reject(error);
  }
);

export default api;
