<template>
  <div>
    <h2>Создание заявки</h2>
    <form @submit.prevent="submitForm">

      <!-- Кнопки добавления/удаления изделий -->
      <div class="button-group">
        <button type="button" @click="addProduct">Добавить изделие</button>
        <button type="button" @click="removeLastProduct">Удалить последнее изделие</button>
      </div>

      <!-- Номер заявки, заказчик, менеджер -->
      <div class="form-row">
        <input v-model="form.task_number" type="number" placeholder="Номер заявки" />

        <select v-model="form.customer" @change="handleCustomerChange">
          <option value="">Выберите заказчика</option>
          <option v-for="customer in referenceData.customers" :key="customer.id" :value="customer.id">
            {{ customer.name }}
          </option>
          <option value="new">Добавить нового</option>
        </select>

        <input v-if="form.customer === 'new'" v-model="newCustomer" placeholder="Новый заказчик" />

        <select v-model="form.manager">
          <option value="">Выберите менеджера</option>
          <option v-for="manager in referenceData.managers" :key="manager.name" :value="manager.value">{{ manager.value }}</option>
        </select>
      </div>

      <!-- Список изделий -->
      <div v-for="(product, index) in products" :key="index" class="product-row">
        <ProductForm
          :product="product"
          :referenceData="referenceData"
          @update="updateProduct(index, $event)"
          @remove="removeProduct(index)"
          :key="index"
        />
      </div>
      <textarea v-model="form.comment" placeholder="Введите комментарий..." rows="3" style="width: 100%"></textarea>
      <!-- Загрузка файлов -->
      <div class="form-row">
        <label for="file-upload">Загрузить файлы:</label>
        <input id="file-upload" type="file" multiple accept="jpg, .jpeg, .png, .pdf, .nc, .xls, .xlsx, .doc, .docx, .dxf, .dwg" @change="handleFileUpload" />
      </div>


      <!-- Отправка -->
      <button type="submit">Отправить заявку</button>
    </form>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import ProductForm from './ProductForm.vue'
import api from '@/utils/axios'
import { useRouter } from 'vue-router'
const router = useRouter()
const form = reactive({
  task_number: '',
  customer: '',
  manager: '',
  comment: '',
})

const newCustomer = ref('')
const files = ref([])
const products = ref([])

const referenceData = reactive({
  customers: [],
  managers: [],
  products: [],
  materials: [],
  urgencies: [],
  workshops: [],
  employees: []
})

onMounted(async () => {
  try {
    const response = await api.get('/reference-data/')
    Object.assign(referenceData, response.data)
  } catch (error) {
    console.error('Ошибка загрузки справочников', error)
  }
})

function handleCustomerChange() {
  if (form.customer !== 'new') newCustomer.value = ''
}

function addProduct() {
  products.value.push({
    product: '',
    material: {},
    product_details: {},
    sheets: [],
    urgency: '',
    workshops: [],
    employees: [],
  })
}

function removeLastProduct() {
  products.value.pop()
}

function updateProduct(index, updatedProduct) {
  products.value[index] = updatedProduct
}

function removeProduct(index) {
  products.value.splice(index, 1)
}

function handleFileUpload(event) {
  files.value = Array.from(event.target.files)
}

async function submitForm() {
  const payload = {
    ...form,
    new_customer: form.customer === 'new' ? newCustomer.value : undefined,
    products: products.value,
    files: files.value.map(f => f.name),
  }

  const formData = new FormData()
  formData.append('bid_data', JSON.stringify(payload))
  files.value.forEach(file => formData.append('files', file))

  try {
    await api.post('/bids/create/', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })
    alert('Заявка успешно создана!')
    router.push('/tasks')
  } catch (error) {
    alert('Ошибка: ' + (error.response?.data?.message || error.message))
  }
}
</script>

<style scoped>
h2 {
  margin-bottom: 1rem;
  font-size: 1.5rem;
}

form {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.form-row {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
}

.form-row input,
.form-row select {
  flex: 1 1 200px;
  padding: 0.5rem;
  font-size: 1rem;
}

textarea {
  padding: 0.5rem;
  font-size: 1rem;
  resize: vertical;
}

.button-group {
  display: flex;
  gap: 1rem;
  margin-bottom: 1rem;
}

button {
  padding: 0.6rem 1.2rem;
  font-size: 1rem;
  background-color: #2d8cf0;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  transition: background-color 0.2s;
}

button:hover {
  background-color: #1a73e8;
}

label {
  font-weight: bold;
}

input[type="file"] {
  margin-top: 0.5rem;
}

.product-row {
  padding: 1rem;
  border: 1px solid #ddd;
  border-radius: 8px;
  margin-bottom: 1rem;
  background-color: #fafafa;
}

/* Немного воздуха внизу */
form > button[type="submit"] {
  align-self: flex-start;
  margin-top: 1rem;
}
</style>

