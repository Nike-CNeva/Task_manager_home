
<script setup>
import { decrypt } from '@/utils/crypto'
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import api from '@/utils/axios'
const showWeightInput = ref(false)
const showWasteInput = ref(false)
const newWeight = ref(null)
const newWaste = ref(null)
const route = useRoute()
const router = useRouter()
const task = ref(null)
const quantities = ref([])
const currentUser = ref(null)
const productType = computed(() => {
  const product = task.value?.tasks?.[0]?.task_products?.[0]?.product
  return product?.type || null
})
const fileInput = ref(null);

const triggerFileInput = () => {
  fileInput.value.click();
};
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
  if (task.value?.tasks?.[0]?.task_products?.length) {
  quantities.value = task.value.tasks[0].task_products.map(() => 0)
} else {
  quantities.value = []
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
  const encrypted = localStorage.getItem('user')
  if (encrypted) {
    try {
      currentUser.value = decrypt(encrypted)
      
    } catch (e) {
      console.error('Ошибка дешифровки пользователя:', e)
    }
  }

  const taskId = route.params.id
  if (taskId) {
    fetchTask(taskId)
  } else {
    alert('ID задачи не указан')
    router.push('/tasks')
  }
})
const newComment = ref('')
function canDeleteComment() {
  if (!currentUser.value) return false
  return (
    currentUser.value.user_type === 'Администратор'
  )
}
async function submitComment() {
  const trimmed = newComment.value.trim()
  if (!trimmed) {
    alert('Комментарий не может быть пустым.')
    return
  }

  try {
    const response = await api.post(`/tasks/${task.value.id}/comments`, {
      content: trimmed,
      bid_id: task.value.id
    })

    task.value.comments.push(response.data)
    newComment.value = ''
  } catch (error) {
    console.error('Ошибка добавления комментария:', error)
    alert('Не удалось отправить комментарий.')
  }
}
async function deleteComment(commentId) {
  if (!confirm('Удалить комментарий?')) return
  try {
    await api.delete(`/comments/${commentId}`)
    task.value.comments = task.value.comments.filter(c => c.id !== commentId)
    alert('Комментарий удалён')
  } catch (error) {
    console.error('Ошибка удаления комментария:', error)
    alert('Не удалось удалить комментарий.')
  }
}

