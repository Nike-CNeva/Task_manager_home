<template>
    <div>
      <h2>Создание заявки</h2>
      <form @submit.prevent="submitForm">
        <!-- Первая строка: кнопки -->
        <div class="button-group">
          <button type="button" @click="addProduct">Добавить изделие</button>
          <button type="button" @click="removeLastProduct">Удалить последнее изделие</button>
        </div>
  
        <!-- Вторая строка: Номер заявки, заказчик, менеджер -->
        <div class="form-row">
          <input v-model="form.task_number" type="number" placeholder="Номер заявки" />
  
          <select v-model="form.customer_id" @change="handleCustomerChange">
            <option value="">Выберите заказчика</option>
            <option v-for="customer in customers" :key="customer.id" :value="customer.id">{{ customer.name }}</option>
            <option value="new">Добавить нового</option>
          </select>
  
          <input v-if="form.customer_id === 'new'" v-model="newCustomer" placeholder="Новый заказчик" />
  
          <select v-model="form.manager">
            <option value="">Выберите менеджера</option>
            <option v-for="manager in managers" :key="manager" :value="manager">{{ manager }}</option>
          </select>
        </div>
  
        <!-- Изделия -->
        <div v-for="(product, index) in products" :key="index" class="product-row">
          <!-- Здесь будут дочерние компоненты -->
          <ProductForm
            :product="product"
            :index="index"
            @update="updateProduct(index, $event)"
            @remove="removeProduct(index)"
          />
        </div>
  
        <!-- Загрузка файлов -->
        <div class="form-row">
          <label for="file-upload">Загрузить файлы:</label>
          <input id="file-upload" type="file" multiple @change="handleFileUpload" />
        </div>
  
        <!-- Статус -->
        <div class="form-row">
          <select v-model="form.status">
            <option value="">Выберите статус</option>
            <option v-for="status in statuses" :key="status" :value="status">{{ status }}</option>
          </select>
        </div>
  
        <!-- Кнопка отправки -->
        <button type="submit">Отправить заявку</button>
      </form>
    </div>
  </template>
  
  <script setup>
  import { ref, reactive, onMounted } from 'vue';
  import ProductForm from './ProductForm.vue'; // Компонент для одного изделия
  
  const form = reactive({
    task_number: '',
    customer_id: '',
    manager: '',
    status: '',
  });
  
  const newCustomer = ref('');
  const files = ref([]);
  const customers = ref([]);
  const managers = ref([]);
  const statuses = ref([]);
  const products = ref([]);
  
  onMounted(async () => {
  // Загружаем данные с API
  const customersResponse = await fetch('/customers/');
  customers.value = await customersResponse.json();
  console.log("Customers:", customers.value); // Выводим данные клиентов в консоль
  
  const managersResponse = await fetch('/managers/');
  managers.value = await managersResponse.json();
  console.log("Managers:", managers.value); // Выводим данные менеджеров в консоль

  const statusesResponse = await fetch('/statuses/');
  statuses.value = await statusesResponse.json();
  console.log("Statuses:", statuses.value); // Выводим данные статусов в консоль
});
  
  function handleCustomerChange() {
    if (form.customer_id !== 'new') newCustomer.value = '';
  }
  
  function addProduct() {
    products.value.push({});
  }
  
  function removeLastProduct() {
    products.value.pop();
  }
  
  function updateProduct(index, data) {
    products.value[index] = data;
  }
  
  function removeProduct(index) {
    products.value.splice(index, 1);
  }
  
  function handleFileUpload(event) {
    files.value = Array.from(event.target.files);
  }
  
  async function submitForm() {
    const payload = {
      ...form,
      new_customer: form.customer_id === 'new' ? newCustomer.value : undefined,
      products: products.value,
      files: files.value.map(f => f.name),
    };
  
    const formData = new FormData();
    formData.append('bid_data', JSON.stringify(payload));
    files.value.forEach(file => formData.append('files', file));
  
    const response = await fetch('/bids/create/', {
      method: 'POST',
      body: formData,
    });
  
    const result = await response.json();
    if (response.ok) {
      alert('Заявка успешно создана!');
    } else {
      alert('Ошибка: ' + result.message);
    }
  }
  </script>
  
  <style scoped>
  /* Можно скопировать стили из HTML или написать на Tailwind / Bootstrap */
  </style>
  