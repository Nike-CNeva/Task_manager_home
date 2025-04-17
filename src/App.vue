<template>
  <div id="app">
    <!-- Навигация -->
    <AppNavbar />

    <!-- Основной контент -->
    <div class="container mt-5">
      <router-view /> <!-- Здесь будет отображаться текущая страница -->
    </div>

    <!-- Подвал -->
    <AppFooter />
  </div>
</template>

<script>
// Импортируем компоненты для навигации и подвала
import AppNavbar from './components/AppNavbar.vue';
import AppFooter from './components/AppFooter.vue';

export default {
  name: 'App',
  components: {
    AppNavbar,
    AppFooter,
  },
};
</script>

<style>
/* Подключение глобальных стилей */
@import "~bootstrap/dist/css/bootstrap.min.css";

/* Дополнительные стили */
body {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}
</style>
