<template>
  <div class="row justify-content-center mt-5">
    <div class="col-md-6">
      <div class="card">
        <div class="card-header">
          <h3 class="text-center">Вход в систему</h3>
        </div>
        <div class="card-body">
          <!-- Ошибка -->
          <div v-if="error" class="alert alert-danger">{{ error }}</div>
          
          <!-- Форма входа -->
          <form @submit.prevent="submitForm">
            <div class="mb-3">
              <label for="username" class="form-label">Логин</label>
              <input 
                type="text" 
                class="form-control" 
                id="username" 
                v-model="username" 
                required
              />
            </div>
            <div class="mb-3">
              <label for="password" class="form-label">Пароль</label>
              <input 
                type="password" 
                class="form-control" 
                id="password" 
                v-model="password" 
                required
              />
            </div>
            <button type="submit" class="btn btn-primary w-100">Войти</button>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import { mapActions } from 'vuex';

export default {
  data() {
    return {
      username: '',
      password: '',
      error: '',
      isLoading: false
    };
  },
  methods: {
    ...mapActions(['login']),
    
    async submitForm() {
      this.isLoading = true;  // Запуск процесса загрузки
      try {
        // Отправляем запрос на сервер для аутентификации
        const response = await axios.post('/login', {
          username: this.username,
          password: this.password
        });

        // Если авторизация успешна, сохраняем токен в Vuex
        if (response.data.access_token) {
          this.login({
            token: response.data.access_token,
          });

          // Локальное сохранение токена для последующего использования
          localStorage.setItem('auth_token', response.data.access_token);
          localStorage.setItem('user', JSON.stringify(response.data.user));
          
          this.$router.push('/home');
        } else {
          this.error = 'Ошибка авторизации: отсутствуют данные пользователя.';
        }
      } catch (error) {
        // Обрабатываем ошибку
        if (error.response) {
          // Если есть ответ от сервера
          this.error = `Ошибка: ${error.response.data.detail || 'Произошла ошибка при попытке войти в систему.'}`;
        } else {
          // Если ошибка не связана с сервером
          this.error = 'Произошла ошибка при попытке войти в систему.';
        }
      } finally {
        this.isLoading = false;  // Завершаем процесс загрузки
      }
    }
  }
};
</script>

<style scoped>
/* Стили для компонента */
</style>
