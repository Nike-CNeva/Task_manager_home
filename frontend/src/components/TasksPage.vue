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
      <div v-for="(bid, index) in rawBids" :key="bid.id" class="mb-3 border rounded">
        <!-- Заголовок заявки -->
        <div
          class="p-3 bg-light"
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
                <th>Тип продукции</th>
                <th>Количество</th>
                <th>Материал</th>
                <th>Листы</th>
                <th>Срочность</th>
                <th>Статус</th>
                <th>Статус цехов</th>
                <th>Дата создания</th>
                <th>Дата завершения</th>
              </tr>
            </thead>
            <tbody>
              <tr
                v-for="task in bid.tasks"
                :key="task.id"
                @click="goToTask(task.id)"
                style="cursor: pointer;"
              >
                <td>{{ task.product.type }}</td>
                <td>{{ task.quantity }}</td>
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
</script>

<style scoped>
.text-muted {
  color: #888;
}
</style>
