<template>
  <nav class="navbar navbar-expand-lg navbar-light bg-light">
    <div class="container-fluid">
      <router-link class="navbar-brand" to="/">🛠️ Производство</router-link>
      <button
        class="navbar-toggler"
        type="button"
        data-bs-toggle="collapse"
        data-bs-target="#navbarNav"
        aria-controls="navbarNav"
        aria-expanded="false"
        aria-label="Toggle navigation"
      >
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarNav">
        <ul class="navbar-nav ms-auto">
          <template v-if="isAuthenticated">
            <li class="nav-item">
              <router-link class="nav-link" to="/">🏠 Главная</router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/tasks">📋 Задачи</router-link>
            </li>
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
            <li class="nav-item">
              <button @click="logout" class="nav-link btn btn-link" type="button">🚪 Выйти</button>
            </li>
          </template>
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
      this.$store.dispatch('logout');
      this.$router.push('/login');
    }
  }
};
</script>

<style scoped>
/* Можно добавить стили по желанию */
</style>
