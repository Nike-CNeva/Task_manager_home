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
import axios from 'axios';

// Добавляем интерцептор для токена
axios.interceptors.request.use(
  (config) => {
    const token = store.state.token;
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

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

// ⚠️ ВАЖНО: Ждём загрузки пользователя перед монтированием
store.dispatch('checkToken').finally(() => {
  const app = createApp(App);
  app.use(store);
  app.use(router);
  app.mount('#app');
});
