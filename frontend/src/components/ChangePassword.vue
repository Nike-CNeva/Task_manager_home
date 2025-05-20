<template>
    <div class="container py-4">
      <h3>Изменение пароля</h3>
  
      <div class="alert alert-danger" v-if="error">{{ error }}</div>
      <div class="alert alert-success" v-if="success">{{ success }}</div>
  
      <form @submit.prevent="submitPasswordChange">
        <ul class="list-group mb-4">
          <li class="list-group-item">
            <strong>Текущий пароль:</strong>
            <input v-model="form.current_password" type="password" class="form-control" required />
          </li>
          <li class="list-group-item">
            <strong>Новый пароль:</strong>
            <input
              v-model="form.new_password"
              type="password"
              class="form-control"
              required
              minlength="6"
            />
          </li>
          <li class="list-group-item">
            <strong>Подтвердите новый пароль:</strong>
            <input
              v-model="form.confirm_password"
              type="password"
              class="form-control"
              required
            />
          </li>
        </ul>
  
        <button type="submit" class="btn btn-primary">Сохранить новый пароль</button>
      </form>
    </div>
  </template>
  
  <script>
  import api from '@/utils/axios';

  export default {
    name: "ChangePassword",
    data() {
      return {
        form: {
          current_password: "",
          new_password: "",
          confirm_password: "",
        },
        error: null,
        success: null,
      };
    },
    methods: {
      async submitPasswordChange() {
        this.error = null;
        this.success = null;
  
        // Простая проверка
        if (this.form.new_password.length < 6) {
          this.error = "Новый пароль должен содержать минимум 6 символов.";
          return;
        }
  
        if (this.form.new_password !== this.form.confirm_password) {
          this.error = "Новый пароль и подтверждение пароля должны совпадать.";
          return;
        }
  
        try {
          await api.put('/profile/password', this.form);
  
          this.success = "Пароль успешно изменён.";
          this.form.current_password = "";
          this.form.new_password = "";
          this.form.confirm_password = "";
        } catch (error) {
          this.error = error.response?.data?.detail || "Ошибка при смене пароля.";
        }
      },
    },
  };
  </script>
  
  <style scoped>
  .alert {
    margin-top: 1rem;
  }
  </style>
  
  