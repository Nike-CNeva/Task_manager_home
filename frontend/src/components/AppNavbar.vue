<template>
  <nav class="navbar navbar-expand-lg navbar-light bg-light">
    <div class="container-fluid">
      <a class="navbar-brand" href="/">🛠️ Производство</a>
      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav"
        aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarNav">
        <ul class="navbar-nav ms-auto">
          <!-- Если пользователь авторизован -->
          <template v-if="isAuthenticated">
            <li class="nav-item">
              <router-link class="nav-link" to="/home">🏠 Главная</router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/tasks">📋 Задачи</router-link>
            </li>
            <!-- Если пользователь - Администратор -->
            <template v-if="userType === 'Администратор'">
              <li class="nav-item">
                <router-link class="nav-link" to="/create-bid">➕ Добавить задачу</router-link>
              </li>
              <li class="nav-item">
                <router-link class="nav-link" to="/workshops">🏭 Цеха</router-link>
              </li>
              <li class="nav-item">
                <router-link class="nav-link" to="/admin/users">⚙️ Управление пользователями</router-link>
              </li>
            </template>
            <li class="nav-item">
              <router-link class="nav-link" to="/profile">👤 Личный кабинет</router-link>
            </li>
            <!-- Здесь меняем <router-link> на <button>, который будет вызывать метод logout -->
            <li class="nav-item">
              <button @click="logout" class="nav-link btn btn-link">🚪 Выйти</button>
            </li>
          </template>
          <!-- Если пользователь не авторизован -->
          <template v-else>
            <li class="nav-item">
              <router-link class="nav-link" to="/login">🔐 Войти</router-link>
            </li>
          </template>
        </ul>
      </div>
    </div>
  </nav>
</template>

  
<script>
import { mapGetters } from 'vuex';

export default {
  name: 'AppNavbar',
  computed: {
    ...mapGetters(['isAuthenticated', 'getUser']),
    userType() {
      return this.getUser?.user_type || '';
    }
  },
  methods: {
    logout() {
  // Удаляем токен и данные о пользователе из Vuex
  this.$store.dispatch('logout');
  
  // Перенаправляем пользователя на страницу логина
  this.$router.push("/login");
}
  }
};
</script>
  
  <style scoped>
  /* Здесь можно добавить стили для Navbar */
  </style>
  