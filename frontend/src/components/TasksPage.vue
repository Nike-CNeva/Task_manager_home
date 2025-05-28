<template>
  <div>
    <h2 class="my-4">Список задач</h2>
    <!-- Лоадер -->
    <div v-if="loading" class="text-center my-4">
      <div class="spinner-border" role="status">
        <span class="visually-hidden">Загрузка...</span>
      </div>
      <p>Загрузка данных...</p>
    </div>
    <table v-else class="table table-striped table-hover sortable">
      <thead>
        <tr>
          <th @click="sortBy('task_number')">№</th>
          <th @click="sortBy('customer.name')">Заказчик</th>
          <th @click="sortBy('manager')">Менеджер</th>
          <th @click="sortBy('product.type')">Тип продукции</th>
          <th @click="sortBy('quantity')">Количество</th>
          <th class="no-sort">Материал</th>
          <th class="no-sort">Листы</th>
          <th @click="sortBy('urgency')">Срочность</th>
          <th @click="sortBy('status')">Статус</th>
          <th class="no-sort">Статус цехов</th>
          <th @click="sortBy('created_at')">Дата создания</th>
          <th @click="sortBy('completed_at')">Дата завершения</th>
          <th class="no-sort">Действия</th>
        </tr>
      </thead>
      <tbody>
        <tr
          v-for="task in sortedTasks"
          :key="task.id"
          @click="goToTask(task.id)"
          style="cursor: pointer;"
        >
          <td>{{ task.task_number }}</td>
          <td>{{ task.customer.name }}</td>
          <td>{{ task.manager }}</td>
          <td>{{ task.product.type }}</td>
          <td>{{ task.quantity }}</td>
          <td>
            <template v-if="task.material">
              {{ task.material.type }} {{ task.material.color }} {{ task.material.thickness }}
            </template>
            <span v-else class="text-muted">—</span>
          </td>
          <td>
            <ul v-if="task.sheets && task.sheets.length" class="mb-0 ps-3">
              <li v-for="sheet in task.sheets" :key="sheet.id">
                {{ sheet.count }} листов {{ sheet.width }}x{{ sheet.length }}
              </li>
            </ul>
            <span v-else class="text-muted">—</span>
          </td>
          <td>{{ task.urgency }}</td>
          <td>{{ task.status }}</td>
          <td>
            <ul v-if="task.workshops && task.workshops.length" class="mb-0 ps-3">
              <li v-for="ws in task.workshops" :key="ws.workshop_name">
                {{ ws.workshop_name }}: {{ ws.status }}
              </li>
            </ul>
            <span v-else class="text-muted">—</span>
          </td>
          <td>{{ formatDate(task.created_at) }}</td>
          <td>{{ formatDate(task.completed_at) }}</td>
          <td @click.stop>
            <button class="btn btn-sm btn-danger" @click="deleteTask(task.id)">Удалить</button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import api from '@/utils/axios'
import { useRouter } from 'vue-router'

const router = useRouter()
const rawBids = ref([])
const tasks = ref([])
const loading = ref(true)
const sortKey = ref('')
const sortAsc = ref(true)

onMounted(async () => {
  loading.value = true
  try {
    const response = await api.get('/tasks')
    rawBids.value = response.data

    // Преобразуем bid.tasks в один плоский массив с дополнительной инфой
    tasks.value = rawBids.value.flatMap(bid =>
      bid.tasks.map(task => ({
        ...task,
        task_number: bid.task_number,
        customer: bid.customer,
        manager: bid.manager,
      }))
    )
  } catch (error) {
    console.error('Ошибка загрузки задач:', error)
  } finally {
    loading.value = false
  }
})

function formatDate(dateStr) {
  if (!dateStr) return '—'
  const date = new Date(dateStr)
  return date.toLocaleDateString()
}

function sortBy(key) {
  if (sortKey.value === key) {
    sortAsc.value = !sortAsc.value
  } else {
    sortKey.value = key
    sortAsc.value = true
  }
}

const sortedTasks = computed(() => {
  if (!sortKey.value) return tasks.value

  const getValue = (obj, path) =>
    path.split('.').reduce((o, p) => (o ? o[p] : ''), obj)

  return [...tasks.value].sort((a, b) => {
    const valA = getValue(a, sortKey.value)
    const valB = getValue(b, sortKey.value)

    const isNumber = !isNaN(valA) && !isNaN(valB)
    if (isNumber) {
      return sortAsc.value ? valA - valB : valB - valA
    }

    return sortAsc.value
      ? String(valA).localeCompare(String(valB))
      : String(valB).localeCompare(String(valA))
  })
})

function goToTask(id) {
  router.push(`/tasks/${id}`)
}

async function deleteTask(id) {
  if (!confirm('Удалить задачу?')) return

  try {
    await api.delete(`/task/${id}/delete`)
    tasks.value = tasks.value.filter(t => t.id !== id)
    alert('Задача удалена')
  } catch (err) {
    console.error('Ошибка удаления:', err)
    alert('Не удалось удалить задачу')
  }
}
</script>


<style scoped>
table {
  width: 100%;
  border-collapse: collapse;
}
thead {
  background-color: #f0f0f0;
}
th, td {
  border: 1px solid #ccc;
  padding: 8px;
  text-align: left;
}
th {
  cursor: pointer;
}
h2 {
  margin-bottom: 16px;
}
.text-muted {
  color: #888;
}
</style>
