import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import store from './store';

import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap';

store.dispatch('checkToken').then(() => {
  router.beforeEach((to, from, next) => {
    if (!store.getters.isAuthChecked) {
      const unwatch = store.watch(
        (state, getters) => getters.isAuthChecked,
        (authChecked) => {
          if (authChecked) {
            unwatch();
            proceed();
          }
        }
      );
    } else {
      proceed();
    }

    function proceed() {
      const publicPages = ['/', '/login'];
      const authRequired = !publicPages.includes(to.path);
      const loggedIn = store.getters.isAuthenticated;

      if (authRequired && !loggedIn) {
        return next('/login');
      }
      next();
    }
  });

  const app = createApp(App);
  app.use(store);
  app.use(router);

  app.mount('#app');

  // Убираем прелоадер и показываем приложение
  document.getElementById('preloader').style.display = 'none';
  document.getElementById('app').style.display = 'block';
});