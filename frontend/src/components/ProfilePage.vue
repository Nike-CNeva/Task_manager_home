<template>
  <div class="container mt-4">
    <h3>Ваши данные:</h3>

    <form @submit.prevent="handleSubmit" novalidate>
      <ul class="list-group mb-4">
        <li class="list-group-item">
          <label><strong>Имя:</strong></label>
          <input v-model="form.name" type="text" class="form-control" required />
        </li>
        <li class="list-group-item">
          <label><strong>Фамилия:</strong></label>
          <input v-model="form.firstname" type="text" class="form-control" />
        </li>
        <li class="list-group-item">
          <label><strong>Почта:</strong></label>
          <input v-model="form.email" type="email" class="form-control" />
        </li>
        <li class="list-group-item">
          <label><strong>Телеграм:</strong></label>
          <input v-model="form.telegram" type="text" class="form-control" placeholder="@username" />
        </li>
        <li class="list-group-item">
          <label><strong>Login:</strong></label>
          <input v-model="form.username" type="text" class="form-control" required />
        </li>
        <li class="list-group-item">
          <strong>Должность:</strong><br />
          {{ form.user_type || 'Не указано' }}
        </li>
        <li class="list-group-item">
          <strong>Цех:</strong><br />
          {{ form.workshops.length ? form.workshops.join(', ') : 'Не указано' }}
        </li>
      </ul>

      <button type="submit" class="btn btn-primary w-100">Сохранить изменения</button>
    </form>

    <router-link to="/profile/password" class="btn btn-warning mt-3 w-100">Изменить пароль</router-link>
  </div>
</template>

<script setup>
import { reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const form = reactive({
  name: '',
  firstname: '',
  email: '',
  telegram: '',
  username: '',
  user_type: '',
  workshops: [],
})

const isEmptyOrDefault = (value) => !value || !value.trim() || value.trim().toLowerCase() === 'не указано'

const isCyrillic = (text) => /^[А-ЯЁ][а-яё]+$/.test(text.trim())

onMounted(async () => {
  try {
    const token = localStorage.getItem('auth_token')
    if (!token) {
      throw new Error('Токен не найден! Пожалуйста, войдите в систему.')
    }

    const response = await fetch('/profile', {
      headers: {
        'Authorization': `Bearer ${token}`,
      },
    })
    if (!response.ok) throw new Error('Ошибка при загрузке данных. Пожалуйста, попробуйте позже.')

    const data = await response.json()

    // Заполняем форму, если данные есть
    form.name = data.name || ''
    form.firstname = data.firstname || ''
    form.email = data.email || ''
    form.telegram = data.telegram || ''
    form.username = data.username || ''
    form.user_type = data.user_type || ''
    form.workshops = Array.isArray(data.workshops) ? data.workshops : []
  } catch (e) {
    alert(`Ошибка: ${e.message}`)
  }
})

const handleSubmit = async () => {
  const errors = []

  if (isEmptyOrDefault(form.name) || !isCyrillic(form.name)) {
    errors.push('Имя должно содержать только кириллицу, первая буква заглавная.')
  }

  if (form.firstname && !isCyrillic(form.firstname)) {
    errors.push('Фамилия должна содержать только кириллицу, первая буква заглавная.')
  }

  if (form.email && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(form.email)) {
    errors.push('Введите корректный email.')
  }

  if (form.telegram && !/^@[a-zA-Z0-9_]{5,}$/.test(form.telegram)) {
    errors.push('Введите корректный Telegram (например, @username).')
  }

  if (isEmptyOrDefault(form.username) || form.username.length < 3) {
    errors.push('Логин должен содержать минимум 3 символа.')
  }

  if (errors.length) {
    alert('Исправьте ошибки:\n\n' + errors.join('\n'))
    return
  }

  try {
    const token = localStorage.getItem('auth_token')
    if (!token) {
      throw new Error('Токен не найден! Пожалуйста, войдите в систему.')
    }
    const response = await fetch('/profile', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(form),
    })

    if (!response.ok) throw new Error('Ошибка при сохранении данных. Пожалуйста, попробуйте позже.')

    alert('Данные успешно сохранены!')
    router.push('/home')
  } catch (e) {
    alert(`Ошибка: ${e.message}`)
  }
}
</script>

<style scoped>
.container {
  max-width: 600px;
}
</style>
