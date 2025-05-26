<template>
    <div>
      <h2>Список задач</h2>
      <table>
        <thead>
          <tr>
            <th>№</th>
            <th>Заказчик</th>
            <th>Тип продукции</th>
            <th>Количество</th>
            <th>Срочность</th>
            <th>Статус</th>
            <th>Дата создания</th>
            <th>Детали</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="task in tasks" :key="task.id">
            <td>{{ task.task_number }}</td>
            <td>{{ task.bid.customer.name }}</td>
            <td>{{ task.product.type }}</td>
            <td>{{ task.quantity }}</td>
            <td>{{ task.urgency }}</td>
            <td>{{ task.status }}</td>
            <td>{{ formatDate(task.created_at) }}</td>
            <td>
              <router-link :to="`/tasks/${task.id}`">Подробнее</router-link>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted } from 'vue'
  import api from '@/utils/axios'
  
  const tasks = ref([])
  
  onMounted(async () => {
    try {
      const response = await api.get('/tasks/')  // ⚠️ Убедись, что этот маршрут существует
      tasks.value = response.data
    } catch (error) {
      console.error('Ошибка загрузки задач:', error)
    }
  })
  
  function formatDate(dateStr) {
    const date = new Date(dateStr)
    return date.toLocaleDateString()
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
  
  h2 {
    margin-bottom: 16px;
  }
  </style>
  