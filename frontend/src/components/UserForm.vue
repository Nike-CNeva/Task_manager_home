<template>
    <div class="container py-4">
      <h1>{{ editMode ? 'Редактировать' : 'Добавить' }} пользователя</h1>
      <form @submit.prevent="submitForm">
        <div class="mb-3">
          <label class="form-label">Имя</label>
          <input v-model="form.name" type="text" class="form-control" required>
        </div>
        <div class="mb-3">
          <label class="form-label">Фамилия</label>
          <input v-model="form.firstname" type="text" class="form-control" required>
        </div>
        <div v-if="!editMode" class="mb-3">
          <label class="form-label">Логин</label>
          <input v-model="form.username" type="text" class="form-control" required>
        </div>
  
        <div v-if="!editMode" class="mb-3">
          <label class="form-label">Пароль</label>
          <input v-model="form.password" type="password" class="form-control" required>
        </div>
  
        <div class="mb-3">
          <label class="form-label">Должность</label>
          <select v-model="form.user_type" class="form-select" required>
            <option v-for="role in roles" :key="role" :value="role">{{ role }}</option>
          </select>
        </div>
  
        <div class="mb-3">
          <label class="form-label">Цех</label>
          <select v-model="form.workshops" class="form-select" multiple required>
            <option v-for="workshop in workshops" :key="workshop" :value="workshop">{{ workshop }}</option>
          </select>
          <small class="text-muted">Удерживайте Ctrl (Cmd на Mac), чтобы выбрать несколько</small>
        </div>
  
        <div v-if="editMode" class="form-check">
          <input class="form-check-input" type="checkbox" v-model="form.is_active" />
          <label class="form-check-label">Активен</label>
        </div>
  
        <button type="submit" class="btn btn-primary mt-3">Сохранить</button>
        <router-link to="/admin/users" class="btn btn-secondary mt-3 ms-2">Отмена</router-link>
      </form>
    </div>
  </template>
  
  <script>
import api from '@/utils/axios';
  
  export default {
    name: 'UserForm',
    data() {
      return {
        editMode: false,
        userId: null,
        form: {
          name: '',
          firstname: '',
          username: '',
          password: '',
          user_type: '',
          workshops: [],
          is_active: true,
        },
        roles: [],
        workshops: [],
      };
    },
    async created() {
      const { id } = this.$route.params;
      this.editMode = !!id;
      this.userId = id;
  
      try {
        const token = localStorage.getItem('auth_token');
        if (!token) throw new Error('Токен не найден, пожалуйста, войдите в систему.');
  
        const url = this.editMode
          ? `/admin/users/${id}/edit`
          : `/admin/users/create`;
  
        const { data: metaData } = await api.get(url);
        this.roles = metaData.roles;
        this.workshops = metaData.workshops;
  
        if (this.editMode) {
          const u = metaData.user_obj;
          this.form.name = u.name;
          this.form.firstname = u.firstname;
          this.form.username = u.username;
          this.form.user_type = u.user_type;
          this.form.workshops = metaData.user_workshops;
          this.form.is_active = u.is_active ?? true;
        }
      } catch (err) {
        console.error("Ошибка при загрузке данных:", err);
        alert(`Ошибка при загрузке данных: ${err.message}`);
      }
    },
    methods: {
      async submitForm() {
        const payload = { ...this.form };
  
        if (this.editMode) {
          payload.id = this.userId;
          // Если не меняем пароль — можно удалить поле или поставить заглушку
          // delete payload.password;
        }
  
        try {
          const token = localStorage.getItem('auth_token');
          if (!token) throw new Error('Токен не найден, пожалуйста, войдите в систему.');
  
          const { data, status } = await api.post('/admin/users/save', payload);
  
          if (status === 200) {
            if (data.redirect_url) {
              this.$router.push(data.redirect_url);
            } else {
              alert('Данные успешно сохранены!');
            }
          } else {
            alert(`Ошибка: ${data.message || 'Неизвестная ошибка'}`);
          }
        } catch (error) {
          alert(`Ошибка: ${error.response?.data?.message || error.message}`);
        }
      }
    }
  };
  </script>
  
