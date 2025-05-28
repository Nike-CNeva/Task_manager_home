<template>
    <div>
      <h2 class="my-4">Детали задачи №{{ task.task_number }}</h2>
  
      <div v-if="task">
        <table class="table table-bordered">
          <tbody>
            <tr>
              <th>Заказчик</th>
              <td>{{ task.customer.name }}</td>
            </tr>
            <tr>
              <th>Менеджер</th>
              <td>{{ task.manager }}</td>
            </tr>
            <tr>
              <th>Тип продукции</th>
              <td>{{ task.product.type }}</td>
            </tr>
            <tr>
              <th>Количество</th>
              <td>{{ task.quantity }}</td>
            </tr>
            <tr>
              <th>Материал</th>
              <td>
                <template v-if="task.material">
                  {{ task.material.type }} {{ task.material.color }} {{ task.material.thickness }}
                </template>
                <span v-else class="text-muted">—</span>
              </td>
            </tr>
            <tr>
              <th>Листы</th>
              <td>
                <ul v-if="task.sheets && task.sheets.length" class="mb-0 ps-3">
                  <li v-for="sheet in task.sheets" :key="sheet.id">
                    {{ sheet.count }} листов {{ sheet.width }}x{{ sheet.length }}
                  </li>
                </ul>
                <span v-else class="text-muted">—</span>
              </td>
            </tr>
            <tr>
              <th>Срочность</th>
              <td>{{ task.urgency }}</td>
            </tr>
            <tr>
              <th>Статус</th>
              <td>{{ task.status }}</td>
            </tr>
            <tr>
              <th>Статус цехов</th>
              <td>
                <ul v-if="task.workshops && task.workshops.length" class="mb-0 ps-3">
                  <li v-for="ws in task.workshops" :key="ws.workshop_name">
                    {{ ws.workshop_name }}: {{ ws.status }}
                  </li>
                </ul>
                <span v-else class="text-muted">—</span>
              </td>
            </tr>
            <tr>
              <th>Дата создания</th>
              <td>{{ formatDate(task.created_at) }}</td>
            </tr>
            <tr>
              <th>Дата завершения</th>
              <td>{{ formatDate(task.completed_at) }}</td>
            </tr>
          </tbody>
        </table>
  
        <button class="btn btn-secondary" @click="goBack">Назад к списку</button>
      </div>
  
      <div v-else>
        <p>Загрузка данных задачи...</p>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted } from 'vue'
  import api from '@/utils/axios'
  import { useRoute, useRouter } from 'vue-router'
  
  const route = useRoute()
  const router = useRouter()
  const task = ref(null)
  
  async function loadTask(id) {
    try {
      const response = await api.get(`/task/${id}`)
      task.value = response.data
    } catch (err) {
      console.error('Ошибка загрузки задачи:', err)
      alert('Не удалось загрузить задачу')
      router.push('/tasks')
    }
  }
  
  function formatDate(dateStr) {
    if (!dateStr) return '—'
    const date = new Date(dateStr)
    return date.toLocaleDateString()
  }
  
  function goBack() {
    router.push('/tasks')
  }
  
  onMounted(() => {
    const id = route.params.id
    loadTask(id)
  })
  </script>
  
  <style scoped>
  table {
    width: 100%;
    border-collapse: collapse;
    margin-bottom: 20px;
  }
  th {
    width: 200px;
    background-color: #f8f9fa;
    text-align: left;
    padding: 8px;
    border: 1px solid #ddd;
  }
  td {
    border: 1px solid #ddd;
    padding: 8px;
  }
  .text-muted {
    color: #888;
  }
  button {
    margin-top: 10px;
  }
  </style>
  