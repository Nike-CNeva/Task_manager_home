<template>
    <div>
      <h1 class="mb-4">Управление пользователями</h1>
  
      <a href="/admin/users/create" class="btn btn-success mb-3">Создать нового пользователя</a>
  
      <table class="table table-striped" v-if="users && users.length > 0">
        <thead>
          <tr>
            <th>ID</th>
            <th>Имя</th>
            <th>Фамилия</th>
            <th>Логин</th>
            <th>Email</th>
            <th>Телеграм</th>
            <th>Роль</th>
            <th>Цех</th>
            <th>Действия</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="user in users" :key="user.id">
            <td>{{ user.id }}</td>
            <td>{{ user.name }}</td>
            <td>{{ user.firstname }}</td>
            <td>{{ user.username }}</td>
            <td>{{ user.email }}</td>
            <td>{{ user.telegram }}</td>
            <td>{{ user.user_type }}</td>
            <td>
              <span
                class="badge bg-primary me-1"
                v-for="workshop in user.workshops"
                :key="workshop"
              >
                {{ workshop.name }}
              </span>
            </td>
            <td>
              <router-link :to="`/admin/users/${user.id}/edit`" class="btn btn-primary btn-sm">Редактировать</router-link>
              <button @click="confirmDelete(user)" class="btn btn-danger btn-sm">Удалить</button>
            </td>
          </tr>
        </tbody>
      </table>
  
      <div v-else class="text-muted">Нет пользователей.</div>
    </div>
  </template>
  
  <script>
  import api from '@/utils/axios';  // Настроенный axios
  
  export default {
    name: "UserManagement",
    data() {
      return {
        users: [],
      };
    },
    methods: {
      async fetchUsers() {
        try {
          const { data } = await api.get('/admin/users');
          this.users = data || [];
        } catch (error) {
          console.error("Ошибка загрузки пользователей:", error);
          this.users = [];
        }
      },
      async confirmDelete(user) {
        if (!confirm(`Удалить пользователя ${user.name}?`)) return;
  
        try {
          await api.delete(`/admin/users/${user.id}/delete`);
          this.users = this.users.filter(u => u.id !== user.id);
        } catch (error) {
          const message = error.response?.data?.detail || 'Не удалось удалить пользователя';
          alert(`Ошибка: ${message}`);
        }
      },
    },
    mounted() {
      this.fetchUsers();
    },
  };
  </script>
  
  