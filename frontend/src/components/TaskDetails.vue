<template>
  <div v-if="task">
    <!-- твои текущие поля задачи ... -->

    <h3>Параметры продукта</h3>
    <div v-if="firstTask && productFields.length">
      <div v-for="field in productFields" :key="field.name" class="form-group">
        <label :for="field.name">{{ field.label }}</label>

        <template v-if="field.type === 'select'">
          <select
            :id="field.name"
            v-model="firstTask[field.name]"
            class="form-control"
          >
            <option
              v-for="option in field.options"
              :key="option.value"
              :value="option.value"
            >
              {{ option.name }}
            </option>
          </select>
        </template>

        <template v-else-if="field.type === 'checkbox'">
          <input
            type="checkbox"
            :id="field.name"
            v-model="firstTask[field.name]"
          />
        </template>

        <template v-else>
          <input
            :type="field.type"
            :id="field.name"
            v-model="firstTask[field.name]"
            class="form-control"
          />
        </template>
      </div>
    </div>

    <button class="btn btn-danger" @click="deleteTask(task.id)">Удалить задачу</button>
  </div>

  <div v-else>
    <p>Загрузка задачи...</p>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import api from '@/utils/axios'

// Импортируй enum или объяви здесь соответствия, для примера сделал объект с полями:
const ProductTypeEnum = {
  PROFILE: 'Профиля',
  KLAMER: 'Клямера',
  BRACKET: 'Кронштейны',
  EXTENSION_BRACKET: 'Удлинители кронштейнов',
  CASSETTE: 'Кассеты',
  LINEAR_PANEL: 'Линеарные панели',
  SHEET: 'Листы',
}

const route = useRoute()
const router = useRouter()

const task = ref(null)
const firstTask = computed(() => task.value?.tasks?.[0] || null)

// Функция возвращает поля для конкретного типа продукта
function getProductFields(type) {
  switch(type) {
    case ProductTypeEnum.PROFILE:
      return [
        { name: 'profile_type', label: 'Тип профиля', type: 'select', options: ProfileTypeEnum },
        { name: 'length', label: 'Введите длину профиля', type: 'number' },
        { name: 'quantity', label: 'Введите количество профилей', type: 'number' },
      ]
    case ProductTypeEnum.KLAMER:
      return [
        { name: 'klamer_type', label: 'Тип клямера', type: 'select', options: KlamerTypeEnum },
        { name: 'quantity', label: 'Введите количество клямеров', type: 'number' },
      ]
    case ProductTypeEnum.BRACKET:
      return [
        { name: 'width', label: 'Ширина', type: 'number' },
        { name: 'length', label: 'Длина', type: 'text' },
        { name: 'quantity', label: 'Количество кронштейнов', type: 'number' },
      ]
    case ProductTypeEnum.EXTENSION_BRACKET:
      return [
        { name: 'width', label: 'Ширина', type: 'number' },
        { name: 'length', label: 'Длина', type: 'text' },
        { name: 'has_heel', label: 'Наличие пятки', type: 'checkbox' },
        { name: 'quantity', label: 'Количество удлинителей', type: 'number' },
      ]
    case ProductTypeEnum.CASSETTE:
      return [
        { name: 'cassette_type', label: 'Тип кассеты', type: 'select', options: CassetteTypeEnum },
        { name: 'description', label: 'Введите описание', type: 'text' },
        { name: 'quantity', label: 'Введите количество кассет', type: 'number' },
      ]
    case ProductTypeEnum.LINEAR_PANEL:
      return [
        { name: 'panel_width', label: 'Поле', type: 'number' },
        { name: 'groove', label: 'Руст', type: 'number' },
        { name: 'length', label: 'Длина', type: 'number' },
        { name: 'has_endcap', label: 'Наличие торцевания', type: 'checkbox' },
        { name: 'quantity', label: 'Количество панелей', type: 'number' },
      ]
    case ProductTypeEnum.SHEET:
      return []
    default:
      return [{ name: 'quantity', label: 'Количество', type: 'number' }]
  }
}

const productFields = computed(() => {
  if (!firstTask.value || !firstTask.value.product) return []
  return getProductFields(firstTask.value.product.type)
})

function formatDate(dateStr) {
  if (!dateStr) return '—'
  const date = new Date(dateStr)
  return date.toLocaleDateString()
}

async function fetchTask(id) {
  try {
    const response = await api.get(`/task/${id}`)
    task.value = response.data
  } catch (error) {
    console.error('Ошибка загрузки задачи:', error)
    alert('Не удалось загрузить задачу')
    router.push('/tasks')
  }
}

async function deleteTask(id) {
  if (!confirm('Удалить задачу?')) return
  try {
    await api.delete(`/task/${id}/delete`)
    alert('Задача удалена')
    router.push('/tasks')
  } catch (error) {
    console.error('Ошибка удаления:', error)
    alert('Не удалось удалить задачу')
  }
}

function goBack() {
  router.push('/tasks')
}

onMounted(() => {
  const taskId = route.params.id
  if (taskId) {
    fetchTask(taskId)
  } else {
    alert('ID задачи не указан')
    router.push('/tasks')
  }
})
</script>

<style scoped>
.form-group {
  margin-bottom: 1rem;
}
.form-control {
  width: 100%;
  padding: 0.5rem;
  font-size: 1rem;
}
</style>
