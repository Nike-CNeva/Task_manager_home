<template>
  <div id="app">
    <AppNavbar />

    <div class="container mt-5" v-if="authChecked">
      <router-view />
    </div>

    <!-- Пока не проверили авторизацию — можно показать простой лоадер или пустой экран -->
    <div v-else class="d-flex justify-content-center align-items-center" style="height: 100vh;">
      <span>Загрузка...</span>
    </div>
    <AppFooter />
  </div>
</template>

<script>
import { mapGetters } from 'vuex';
import AppNavbar from './components/AppNavbar.vue';
import AppFooter from './components/AppFooter.vue';

export default {
  name: 'App',
  components: {
    AppNavbar,
    AppFooter,
  },
  computed: {
    ...mapGetters(['isAuthChecked']),
    authChecked() {
      return this.isAuthChecked;
    },
  },
  created() {
  },
};
</script>

<style>
/* Подключение глобальных стилей */
@import "bootstrap/dist/css/bootstrap.min.css";

/* Дополнительные стили */
body {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}
</style>
