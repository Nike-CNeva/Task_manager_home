
<script setup>
import { decrypt } from '@/utils/crypto'
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useStore } from 'vuex';
import api from '@/utils/axios'
const store = useStore();
const fromWaste = ref(false)
const showWeightInput = ref(false)
const showWasteInput = ref(false)
const showSheetInput = ref(false)
const newWidth = ref(null)
const newLength = ref(null)
const newSheetCount = ref(null)
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

async function updateMaterialField(fieldName, fieldValue, fromWaste = null) {
  try {
    const payload = {}

    if (fieldName === 'weight') {
      payload.weight = Number(fieldValue)
      payload.from_waste = !!fromWaste
    } else {
      payload[fieldName] = fieldValue
    }

    await api.patch(`/tasks/${task.value.tasks[0].id}/material`, payload)

    // Обновим локально (при необходимости, или просто перезагрузим задачу)
    if (fieldName === 'waste') {
      task.value.tasks[0].material.waste = fieldValue
    }
    if (fieldName === 'weight') {
      task.value.tasks[0].material.weights.push({
        id: Date.now(), // временный ID
        weight: Number(fieldValue),
        from_waste: !!fromWaste,
      })
    }
    // Закрываем форму
    if (fieldName === 'weight') showWeightInput.value = false
    if (fieldName === 'waste') showWasteInput.value = false

    // Уведомление
    const labels = {
      weight: 'Вес',
      from_waste: 'Флаг "из отходов"',
      waste: 'Отходность'
    }

    alert(`${labels[fieldName] || fieldName} обновлён(а)`)
  } catch (error) {
    console.error(`Ошибка обновления ${fieldName}:`, error)

    const labels = {
      weight: 'вес',
      from_waste: 'флаг "из отходов"',
      waste: 'отходность'
    }

    alert(`Не удалось обновить ${labels[fieldName] || fieldName}.`)
  }
}

