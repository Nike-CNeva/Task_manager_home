<template>
  <div class="row justify-content-center">
    <div class="col-md-12">
      <div class="card">
        <div class="card-body">
          <p>Текущая дата и время: <span>{{ currentTime }}</span></p>

          <div v-if="userAuthenticated" id="auth-content">
            <h2>Добро пожаловать, {{ userName }}!</h2>
            <a href="/tasks" class="btn btn-success">Перейти к задачам</a>
          </div>

          <div v-else id="auth-content">
            <div class="alert alert-warning mt-4">
              <h4 class="alert-heading">Добро пожаловать на главную страницу!</h4>
              <p>Пожалуйста, авторизуйтесь, чтобы начать работать.</p>
              <a href="/login" class="btn btn-primary">Войти</a>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapState } from 'vuex';
import { fetchWithToken } from '@/utils/api';

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
    this.getData();
    setInterval(this.updateTime, 1000);
  },
  methods: {
    async getData() {
      try {
        const response = await fetchWithToken('/home', {
          headers: {
            Authorization: `Bearer ${this.token}`,
          }
        });
        console.log(response);
        this.currentTime = new Date(response.current_datetime).toLocaleString();
        this.user = response.user;

      } catch (error) {
        console.error("Ошибка при получении данных:", error);
      }
    },
    updateTime() {
      const currentTime = new Date();
      this.currentTime = currentTime.toLocaleString();
    }
  }
};
</script>

<style scoped>
/* Добавьте стили для компонента, если необходимо */
</style>
