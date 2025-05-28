import { createRouter, createWebHistory } from 'vue-router';
import HomePage from '../components/HomePage.vue';
import TasksPage from '../components/TasksPage.vue';
import LoginPage from '../components/LoginPage.vue';
import ProfilePage from '../components/ProfilePage.vue';
import UserManagement from '@/components/UserManagement.vue';
import UserForm from '@/components/UserForm.vue';
import ChangePassword from '@/components/ChangePassword.vue';
import CreateBid from '../components/CreateBid.vue';
import TaskDetails from '@/components/TaskDetails.vue';
// другие страницы...

const routes = [
  { path: '/', name: 'HomePage', component: HomePage, meta: { requiresAuth: true } },
  { path: '/tasks', name: 'TasksPage', component: TasksPage, meta: { requiresAuth: true } },
  { path: '/tasks/:id', name: 'TaskDetails', component: TaskDetails, meta: { requiresAuth: true } },
  { path: '/profile', name: 'ProfilePage', component: ProfilePage, meta: { requiresAuth: true } },
  { path: '/profile/password', name: 'ChangePassword', component: ChangePassword, meta: { requiresAuth: true } },
  { path: '/admin/users', name: 'UserManagement', component: UserManagement, meta: { requiresAuth: true } },
  { path: '/admin/users/create', name: 'UserCreate', component: UserForm, meta: { requiresAuth: true } },
  { path: '/admin/users/:id/edit', name: 'UserEdit', component: UserForm, props: true, meta: { requiresAuth: true } },
  { path: '/create-bid', name: 'CreateBid', component: CreateBid, meta: { requiresAuth: true } },
  { path: '/login', name: 'LoginPage', component: LoginPage }, // доступен без авторизации
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