async function handleFileUpload(event) {
  const files = event.target.files
  if (!files.length) return

  const formData = new FormData()
  for (let file of files) {
    formData.append('files', file)
  }
  formData.append('task_id', task.value.tasks[0].id)
  try {
    const response = await api.post(`/tasks/${task.value.id}/files`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
    task.value.files.push(...response.data)
    alert('Файлы загружены')
    await fetchTask(task.value.tasks[0].id)
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
// Цехи, которым можно начинать при статусе "В работе" у предыдущего
const ALLOWED_IF_PREV_IN_PROGRESS = ["Координатка", "Гибка", "Покраска"];

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
  ) {
    return false;
  }

  const workshops = task.value.tasks[0].workshops;
  const allAreNew = workshops.every(w => w.status === "Новая");

  if (allAreNew) {
    const firstNewWorkshopName = WORKSHOP_ORDER.find(orderName =>
      workshops.some(w => w.workshop_name === orderName && w.status === "Новая")
    );
    const hasAccess = store.getters.hasWorkshop([firstNewWorkshopName]);
    return !!firstNewWorkshopName && hasAccess;
  }

  for (let i = 0; i < WORKSHOP_ORDER.length; i++) {
    const workshopName = WORKSHOP_ORDER[i];
    const workshopInfo = workshops.find(w => w.workshop_name === workshopName);
    if (!workshopInfo) continue;

    if (workshopInfo.status !== "Новая" && workshopInfo.status !== "На удержании") continue;

    // Проверка предыдущих цехов
    let prevIsReady = true;
    if (ALLOWED_IF_PREV_IN_PROGRESS.includes(workshopName)) {
      // Только ближайший предыдущий
      const prevWorkshopName = WORKSHOP_ORDER[i - 1];
      const prevWorkshop = workshops.find(w => w.workshop_name === prevWorkshopName);
      prevIsReady =
        !prevWorkshop || ["В работе", "Выполнена"].includes(prevWorkshop.status);
    } else {
      // Все предыдущие должны быть завершены
      prevIsReady = WORKSHOP_ORDER.slice(0, i).every(prevName => {
        const prevWorkshop = workshops.find(w => w.workshop_name === prevName);
        return !prevWorkshop || prevWorkshop.status === "Выполнена";
      });
    }

    if (!prevIsReady) continue;

    const hasAccess = store.getters.hasWorkshop([workshopName]);
    if (hasAccess) return true;
  }

  return false;
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


// Разбиваем файлы на блоки по 10
const chunkedFiles = computed(() => {
  const files = task.value.files || []
  const result = []
  for (let i = 0; i < files.length; i += 10) {
    result.push(files.slice(i, i + 10))
  }
  return result
})
async function submitSheet() {
  try {
    const payload = {
      task_id: task.value.tasks[0].id,
      width: newWidth.value,
      length: newLength.value,
      quantity: newSheetCount.value
    }

    const response = await api.post(`/tasks/${payload.task_id}/sheets`, payload)

    task.value.tasks[0].sheets.push(response.data)
    alert('Лист добавлен')
    showSheetInput.value = false
  } catch (error) {
    console.error('Ошибка добавления листа:', error)
    alert('Не удалось добавить лист.')
  }
}
function removeSheet(taskId, sheetId) {
  api
    .delete(`/tasks/${taskId}/sheets/${sheetId}`)
    .then(() => {
      // Удаляем лист на фронте
      const sheets = task.value.tasks[0].sheets;
      task.value.tasks[0].sheets = sheets.filter(sheet => sheet.id !== sheetId);
    })
    .catch((error) => {
      console.error('Ошибка при удалении листа:', error);
      // Можно вывести уведомление пользователю
    });
}

async function downloadAllAsZip() {
  try {
    const response = await api.get(`/tasks/${task.value.id}/files/zip`, {
      responseType: "blob",
    });
    const blob = new Blob([response.data], { type: "application/zip" });
    const link = document.createElement("a");
    link.href = URL.createObjectURL(blob);
    link.download = `bid_${task.value.id}_files.zip`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  } catch (error) {
    console.error("Ошибка при скачивании архива:", error);
    alert("Ошибка при скачивании архива.");
  }
}
const deleteFile = async (file) => {
  if (!confirm(`Удалить файл "${file.filename}"?`)) return;

  try {
    await api.delete(`/files/${file.id}`);
    task.value.files = task.value.files.filter(f => f.id !== file.id);
  } catch (error) {
    console.error("Ошибка при удалении файла:", error);
    alert("Не удалось удалить файл.");
  }
};

import { saveAs } from "file-saver";

const openFile = async (file) => {
  const fileName = file.filename;
  const bidId = file.bid_id;
  const fileExt = fileName.split('.').pop().toLowerCase();

  const browserSupportedExt = new Set(['jpg', 'jpeg', 'png', 'pdf', 'gif', 'webp', 'txt', 'html', 'mp4', 'webm', 'ogg', 'mp3']);

  try {
    const response = await api.get(`/uploads/${bidId}/${encodeURIComponent(fileName)}`, {
      responseType: 'blob',
    });

    if (browserSupportedExt.has(fileExt)) {
      // Попробуем взять MIME из заголовков ответа
      const mimeType = response.headers['content-type'] || `application/octet-stream`;
      const blob = new Blob([response.data], { type: mimeType });
      const blobUrl = URL.createObjectURL(blob);

      window.open(blobUrl, '_blank');

      // Можно добавить revokeObjectURL после небольшой задержки, чтобы не утекала память
      setTimeout(() => URL.revokeObjectURL(blobUrl), 10000);
    } else {
      saveAs(response.data, fileName);
    }
  } catch (error) {
    console.error('Ошибка при открытии файла:', error);
    alert('Не удалось открыть файл. Возможно, истёк срок действия авторизации.');
  }
};
const taskWorkshopNames = computed(() => {
  const ws = task.value?.tasks?.[0]?.workshops;
  if (Array.isArray(ws)) {
    return ws.map(w => w.workshop_name);
  }
  
  return [];
});

const hasWorkshopInProgress = computed(() => {
  if (
    !currentUser.value ||
    !task.value ||
    !task.value.tasks?.[0] ||
    !task.value.tasks[0].workshops
  ) return false;

  const workshops = task.value.tasks[0].workshops;
  const userWorkshopNames = currentUser.value.workshops.map(w => w.name);

  // Ищем хотя бы один цех у задачи со статусом "В работе",
  // который совпадает с цехом пользователя
  return workshops.some(w => 
    w.status === "В работе" && userWorkshopNames.includes(w.workshop_name)
  );
});
const isTaskReadyEngineer = computed(() => {
  if (!Array.isArray(task.value.tasks)) {
    return false
  }

  if (task.value.tasks.length === 0) {
    return false
  }

  const firstTask = task.value.tasks[0]

  if (!firstTask) {
    return false
  }

  if (!Array.isArray(firstTask.sheets)) {
    return false
  }

  const hasSheets = firstTask.sheets.length > 0

  if (!Array.isArray(task.value.files)) {
  return false
}

const hasNcFiles = task.value.files.some(file => {
  const res = typeof file.filename === 'string' && file.filename.toLowerCase().endsWith('.nc')
  return res
})

const result = hasSheets && hasNcFiles

return result
})


const isTaskReadyCutting = computed(() => {
  if (!Array.isArray(task.value.tasks) || task.value.tasks.length === 0) {
    return false
  }

  const weight = task.value.tasks[0].material?.weights

  return Array.isArray(weight) && weight.length > 0
})

const isTaskQuantityReady = computed(() => {
  const tasks = task.value.tasks

  if (!Array.isArray(tasks) || tasks.length === 0) {
    return false
  }

  const currentTask = tasks[0]

  // Проверяем количество
  const isQuantityComplete = currentTask.done_quantity === currentTask.total_quantity

  return isQuantityComplete
})

const arePreviousWorkshopsDone = computed(() => {
  const workshops = task.value.tasks[0].workshops
  const userWorkshops = currentUser.value?.workshops || []
  if (!Array.isArray(workshops) || !Array.isArray(userWorkshops)) {
    return false
  }

  // Находим самый ранний цех пользователя по порядку
  const userWorkshopIndexes = userWorkshops
    .map(w => WORKSHOP_ORDER.indexOf(w.name))
    .filter(index => index !== -1)

  if (userWorkshopIndexes.length === 0) return false

  const minUserIndex = Math.min(...userWorkshopIndexes)

  // Все предыдущие цеха до первого пользовательского должны быть "Выполнена"
  const requiredWorkshopNames = WORKSHOP_ORDER.slice(0, minUserIndex)

  return requiredWorkshopNames.every(name =>
    workshops.some(w => w.workshop_name === name && w.status === "Выполнена")
  )
})

const shouldShowSection = computed(() => {
  if (store.getters.hasRole('Инженер')) {
    return isTaskReadyEngineer.value && hasWorkshopInProgress.value
    } else if (store.getters.hasWorkshop(['Резка'])) {
    return isTaskReadyCutting.value && hasWorkshopInProgress.value
    } else if (store.getters.hasWorkshop(['Гибка'])) {
    return isTaskQuantityReady.value && hasWorkshopInProgress.value && arePreviousWorkshopsDone.value
  } else {
    return store.getters.hasWorkshop(taskWorkshopNames.value) && hasWorkshopInProgress.value
  }
})

const sortedWorkshops = computed(() => {
  const workshops = task.value?.tasks?.[0]?.workshops || []
  return WORKSHOP_ORDER
    .map(name => workshops.find(ws => ws.workshop_name === name))
    .filter(Boolean) // убираем undefined, если цеха нет в задаче
})

</script>

<template>
  <div v-if="task" class="task-container">
    <!-- Боковая панель управления -->
    <aside class="sidebar">
      <h2>Управление 🛠️</h2>
      <button class="btn btn-secondary" @click="goBack">⬅️ Назад</button>

      <button v-if="canShowInWorkButton" class="btn btn-warning" @click="updateTaskStatus('В работе')">🚧 В работу</button>

      <button v-if="shouldShowSection" class="btn btn-success" @click="updateTaskStatus('Выполнена')">✅ Выполнена</button>
      <button v-if="hasWorkshopInProgress && $store.getters.hasWorkshop(['Гибка']) && !isTaskQuantityReady" class="btn btn-primary" @click="showQuantityInput = !showQuantityInput">➕ Кол-во</button>
      <div v-if="showQuantityInput" class="input-block">
        <label>Введите количество готовой продукции:</label>
        <div v-for="(tp, index) in task.tasks[0]?.task_products || []" :key="tp.id">
          <p><strong>Продукт №{{ index + 1 }}</strong></p>
          <input type="number" v-model.number="quantities[index]" min="0" />
        </div>
        <button class="btn btn-success" @click="submitQuantity">Сохранить</button>
      </div>

      <button v-if="$store.getters.hasWorkshop(['Резка']) && hasWorkshopInProgress" class="btn btn-secondary" @click="showWeightInput = true">⚖️ Вес</button>
      <div v-if="showWeightInput" class="input-block">
        <label>Введите вес (в кг):</label>
        <input type="number" v-model="newWeight" />

        <label>
          <input type="checkbox" v-model="fromWaste" />
          Из отходов
        </label>

        <button class="btn btn-primary" @click="updateMaterialField('weight', newWeight, fromWaste)">Сохранить</button>
      </div>

      <button v-if="hasWorkshopInProgress && ( $store.getters.hasRole('Администратор') || $store.getters.hasRole('Инженер') )" class="btn btn-secondary" @click="showWasteInput = true">♻️ Отходы</button>
      <div v-if="showWasteInput" class="input-block">
        <label>Введите отходность (%):</label>
        <input type="number" v-model="newWaste" />
        <button class="btn btn-primary" @click="updateMaterialField('waste', newWaste)">Сохранить</button>
      </div>
      
      <button v-if="hasWorkshopInProgress && ( $store.getters.hasRole('Администратор') || $store.getters.hasRole('Инженер') )" class="btn btn-secondary" @click="showSheetInput = true">📄 Листы</button>
      <div v-if="showSheetInput" class="input-block">
        <label>Введите ширину листа (мм):</label>
        <input type="number" v-model="newWidth" />
        <label>Введите длину листа (мм):</label>
        <input type="number" v-model="newLength" />
        <label>Введите количество листов:</label>
        <input type="number" v-model="newSheetCount" />
        <button class="btn btn-primary" @click="submitSheet">Сохранить</button>
      </div>

      <button v-if="$store.getters.hasRole('Администратор') || $store.getters.hasRole('Инженер')" class="btn btn-secondary" @click="triggerFileInput">📎 Файлы</button>
      <input ref="fileInput" type="file" multiple style="display: none" @change="handleFileUpload" />

      <button v-if="$store.getters.hasRole('Администратор')" class="btn btn-danger" @click="() => deleteTask(task.tasks[0].id)">🗑️ Удалить</button>
    </aside>

    <!-- Основной блок с деталями -->
    <main class="details">
      <h2>Детали задачи №{{ task.task_number }}</h2>

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

      <p v-if="!$store.getters.hasRole('Инженер') && !$store.getters.hasWorkshop(['Резка', 'Координатка'])"><strong>Готово:</strong> {{ task.tasks[0]?.done_quantity || '—' }}</p>

      <p><strong>Материал:</strong></p>
      <p>
        <span v-if="task.tasks[0]?.material">
          {{ task.tasks[0].material.type }} {{ task.tasks[0].material.color }} {{ task.tasks[0].material.thickness }}
        </span>
        <span v-else>—</span>
      </p>

      <p v-if="!$store.getters.hasRole('Инженер') && !$store.getters.hasWorkshop(['Гибка', 'Координатка'])">
        <strong>Вес:</strong>
      </p>
      <p v-if="!$store.getters.hasRole('Инженер') && !$store.getters.hasWorkshop(['Гибка', 'Координатка'])">
        <span v-if="task.tasks[0]?.material?.weights?.length">
          <span v-for="(w, index) in task.tasks[0].material.weights" :key="w.id">
            {{ w.weight }} кг<span v-if="w.from_waste"> (из отходов)</span><span v-if="index !== task.tasks[0].material.weights.length - 1"><br> </span>
          </span>
        </span>
        <span v-else>—</span>
      </p>
      <p v-if="$store.getters.hasRole('Инженер') || $store.getters.hasRole('Администратор')">
        <strong>Отходность:</strong>
        {{ task.tasks[0]?.material?.waste != null ? task.tasks[0].material.waste.toFixed(1) : '—' }} %
      </p>
      <div v-if="$store.getters.hasRole('Инженер') || $store.getters.hasRole('Администратор') || $store.getters.hasWorkshop(['Резка', 'Координатка'])">
        <p><strong>Листы:</strong></p>
        <ul v-if="task.tasks[0]?.sheets?.length">
          <li 
            v-for="sheet in [...task.tasks[0].sheets].sort((a, b) => {
              if (b.length !== a.length) {
                return b.length - a.length
              }
              return b.width - a.width
            })"
            :key="sheet.id"
            style="display: flex; align-items: center; gap: 8px;"
          >
            <span>{{ sheet.count }} листов {{ sheet.width }}x{{ sheet.length }}</span>
            <button 
              v-if="$store.getters.hasRole('Администратор') || $store.getters.hasRole('Инженер')"
              @click="removeSheet(task.tasks[0].id, sheet.id)" 
              style="background: none; border: none; color: red; font-weight: bold; cursor: pointer;"
            >
              ❌
            </button>
          </li>
        </ul>
        <p v-else>—</p>
      </div>
      <p><strong>Срочность:</strong> {{ task.tasks[0]?.urgency || '—' }}</p>

      <p v-if="$store.getters.hasRole('Администратор')"><strong>Статус:</strong> {{ task.tasks[0]?.status || '—' }}</p>

      <p><strong>Статус цехов:</strong></p>
      <ul v-if="sortedWorkshops.length">
        <li v-for="ws in sortedWorkshops" :key="ws.workshop_name">
          {{ ws.workshop_name }}: {{ ws.status }}
        </li>
      </ul>
      <p v-else>—</p>

      <p><strong>Дата создания:</strong> {{ formatDate(task.tasks[0]?.created_at) }}</p>

      <p><strong>Дата завершения:</strong> {{ formatDate(task.tasks[0]?.completed_at) }}</p>

      <div v-if="task?.files?.length">
        <details class="files-block">
          <summary>📁 Файлы ({{ task.files.length }})</summary>
          <div class="mt-2">
            <button @click="downloadAllAsZip" class="btn">📦 Скачать архивом</button>
            <div class="file-grid mt-2">
              <div
                v-for="(fileChunk, index) in chunkedFiles"
                :key="index"
                class="file-column"
              >
                <ul>
                  <li v-for="file in fileChunk" :key="file.id" class="file-row">
                    <span @click="openFile(file)" class="clickable-filename">📄 {{ file.filename }}</span>
                    <button v-if="$store.getters.hasRole('Администратор')" @click="deleteFile(file)" class="btn btn-sm">❌</button>
                  </li>
                </ul>
              </div>
            </div>
          </div>
        </details>
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
              <button v-if="$store.getters.hasRole('Администратор')" @click="deleteComment(comment.id)" class="btn-delete-comment">❌</button>
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
.clickable-filename {
  cursor: pointer;
  color: #3b3b3b;
  text-decoration: underline;
  transition: color 0.2s;
}

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
  background-color: #adc7df;
  color: black;
}
.btn-secondary {
  background-color: #cfcfcf;
  color: black;
}
.btn-success {
  background-color: #aad4c8;
  color: black;
}
.btn-warning {
  background-color: #ffefc7;
  color: black;
}
.btn-danger {
  background-color: rgb(239,161,140);
  color: black;
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
  background-color: rgb(239,161,140);
  color: white;
  font-size: 12px;
  padding: 4px 6px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  height: 24px;
}

</style>
