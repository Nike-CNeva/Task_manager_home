import { createRouter, createWebHistory } from 'vue-router';
import HomePage from '../components/HomePage.vue';
import TasksPage from '../components/TasksPage.vue';
import LoginPage from '../components/LoginPage.vue';
import ProfilePage from '../components/ProfilePage.vue';
import UserManagement from '@/components/UserManagement.vue';
import UserForm from '@/components/UserForm.vue';
import ChangePassword from '@/components/ChangePassword.vue';
import CreateBid from '../components/CreateBid.vue';
// другие страницы...

const routes = [
  { path: '/', name: 'HomePage', component: HomePage, meta: { requiresAuth: true } },
  { path: '/tasks', component: TasksPage, meta: { requiresAuth: true } },
  { path: '/profile', component: ProfilePage, meta: { requiresAuth: true } },
  { path: '/profile/password', component: ChangePassword, meta: { requiresAuth: true } },
  { path: '/admin/users', name: 'UserManagement', component: UserManagement, meta: { requiresAuth: true } },
  { path: '/admin/users/create', name: 'UserCreate', component: UserForm, meta: { requiresAuth: true } },
  { path: '/admin/users/:id/edit', name: 'UserEdit', component: UserForm, props: true, meta: { requiresAuth: true } },
  { path: '/create-bid', name: 'CreateBid', component: CreateBid, meta: { requiresAuth: true } },
  { path: '/login', name: 'LoginPage', component: LoginPage }, // доступен без авторизации
];

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
});
router.beforeEach((to, from, next) => {
  if (!store.getters.isAuthChecked) {
    // Ждём, пока store не проверит токен
    const unwatch = store.watch(
      (state) => state.authChecked,
      (val) => {
        if (val) {
          unwatch();
          proceed();
        }
      }
    );
  } else {
    proceed();
  }

  function proceed() {
    if (to.meta.requiresAuth && !store.getters.isAuthenticated) {
      next({ name: 'Login' });
    } else {
      next();
    }
  }
});
export default router;
