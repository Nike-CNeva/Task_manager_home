<template>
  <div v-if="task">
    <h2>Детали задачи №{{ task.task_number }}</h2>

    <p><strong>Заказчик:</strong> {{ task.customer?.name || '—' }}</p>
    <p><strong>Менеджер:</strong> {{ task.manager || '—' }}</p>
    <p><strong>Тип продукции:</strong> {{ firstTask?.product?.type || '—' }}</p>
    <p><strong>Количество:</strong> {{ firstTask?.quantity || '—' }}</p>

    <p><strong>Материал:</strong>
      <span v-if="firstTask?.material">
        {{ firstTask.material.type }} {{ firstTask.material.color }} {{ firstTask.material.thickness }}
      </span>
      <span v-else>—</span>
    </p>

    <p><strong>Листы:</strong></p>
    <ul v-if="firstTask?.sheets?.length">
      <li v-for="sheet in firstTask.sheets" :key="sheet.id">
        {{ sheet.count }} листов {{ sheet.width }}x{{ sheet.length }}
      </li>
    </ul>
    <p v-else>—</p>

    <p><strong>Срочность:</strong> {{ firstTask?.urgency || '—' }}</p>
    <p><strong>Статус:</strong> {{ firstTask?.status || '—' }}</p>

    <p><strong>Статус цехов:</strong></p>
    <ul v-if="firstTask?.workshops?.length">
      <li v-for="ws in firstTask.workshops" :key="ws.workshop_name">
        {{ ws.workshop_name }}: {{ ws.status }}
      </li>
    </ul>
    <p v-else>—</p>

    <p><strong>Дата создания:</strong> {{ formatDate(firstTask?.created_at) }}</p>
    <p><strong>Дата завершения:</strong> {{ formatDate(firstTask?.completed_at) }}</p>

    <button class="btn btn-danger" @click="deleteTask(task.id)">Удалить задачу</button>
    <button class="btn btn-secondary" @click="goBack">← Назад к списку задач</button>
  </div>

  <div v-else>
    <p>Загрузка задачи...</p>
  </div>
</template>
<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import api from '@/utils/axios'

const route = useRoute()
const router = useRouter()

const task = ref(null)

// Поскольку задача всегда одна, достаём первую
const firstTask = computed(() => task.value?.tasks?.[0] || null)

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
    router.push('/tasks') // возврат к списку
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
p {
  font-size: 16px;
  margin: 8px 0;
}

.subtask-block {
  padding: 12px;
  border: 1px solid #ccc;
  border-radius: 8px;
  margin: 16px 0;
}
</style>
