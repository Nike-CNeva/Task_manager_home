<template>
  <div>
    <h2 class="my-4">Список заявок</h2>

    <div v-if="loading" class="text-center my-4">
      <div class="spinner-border" role="status">
        <span class="visually-hidden">Загрузка...</span>
      </div>
      <p>Загрузка данных...</p>
    </div>

    <div v-else>
      <div
        v-for="(bid, index) in rawBids"
        :key="bid.id"
        class="mb-3 border rounded"
      >
        <!-- Заголовок заявки с динамичным цветом -->
        <div
          class="p-3"
          :style="{ backgroundColor: getBidBackground(bid) }"
          @click="toggle(index)"
          style="cursor: pointer;"
        >
          <strong>Заявка №{{ bid.task_number }}</strong> — {{ bid.customer.name }} (Менеджер: {{ bid.manager }}) Прогресс: {{ calculateBidProgress(bid).toFixed(1) }}%

        </div>
        <!-- Список задач -->
        <div v-show="expandedIndex === index" class="p-3">
          <table class="table table-bordered table-sm">
            <thead>
              <tr>
                <th>Продукция</th>
                <th>Цвет</th>
                <th>Кол-во</th>
                <th>Покраска</th>
                <th>Материал</th>
                <th>Листы</th>
                <th>Срочность</th>
                <th>Прогресс</th>
                <th>Статус</th>
                <th>Цеха</th>
                <th>Создано</th>
                <th>Завершено</th>
              </tr>
            </thead>
            <tbody>
              <template v-for="task in bid.tasks" :key="task.id">
                <tr>
                  <td
                    colspan="12"
                    @click="goToTask(task.id)"
                    :style="{ backgroundColor: getTaskBackground(task), cursor: 'pointer' }"
                  >
                  <strong>Задача №{{ task.id }}</strong> — Всего: {{ task.total_quantity }}, Выполнено: {{ task.done_quantity }} ({{ calculateTaskProgress(task).toFixed(1) }}%)

                  </td>
                </tr>

                <tr
                  v-for="(tp, i) in task.task_products || []"
                  :key="`${task.id}-${i}`"
                  @click="goToTask(task.id)"
                  style="cursor: pointer;"
                >
                  <td :style="{ backgroundColor: getTaskBackground(task), cursor: 'pointer' }">{{ tp.product.type }} — {{ tp.product.cassette?.description || '—' }}</td>
                  <td :style="{ backgroundColor: getTaskBackground(task), cursor: 'pointer' }">{{ tp.color }}</td>
                  <td :style="{ backgroundColor: getTaskBackground(task), cursor: 'pointer' }">{{ tp.quantity }}</td>
                  <td :style="{ backgroundColor: getTaskBackground(task), cursor: 'pointer' }">{{ tp.painting ? 'Да' : 'Нет' }}</td>
                  <td :style="{ backgroundColor: getTaskBackground(task), cursor: 'pointer' }">
                    <template v-if="task.material">
                      {{ task.material.type }} {{ task.material.color }} {{ task.material.thickness }}
                    </template>
                    <span v-else class="text-muted">—</span>
                  </td>
                  <td :style="{ backgroundColor: getTaskBackground(task), cursor: 'pointer' }">
                    <ul v-if="task.sheets?.length" class="mb-0 ps-3">
                      <li v-for="sheet in task.sheets" :key="sheet.id">
                        {{ sheet.count }} листов {{ sheet.width }}x{{ sheet.length }}
                      </li>
                    </ul>
                    <span v-else class="text-muted">—</span>
                  </td>
                  <td :style="{ backgroundColor: getTaskBackground(task), cursor: 'pointer' }">{{ task.urgency }}</td>
                  <td :style="{ backgroundColor: getTaskBackground(task), cursor: 'pointer' }">{{ task.progress_percent }}%</td>
                  <td :style="{ backgroundColor: getTaskBackground(task), cursor: 'pointer' }">{{ task.status }}</td>
                  <td :style="{ backgroundColor: getTaskBackground(task), cursor: 'pointer' }">
                    <ul v-if="task.workshops?.length" class="mb-0 ps-3">
                      <li v-for="ws in task.workshops" :key="ws.workshop_name">
                        {{ ws.workshop_name }}: {{ ws.status }}
                      </li>
                    </ul>
                    <span v-else class="text-muted">—</span>
                  </td>
                  <td :style="{ backgroundColor: getTaskBackground(task), cursor: 'pointer' }">{{ formatDate(task.created_at) }}</td>
                  <td :style="{ backgroundColor: getTaskBackground(task), cursor: 'pointer' }">{{ formatDate(task.completed_at) }}</td>
                </tr>
              </template>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '@/utils/axios'
import { useRouter } from 'vue-router'

const router = useRouter()
const rawBids = ref([])
const loading = ref(true)
const expandedIndex = ref(null)

onMounted(async () => {
  try {
    const response = await api.get('/tasks')
    rawBids.value = response.data
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

function goToTask(id) {
  router.push(`/tasks/${id}`)
}

function toggle(index) {
  expandedIndex.value = expandedIndex.value === index ? null : index
}
function getColorByProgress(progress) {
  if (progress === 0) return 'hsl(0, 0%, 100%)' // белый
  if (progress <= 20) return 'hsl(60, 100%, 90%)' // светло-жёлтый
  if (progress <= 50) return 'hsl(80, 100%, 85%)' // жёлто-зелёный
  if (progress <= 80) return 'hsl(100, 100%, 80%)' // светло-зелёный
  return 'hsl(120, 100%, 75%)' // зелёный
}

function getBidBackground(bid) {
  if (!bid || !bid.tasks || bid.tasks.length === 0) return 'hsl(0, 0%, 100%)'

  const progress = calculateBidProgress(bid)
  return getColorByProgress(progress)
}

function getTaskBackground(task) {
  if (!task) return 'hsl(0, 0%, 100%)'

  const status = task.status?.toLowerCase()?.trim()
  if (status !== 'в работе' && status !== 'выполнена') return 'hsl(0, 0%, 100%)'

  const progress = calculateTaskProgress(task)
  return getColorByProgress(progress)
}
function calculateTaskProgress(task) {
  const workshops = task.workshops || []
  if (workshops.length <= 1) {
    return task.total_quantity ? (task.done_quantity / task.total_quantity) * 100 : 0
  } else {
    const doneCount = workshops.filter(ws => ws.status === 'Выполнена').length
    return workshops.length ? (doneCount / workshops.length) * 100 : 0
  }
}

function calculateBidProgress(bid) {
  const tasks = bid.tasks || []
  if (tasks.length === 0) return 0
  const total = tasks.reduce((acc, task) => acc + calculateTaskProgress(task), 0)
  return total / tasks.length
}
</script>


<style scoped>
.text-muted {
  color: #888;
}
</style>
