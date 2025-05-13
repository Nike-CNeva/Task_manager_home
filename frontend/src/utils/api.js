// utils/api.js
export async function fetchWithToken(url, options = {}) {
    const token = localStorage.getItem('auth_token');  // Получаем токен из localStorage
    if (!token) {
      throw new Error('Токен не найден! Пожалуйста, войдите в систему.');
    }
  
    const headers = {
      'Authorization': `Bearer ${token}`,  // Добавляем токен в заголовок
      'Content-Type': 'application/json',
      ...options.headers,  // Сливаем пользовательские заголовки
    };
  
    const response = await fetch(url, {
      ...options,
      headers,
    });
  
    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail || 'Неизвестная ошибка');
    }
  
    return response.json();
  }
  