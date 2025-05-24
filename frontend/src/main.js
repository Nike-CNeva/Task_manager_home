import { createApp } from 'vue';
import App from './App.vue';
import { createRouter, createWebHistory } from 'vue-router';
import HomePage from './components/HomePage.vue';
import LoginPage from './components/LoginPage.vue';
import ProfilePage from './components/ProfilePage.vue';
import UserManagement from './components/UserManagement.vue';
import UserForm from './components/UserForm.vue';
import ChangePassword from './components/ChangePassword.vue';
import CreateBid from './components/CreateBid.vue';
import store from './store'; // Vuex
import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap'; // <-- Это важно!

// Маршруты
const routes = [
  { path: '/', component: HomePage },
  { path: '/login', component: LoginPage },
  { path: '/profile', component: ProfilePage },
  { path: '/profile/password', component: ChangePassword },
  { path: '/admin/users', component: UserManagement },
  { path: '/admin/users/create', component: UserForm },
  { path: '/admin/users/:id/edit', component: UserForm, props: true },
  { path: '/create-bid', component: CreateBid },
];

// Роутер
const router = createRouter({
  history: createWebHistory(),
  routes,
});
// Простой guard авторизации
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
// Асинхронный старт приложения
store.dispatch('checkToken').then(() => {
  const app = createApp(App);
  app.use(store);
  app.use(router);
  app.mount('#app');
});
