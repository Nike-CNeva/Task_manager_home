<template>
  <div class="row justify-content-center">
    <div class="col-md-12">
      <div class="card">
        <div class="card-body">
          <p>Текущая дата и время: <span>{{ currentTime }}</span></p>

          <div v-if="userAuthenticated" class="auth-content">
            <h2>Добро пожаловать, {{ userName }}!</h2>
            <router-link to="/tasks" class="btn btn-success">Перейти к задачам</router-link>
          </div>

          <div v-else class="auth-content">
            <div class="alert alert-warning mt-4">
              <h4 class="alert-heading">Добро пожаловать на главную страницу!</h4>
              <p>Пожалуйста, авторизуйтесь, чтобы начать работать.</p>
              <router-link to="/login" class="btn btn-primary">Войти</router-link>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapState } from 'vuex';

export default {
  data() {
    return {
      currentTime: '',
      user: null
    };
  },
  computed: {
    ...mapState(['token']),
    userAuthenticated() {
      return !!this.token;
    },
    userName() {
      return this.user?.name || 'Гость';
    }
  },
  mounted() {
    if (this.userAuthenticated) {
      this.getData();
    }
    this.updateTime();
    setInterval(this.updateTime, 1000);
  },
  methods: {
    async fetchWithToken(url, options = {}) {
      // Пример функции fetch с токеном и обработкой ошибок
      const baseUrl = ''; // если нужно, добавь базовый URL API
      const response = await fetch(baseUrl + url, options);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      return await response.json();
    },

    async getData() {
      try {
        const data = await this.fetchWithToken('/home', {
          headers: {
            Authorization: `Bearer ${this.token}`,
          }
        });
        this.currentTime = new Date(data.current_datetime).toLocaleString();
        this.user = data.user;
      } catch (error) {
        console.error("Ошибка при получении данных:", error);
      }
    },

    updateTime() {
      this.currentTime = new Date().toLocaleString();
    }
  }
};
</script>

<style scoped>

</style>