async function updateMaterialField(fieldName, fieldValue) {
  try {
    const payload = {}

    if (fieldName === 'weight') {
      const currentWeight = Number(task.value.tasks[0].material.weight) || 0
      const newWeight = currentWeight + Number(fieldValue)
      payload[fieldName] = newWeight
    } else {
      payload[fieldName] = fieldValue
    }

    await api.patch(`/tasks/${task.value.tasks[0].id}/material`, payload)

    // Обновляем локальное состояние
    task.value.tasks[0].material[fieldName] = payload[fieldName]

    if (fieldName === 'weight') showWeightInput.value = false
    if (fieldName === 'waste') showWasteInput.value = false

    alert(`${fieldName === 'weight' ? 'Вес' : 'Отходность'} обновлена`)
  } catch (error) {
    console.error(`Ошибка обновления ${fieldName}:`, error)
    alert(`Не удалось обновить ${fieldName === 'weight' ? 'вес' : 'отходность'}.`)
  }
}
async function handleFileUpload(event) {
  const files = event.target.files
  if (!files.length) return

  const formData = new FormData()
  for (let file of files) {
    formData.append('files', file)
  }
  try {
    const response = await api.post(`/tasks/${task.value.id}/files`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
    task.value.files.push(...response.data)
    alert('Файлы загружены')
  } catch (error) {
    console.error('Ошибка загрузки файлов:', error)
    alert('Не удалось загрузить файлы.')
  }
}
async function updateTaskStatus(newStatus) {
  const taskId = task.value.tasks[0].id

  try {
    const response = await api.patch(`/tasks/${taskId}/status?new_status=${newStatus}`)

    const data = response.data

    // Обновляем статус задачи
    task.value.tasks[0].status = data.task_status

    const taskWorkshops = task.value.tasks[0].workshops;
    const responseWorkshops = response.data.workshops;

    for (let i = 0; i < taskWorkshops.length; i++) {
      const taskWorkshop = taskWorkshops[i];
      
      // Найти цех с таким же именем в response
      const matchedWorkshop = responseWorkshops.find(
        w => w.workshop_name === taskWorkshop.workshop_name
      );
      
      if (matchedWorkshop) {
        // Обновить статус
        taskWorkshop.status = matchedWorkshop.status;
      }
    }

  } catch (error) {
    console.error('Ошибка обновления статуса:', error)
    alert('Не удалось обновить статус.')
  }
}
const WORKSHOP_ORDER = [
  "Инженер",
  "Резка",
  "Координатка",
  "Гибка",
  "Прокат профилей",
  "Прокат клямеров",
  "Прокат кронштейнов",
  "Гибка удлинителей кронштейнов",
  "Покраска",
];

const canShowInWorkButton = computed(() => {
  if (
    !currentUser.value ||
    !task.value ||
    !task.value.tasks?.[0] ||
    !task.value.tasks[0].workshops
  ) return false;

  // получаем массив имён цехов пользователя
  const userWorkshopNames = currentUser.value.workshops.map(w => w.name);
  if (!userWorkshopNames.length) return false;

  const workshops = task.value.tasks[0].workshops;

  return userWorkshopNames.some(userWorkshop => {
    const curIndex = WORKSHOP_ORDER.indexOf(userWorkshop);
    if (curIndex === -1) return false;

    const workshopInfo = workshops.find(w => w.workshop_name === userWorkshop);
    if (!workshopInfo) return false;

    const status = workshopInfo.status;
    if (status !== "Новая" && status !== "На удержании") return false;

    // Проверяем предыдущий цех
    if (curIndex > 0) {
      const prevWorkshopName = WORKSHOP_ORDER[curIndex - 1];
      const prevWorkshopInfo = workshops.find(w => w.workshop_name === prevWorkshopName);
      if (prevWorkshopInfo && prevWorkshopInfo.status !== "Выполнена") return false;
    }

    return true;
  });
});
const showQuantityInput = ref(false)

async function submitQuantity() {
  const payload = quantities.value
    .map((qty, index) => ({
      product_id: task.value.tasks[0].task_products[index].product.id,
      quantity: qty,
    }))
    .filter(item => item.quantity > 0)  // отправляем только положительные значения

  if (!payload.length) {
    alert('Введите количество хотя бы для одного продукта.')
    return
  }

  try {
    // Замените URL и метод на свои
    await api.post(`/tasks/${task.value.tasks[0].id}/add_quantity`, { task_id: task.value.tasks[0].id, quantities: payload })
    alert('Количество успешно добавлено')
    showQuantityInput.value = false

    // Можно перезагрузить задачу или обновить локально done_quantity и т.п.
    fetchTask(task.value.tasks[0].id)

  } catch (error) {
    console.error('Ошибка при сохранении количества:', error)
    alert('Не удалось сохранить количество')
  }
}
const props = defineProps({
  task: Object
})

// Разбиваем файлы на блоки по 10
const chunkedFiles = computed(() => {
  const files = props.task.files || []
  const result = []
  for (let i = 0; i < files.length; i += 10) {
    result.push(files.slice(i, i + 10))
  }
  return result
})
</script>

<template>
  <div v-if="task" class="task-container">
    <!-- Боковая панель управления -->
    <aside class="sidebar">
      <h2>Управление 🛠️</h2>
      <button class="btn btn-secondary" @click="goBack">⬅️ Назад</button>
      <button v-if="canShowInWorkButton" class="btn btn-warning" @click="updateTaskStatus('В работе')">🚧 В работу</button>
      <button class="btn btn-success" @click="updateTaskStatus('Выполнена')">✅ Выполнена</button>
      <button class="btn btn-primary" @click="showQuantityInput = !showQuantityInput">➕ Кол-во</button>
      <button class="btn btn-secondary" @click="showWeightInput = true">⚖️ Вес</button>
      <button class="btn btn-secondary" @click="showWasteInput = true">♻️ Отходы</button>
      <button class="btn btn-secondary" @click="triggerFileInput">📎 Файлы</button>
      <input ref="fileInput" type="file" multiple style="display: none" @change="handleFileUpload" />
      <button class="btn btn-danger" @click="() => deleteTask(task.tasks[0].id)">🗑️ Удалить</button>
    </aside>

    <!-- Основной блок с деталями -->
    <main class="details">
      <h2>Детали задачи №{{ task.task_number }}</h2>

      <div v-if="showQuantityInput" class="input-block">
        <label>Введите количество готовой продукции:</label>
        <div v-for="(tp, index) in task.tasks[0]?.task_products || []" :key="tp.id">
          <p><strong>Продукт №{{ index + 1 }}</strong></p>
          <input type="number" v-model.number="quantities[index]" min="0" />
        </div>
        <button class="btn btn-success" @click="submitQuantity">Сохранить</button>
      </div>

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
      <p><strong>Готово:</strong> {{ task.tasks[0]?.done_quantity || '—' }}</p>

      <p><strong>Материал:</strong>
        <span v-if="task.tasks[0]?.material">
          {{ task.tasks[0].material.type }} {{ task.tasks[0].material.color }} {{ task.tasks[0].material.thickness }}
        </span>
        <span v-else>—</span>
      </p>

      <div v-if="showWeightInput" class="input-block">
        <label>Введите вес (в кг):</label>
        <input type="number" v-model="newWeight" />
        <button class="btn btn-primary" @click="updateMaterialField('weight', newWeight)">Сохранить</button>
      </div>

      <div v-if="showWasteInput" class="input-block">
        <label>Введите отходность (%):</label>
        <input type="number" v-model="newWaste" />
        <button class="btn btn-primary" @click="updateMaterialField('waste', newWaste)">Сохранить</button>
      </div>

      <p><strong>Вес:</strong> {{ task.tasks[0]?.material?.weight ?? '—' }} кг</p>
      <p><strong>Отходность:</strong> {{ task.tasks[0]?.material?.waste ?? '—' }} %</p>

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

      <div v-if="task?.files?.length">
        <h3>📁 Файлы:</h3>
        <div class="file-grid">
          <div
            v-for="(fileChunk, index) in chunkedFiles"
            :key="index"
            class="file-column"
          >
            <ul>
              <li v-for="file in fileChunk" :key="file.id">
                <a :href="file.url" target="_blank">{{ file.filename }}</a>
              </li>
            </ul>
          </div>
        </div>
      </div>
      <p v-else>Файлы не прикреплены.</p>
    </main>

    <!-- Комментарии -->
    <aside class="comments">
      <h3>💬 Комментарии</h3>
      <div v-if="task.comments?.length">
        <ul>
          <li v-for="comment in task.comments" :key="comment.id" class="comment-item">
            <div class="comment-header">
              <div class="comment-content">
                <p><strong>{{ comment.user.firstname }} {{ comment.user.name }}</strong> — {{ formatDate(comment.created_at) }}</p>
                <p>{{ comment.content }}</p>
              </div>
              <button v-if="canDeleteComment(comment)" @click="deleteComment(comment.id)" class="btn-delete-comment">✕</button>
            </div>
          </li>
        </ul>
      </div>
      <p v-else>Комментариев пока нет.</p>

      <div class="comment-form">
        <textarea v-model="newComment" rows="3" placeholder="Введите комментарий..."></textarea>
        <button class="btn btn-primary" @click="submitComment">Отправить</button>
      </div>
    </aside>
  </div>
  <div v-else>
    <p>Загрузка задачи...</p>
  </div>
</template>

<style scoped>
.file-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 16px;
}

.file-column ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.file-column li {
  margin-bottom: 6px;
}
.task-container {
  display: flex;
  flex-direction: row;
  gap: 24px;
  padding: 16px;
}
.sidebar {
  width: 220px;
  background: #f5f5f5;
  padding: 12px;
  border-radius: 8px;
  display: flex;
  flex-direction: column;
  gap: 10px;
}
.details {
  flex: 1;
  max-width: 800px;
}
.comments {
  width: 300px;
  background: #fafafa;
  padding: 12px;
  border-radius: 8px;
}
.btn {
  padding: 8px 12px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}
.input-block {
  margin: 16px 0;
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
.btn-secondary {
  background-color: #6c757d;
  color: white;
}
.btn-success {
  background-color: #28a745;
  color: white;
}
.btn-warning {
  background-color: #ffc107;
  color: black;
}
.btn-danger {
  background-color: red;
  color: white;
}
.comment-item {
  margin-bottom: 12px;
}
.comment-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
}
.btn-delete-comment {
  background-color: red;
  color: white;
  font-size: 12px;
  padding: 4px 6px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  height: 24px;
}
.btn-delete-comment:hover {
  background-color: darkred;
}
</style>
