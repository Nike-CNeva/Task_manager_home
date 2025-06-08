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
          <strong>Заявка №{{ bid.task_number }}</strong> — {{ bid.customer.name }} (Менеджер: {{ bid.manager }})
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
                <tr :style="{ backgroundColor: getTaskBackground(task), cursor: 'pointer' }">
                  <td colspan="12" @click="goToTask(task.id)" style="cursor: pointer;">
                    <strong>Задача №{{ task.id }}</strong> — Всего: {{ task.total_quantity }}, Выполнено: {{ task.done_quantity }} ({{ task.progress_percent }}%)
                  </td>
                </tr>

                <tr
                  v-for="(tp, i) in task.task_products || []"
                  :key="`${task.id}-${i}`"
                  @click="goToTask(task.id)"
                  :style="{ backgroundColor: getTaskBackground(task), cursor: 'pointer' }"
                >
                  <td>{{ tp.product.type }} — {{ tp.product.cassette?.description || '—' }}</td>
                  <td>{{ tp.color }}</td>
                  <td>{{ tp.quantity }}</td>
                  <td>{{ tp.painting ? 'Да' : 'Нет' }}</td>
                  <td>
                    <template v-if="task.material">
                      {{ task.material.type }} {{ task.material.color }} {{ task.material.thickness }}
                    </template>
                    <span v-else class="text-muted">—</span>
                  </td>
                  <td>
                    <ul v-if="task.sheets?.length" class="mb-0 ps-3">
                      <li v-for="sheet in task.sheets" :key="sheet.id">
                        {{ sheet.count }} листов {{ sheet.width }}x{{ sheet.length }}
                      </li>
                    </ul>
                    <span v-else class="text-muted">—</span>
                  </td>
                  <td>{{ task.urgency }}</td>
                  <td>{{ task.progress_percent }}%</td>
                  <td>{{ task.status }}</td>
                  <td>
                    <ul v-if="task.workshops?.length" class="mb-0 ps-3">
                      <li v-for="ws in task.workshops" :key="ws.workshop_name">
                        {{ ws.workshop_name }}: {{ ws.status }}
                      </li>
                    </ul>
                    <span v-else class="text-muted">—</span>
                  </td>
                  <td>{{ formatDate(task.created_at) }}</td>
                  <td>{{ formatDate(task.completed_at) }}</td>
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
function getBidBackground(bid) {
  let allTasks = bid.tasks || []

  if (allTasks.length === 0) return '#ffffff' // нет задач

  const allStarted = allTasks.some(task => task.status !== 'Новая')
  if (!allStarted) return '#ffffff' // все задачи не начаты

  let totalProgress = 0
  let workshopProgress = 0
  let workshopCount = 0

  allTasks.forEach(task => {
    totalProgress += task.progress_percent || 0

    // считаем процент выполненных цехов
    const workshops = task.workshops || []
    const doneWorkshops = workshops.filter(ws => ws.status === 'Выполнена').length
    if (workshops.length > 0) {
      workshopProgress += (doneWorkshops / workshops.length) * 100
      workshopCount++
    }
  })

  const avgProgress = totalProgress / allTasks.length
  const avgWorkshop = workshopCount > 0 ? workshopProgress / workshopCount : 0

  // Итоговый процент: смешанный по задачам и цехам
  const percent = (avgProgress * 0.6 + avgWorkshop * 0.4)

  // Цвет от жёлтого (60°) к зелёному (120°) в HSL
  const hue = 60 + (percent / 100) * 60
  return `hsl(${hue}, 100%, 85%)`
}
function getTaskBackground(task) {
  if (!task || task.status === 'Новая') return '#ffffff'
  console.log(task)
  const progress = task.progress_percent || 0

  const workshops = task.workshops || []
  const doneCount = workshops.filter(ws => ws.status === 'Выполнена').length
  const totalCount = workshops.length
  const workshopPercent = totalCount > 0 ? (doneCount / totalCount) * 100 : 0

  // Смешанный процент: 60% прогресс задачи + 40% завершение по цехам
  const total = (progress * 0.6 + workshopPercent * 0.4)

  // Цвет от жёлтого (60°) до зелёного (120°)
  const hue = 60 + (total / 100) * 60
  return `hsl(${hue}, 100%, 85%)`
}
</script>


<style scoped>
.text-muted {
  color: #888;
}
</style>
