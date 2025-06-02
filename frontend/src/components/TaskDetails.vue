<template>
  <div v-if="task">
    <h2>Детали задачи №{{ task.task_number }}</h2>
    <button class="btn btn-secondary" @click="goBack">← Назад к списку задач</button>

    <p><strong>Заказчик:</strong> {{ task.customer?.name || '—' }}</p>
    <p><strong>Менеджер:</strong> {{ task.manager || '—' }}</p>
    <p><strong>Тип продукции:</strong> {{ productType || '—' }}</p>

    <div v-for="(tp, index) in task.tasks[0]?.task_products || []" :key="index" class="subtask-block">
      <h3>Продукт №{{ index + 1 }}</h3>
      <ul v-if="tp.product_fields?.length">
        <li v-for="field in tp.product_fields" :key="field.name">
          <strong>{{ field.label }}:</strong> {{ getProductFieldValue(tp, field.name) }}
        </li>
      </ul>
    </div>

    <p><strong>Количество:</strong> {{ task.tasks[0]?.total_quantity || '—' }}</p>

    <p><strong>Материал:</strong>
      <span v-if="task.tasks[0]?.material">
        {{ task.tasks[0].material.type }} {{ task.tasks[0].material.color }} {{ task.tasks[0].material.thickness }}
      </span>
      <span v-else>—</span>
    </p>

    <p><strong>Листы:</strong></p>
    <ul v-if="task.tasks[0]?.sheets?.length">
      <li v-for="sheet in task.tasks[0].sheets" :key="sheet.id">
        {{ sheet.count }} листов {{ sheet.width }}x{{ sheet.length }}
      </li>
    </ul>
    <p v-else>—</p>

    <p><strong>Срочность:</strong> {{ task.tasks[0]?.urgency || '—' }}</p>
    <p><strong>Статус:</strong> {{ task.tasks[0]?.status || '—' }}</p>

    <p><strong>Статус цехов:</strong></p>
    <ul v-if="task.tasks[0]?.workshops?.length">
      <li v-for="ws in task.tasks[0].workshops" :key="ws.workshop_name">
        {{ ws.workshop_name }}: {{ ws.status }}
      </li>
    </ul>
    <p v-else>—</p>

    <p><strong>Дата создания:</strong> {{ formatDate(task.tasks[0]?.created_at) }}</p>
    <p><strong>Дата завершения:</strong> {{ formatDate(task.tasks[0]?.completed_at) }}</p>
    <!-- Комментарии -->
    <div v-if="task.comments?.length">
      <h3>Комментарии:</h3>
      <ul>
        <li v-for="comment in task.comments" :key="comment.id">
          <p><strong>{{ comment.author }}</strong> — {{ formatDate(comment.created_at) }}</p>
          <p>{{ comment.text }}</p>
        </li>
      </ul>
    </div>
    <p v-else>Комментариев пока нет.</p>

    <!-- Добавление нового комментария -->
    <div class="comment-form">
      <h3>Добавить комментарий</h3>
      <textarea v-model="newComment" rows="3" placeholder="Введите комментарий..."></textarea>
      <button class="btn btn-primary" @click="submitComment">Отправить</button>
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

const route = useRoute()
const router = useRouter()
const task = ref(null)

const productType = computed(() => {
  const product = task.value?.tasks?.[0]?.task_products?.[0]?.product
  return product?.type || null
})

function getProductFieldValue(taskProduct, fieldName) {
  const product = taskProduct.product
  const value =
    taskProduct[fieldName] ??
    product?.klamer?.[fieldName] ??
    product?.bracket?.[fieldName] ??
    product?.extension_bracket?.[fieldName] ??
    product?.cassette?.[fieldName] ??
    product?.profile?.[fieldName] ??
    product?.linear_panel?.[fieldName] ??
    '—'

  if (typeof value === 'boolean') return value ? 'Да' : 'Нет'
  return value ?? '—'
}

function formatDate(dateStr) {
  if (!dateStr) return '—'
  const date = new Date(dateStr)
  return date.toLocaleDateString()
}

async function fetchTask(id) {
  try {
    const response = await api.get(`/task/${id}`)
    task.value = response.data
    if (!task.value.comments) task.value.comments = []
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
const newComment = ref('')

async function submitComment() {
  const trimmed = newComment.value.trim()
  if (!trimmed) {
    alert('Комментарий не может быть пустым.')
    return
  }

  try {
    const response = await api.post(`/task/${task.value.id}/comments`, {
      text: trimmed
    })

    // Предполагаем, что сервер возвращает добавленный комментарий
    task.value.comments.push(response.data)
    newComment.value = ''
  } catch (error) {
    console.error('Ошибка добавления комментария:', error)
    alert('Не удалось отправить комментарий.')
  }
}
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
.btn {
  margin-bottom: 16px;
  padding: 8px 12px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}
.btn-secondary {
  background-color: #6c757d;
  color: white;
}
.comment-form {
  margin-top: 20px;
}

textarea {
  width: 100%;
  padding: 8px;
  font-size: 14px;
  margin-bottom: 8px;
  border-radius: 4px;
  border: 1px solid #ccc;
}

.btn-primary {
  background-color: #007bff;
  color: white;
}
</style>
