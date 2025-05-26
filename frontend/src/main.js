import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import store from './store'; // Vuex

import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap'; // <-- Это важно!

// Асинхронный старт приложения
store.dispatch('checkToken').then(() => {
  const app = createApp(App);
  app.use(store);
  app.use(router);
  app.mount('#app');
});
