<template>
  <div v-if="task" class="task-details">
    <!-- Панель управления -->
    <div class="top-bar">
      <div class="left-buttons">
        <button class="btn btn-secondary" @click="goBack">← Назад</button>
        <button v-if="canShowInWorkButton" class="btn btn-warning" @click="updateTaskStatus('В работе')">В работу</button>
        <button class="btn btn-success" @click="updateTaskStatus('Выполнена')">Выполнена</button>
      </div>

      <div class="right-actions">
        <button class="btn btn-primary" @click="showQuantityInput = !showQuantityInput">➕ Количество</button>
        <button class="btn btn-secondary" @click="showWeightInput = true">⚖️ Вес</button>
        <button class="btn btn-secondary" @click="showWasteInput = true">♻️ Отходность</button>
        <button class="btn btn-secondary" @click="triggerFileInput">📎 Файлы</button>
        <input
          ref="fileInput"
          type="file"
          multiple
          accept=".jpg,.jpeg,.png,.pdf,.nc,.xls,.xlsx,.doc,.docx,.dxf,.dwg"
          @change="handleFileUpload"
          style="display: none"
        />
      </div>
    </div>

    <!-- Интерактивные поля -->
    <div class="input-panel" v-if="showQuantityInput">
      <h3>Добавить количество</h3>
      <div v-for="(tp, index) in task.tasks[0]?.task_products || []" :key="tp.id">
        <label>Продукт №{{ index + 1 }} (ID: {{ tp.id }}):</label>
        <input type="number" v-model.number="quantities[index]" min="0" />
      </div>
      <button class="btn btn-success" @click="submitQuantity">Сохранить</button>
    </div>

    <div v-if="showWeightInput" class="input-panel">
      <label>Вес (кг):</label>
      <input type="number" v-model="newWeight" />
      <button class="btn btn-primary" @click="updateMaterialField('weight', newWeight)">Сохранить</button>
    </div>

    <div v-if="showWasteInput" class="input-panel">
      <label>Отходность (%):</label>
      <input type="number" v-model="newWaste" />
      <button class="btn btn-primary" @click="updateMaterialField('waste', newWaste)">Сохранить</button>
    </div>

    <!-- Основные данные -->
    <div class="card">
      <h2>Задача №{{ task.task_number }}</h2>
      <p><strong>Заказчик:</strong> {{ task.customer?.name || '—' }}</p>
      <p><strong>Менеджер:</strong> {{ task.manager || '—' }}</p>
      <p><strong>Тип продукции:</strong> {{ productType || '—' }}</p>
      <p><strong>Статус:</strong> {{ task.tasks[0]?.status || '—' }}</p>
      <p><strong>Срочность:</strong> {{ task.tasks[0]?.urgency || '—' }}</p>
    </div>

    <!-- Продукты -->
    <div v-for="(tp, index) in task.tasks[0]?.task_products || []" :key="index" class="card">
      <h3>Продукт №{{ index + 1 }}</h3>
      <ul v-if="tp.product_fields?.length">
        <li v-for="field in tp.product_fields" :key="field.name">
          <strong>{{ field.label }}:</strong> {{ getProductFieldValue(tp, field.name) }}
        </li>
      </ul>
    </div>

    <!-- Материалы -->
    <div class="card">
      <h3>Материалы</h3>
      <p><strong>Материал:</strong>
        <span v-if="task.tasks[0]?.material">
          {{ task.tasks[0].material.type }} {{ task.tasks[0].material.color }} {{ task.tasks[0].material.thickness }}
        </span>
        <span v-else>—</span>
      </p>
      <p><strong>Вес:</strong> {{ task.tasks[0]?.material?.weight ?? '—' }} кг</p>
      <p><strong>Отходность:</strong> {{ task.tasks[0]?.material?.waste ?? '—' }} %</p>
      <p><strong>Количество:</strong> {{ task.tasks[0]?.total_quantity || '—' }}</p>
      <p><strong>Готово:</strong> {{ task.tasks[0]?.done_quantity || '—' }}</p>
    </div>

    <!-- Листы -->
    <div class="card">
      <h3>Листы</h3>
      <ul v-if="task.tasks[0]?.sheets?.length">
        <li v-for="sheet in task.tasks[0].sheets" :key="sheet.id">
          {{ sheet.count }} листов {{ sheet.width }}x{{ sheet.length }}
        </li>
      </ul>
      <p v-else>—</p>
    </div>

    <!-- Цеха -->
    <div class="card">
      <h3>Статус по цехам</h3>
      <ul v-if="task.tasks[0]?.workshops?.length">
        <li v-for="ws in task.tasks[0].workshops" :key="ws.workshop_name">
          {{ ws.workshop_name }}: {{ ws.status }}
        </li>
      </ul>
      <p v-else>—</p>
    </div>

    <!-- Даты -->
    <div class="card">
      <p><strong>Создана:</strong> {{ formatDate(task.tasks[0]?.created_at) }}</p>
      <p><strong>Завершена:</strong> {{ formatDate(task.tasks[0]?.completed_at) }}</p>
    </div>

    <!-- Файлы -->
    <div class="card">
      <h3>Файлы</h3>
      <ul v-if="task.files?.length">
        <li v-for="file in task.files" :key="file.id">
          <a :href="file.url" target="_blank">{{ file.filename }}</a>
        </li>
      </ul>
      <p v-else>Файлы не прикреплены.</p>
    </div>

    <!-- Комментарии -->
    <div class="card">
      <h3>Комментарии</h3>
      <ul v-if="task.comments?.length">
        <li v-for="comment in task.comments" :key="comment.id">
          <p><strong>{{ comment.user.firstname }} {{ comment.user.name }}</strong> — {{ formatDate(comment.created_at) }}</p>
          <p>{{ comment.content }}</p>
          <button
            v-if="canDeleteComment(comment)"
            @click="deleteComment(comment.id)"
            class="btn-delete-comment"
          >✕</button>
        </li>
      </ul>
      <p v-else>Комментариев пока нет.</p>
      <div class="comment-form">
        <textarea v-model="newComment" rows="3" placeholder="Введите комментарий..."></textarea>
        <button class="btn btn-primary" @click="submitComment">Отправить</button>
      </div>
    </div>

    <!-- Удаление -->
    <div class="delete-panel">
      <button class="btn btn-danger" @click="() => deleteTask(task.tasks[0].id)">Удалить задачу</button>
    </div>
  </div>

  <div v-else>
    <p>Загрузка задачи...</p>
  </div>
