<template>
  <div class="row justify-content-center">
    <div class="col-md-12">
      <div class="card">
        <div class="card-body">

          <p>Текущая дата и время: <span>{{ currentTime }}</span></p>

          <!-- Если загружаемся — показываем лоадер -->
          <div v-if="loading" class="text-center my-4">
            <span>Загрузка данных...</span>
          </div>

          <!-- Если данные загружены -->
          <div v-else>
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
  </div>
</template>

<script>
import { mapState } from 'vuex';
import api from '@/utils/axios';

export default {
  data() {
    return {
      currentTime: '',
      user: null,
      timerId: null,
      loading: false,  // вот она — переменная загрузки
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
    this.timerId = setInterval(this.updateTime, 1000);
  },
  beforeUnmount() {
    clearInterval(this.timerId);
  },
  methods: {
    async getData() {
      this.loading = true;  // старт загрузки
      try {
        const { data } = await api.get('/');
        this.currentTime = new Date(data.current_datetime).toLocaleString();
        this.user = data.user;
      } catch (error) {
        console.error("Ошибка при получении данных:", error);
      } finally {
        this.loading = false; // загрузка завершена (успех или ошибка)
      }
    },
    updateTime() {
      this.currentTime = new Date().toLocaleString();
    }
  }
};
</script>