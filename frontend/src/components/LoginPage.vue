<template>
  <div class="row justify-content-center mt-5">
    <div class="col-md-6">
      <div class="card shadow-sm">
        <div class="card-header">
          <h3 class="text-center">Вход в систему</h3>
        </div>
        <div class="card-body">
          <!-- Ошибка -->
          <div v-if="error" class="alert alert-danger" role="alert">{{ error }}</div>
          
          <!-- Форма входа -->
          <form @submit.prevent="submitForm" novalidate>
            <div class="mb-3">
              <label for="username" class="form-label">Логин</label>
              <input
                type="text"
                class="form-control"
                id="username"
                v-model.trim="username"
                required
                autocomplete="username"
                :disabled="isLoading"
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
                autocomplete="current-password"
                :disabled="isLoading"
              />
            </div>
            <button
              type="submit"
              class="btn btn-primary w-100"
              :disabled="isLoading"
            >
              <span v-if="isLoading" class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
              Войти
            </button>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import api from '@/utils/axios';
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
    this.error = '';
    if (!this.username || !this.password) {
      this.error = 'Пожалуйста, заполните все поля.';
      return;
    }

    this.isLoading = true;

    try {
      const response = await api.post('/login', {
        username: this.username,
        password: this.password
      });

      if (response.data.access_token && response.data.user) {
        // Передаем токен и пользователя сразу в Vuex action
        await this.login({ token: response.data.access_token, user: response.data.user });

        this.$router.push('/');
      } else {
        this.error = 'Ошибка авторизации: отсутствуют данные пользователя.';
      }
    } catch (error) {
      if (error.response) {
        this.error = `Ошибка: ${error.response.data.detail || 'Не удалось войти в систему.'}`;
      } else {
        this.error = 'Сетевая ошибка. Проверьте подключение и попробуйте снова.';
      }
    } finally {
      this.isLoading = false;
    }
  }
  }
};
</script>

<style scoped>
.card {
  border-radius: 0.5rem;
}
</style>