</template>
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
</script>


<style scoped>
h2, h3 {
  margin-top: 1rem;
  margin-bottom: 0.5rem;
  color: #333;
}

.top-buttons {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-bottom: 1rem;
}

.quantity-input-block,
.comment-form,
.subtask-block {
  margin-top: 1rem;
  padding: 1rem;
  background: #f9f9f9;
  border: 1px solid #ddd;
  border-radius: 8px;
}

.quantity-for-product {
  margin-bottom: 0.5rem;
}

input[type="number"],
textarea {
  width: 100%;
  padding: 0.4rem;
  margin-top: 0.3rem;
  margin-bottom: 0.6rem;
  border: 1px solid #ccc;
  border-radius: 6px;
}

.btn {
  padding: 0.4rem 0.8rem;
  border: none;
  border-radius: 6px;
  cursor: pointer;
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
  background-color: #dc3545;
  color: white;
}

.comment-item {
  margin-bottom: 1rem;
  background: #f2f2f2;
  border-left: 4px solid #007bff;
  padding: 0.5rem;
  border-radius: 6px;
  position: relative;
}

.comment-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
}

.btn-delete-comment {
  background: transparent;
  border: none;
  font-size: 1rem;
  color: #888;
  cursor: pointer;
  position: absolute;
  top: 5px;
  right: 10px;
}

ul {
  padding-left: 1.2rem;
}

ul li {
  margin-bottom: 0.4rem;
}

a {
  color: #007bff;
  text-decoration: none;
}

a:hover {
  text-decoration: underline;
}
</style>