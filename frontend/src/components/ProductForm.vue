<template>
    <div class="product-container">
      <!-- Выбор изделия -->
      <select v-model="productData.product_id" @change="handleProductChange">
        <option value="">Выберите изделие</option>
        <option v-for="product in productOptions" :key="product.value" :value="product.value">
          {{ product.label }}
        </option>
      </select>
  
      <!-- Поля изделия -->
      <div v-if="productFields.length" class="product-fields">
        <div v-for="field in productFields" :key="field.name">
          <template v-if="field.type === 'select'">
            <select :name="field.name" v-model="productData.product_details[field.name]" @change="handleSpecialField(field.name)">
              <option value="">{{ field.label }}</option>
              <option v-for="opt in field.options" :key="opt.name" :value="opt.value">{{ opt.label }}</option>
            </select>
          </template>
  
          <template v-else-if="field.type === 'checkbox'">
            <label>
              <input type="checkbox" :name="field.name" v-model="productData.product_details[field.name]" />
              {{ field.label }}
            </label>
          </template>
  
          <template v-else>
            <input :type="field.type" :name="field.name" :placeholder="field.label" v-model="productData.product_details[field.name]" />
          </template>
        </div>
  
        <!-- Нестандартный профиль -->
        <input v-if="productData.product_details.profile_type_id === '11'" type="text" placeholder="Введите тип профиля"
               v-model="productData.product_details.custom_profile_type" />
        <!-- Нестандартная кассета -->
        <input v-if="productData.product_details.cassette_type_id === 'OTHER'" type="text" placeholder="Описание кассеты"
               v-model="productData.product_details.custom_cassette_type" />
      </div>
  
      <!-- Материалы -->
      <div class="material-fields" v-if="materialForms.length">
        <select v-model="productData.material" @change="loadMaterialTypes">
          <option value="">Выберите форму материала</option>
          <option v-for="form in materialForms" :key="form.name" :value="form.name">{{ form.value }}</option>
        </select>
      </div>
  
      <div v-if="materialTypes.length">
        <select v-model="productData.material_type" @change="loadThickness">
          <option value="">Выберите тип материала</option>
          <option v-for="type in materialTypes" :key="type.name" :value="type.name">{{ type.value }}</option>
        </select>
      </div>
  
      <div v-if="thicknesses.length">
        <select v-model="productData.thickness">
          <option value="">Выберите толщину</option>
          <option v-for="thick in thicknesses" :key="thick.name" :value="thick.name">{{ thick.value }}</option>
        </select>
      </div>
  
      <!-- Листы -->
      <div v-if="showSheets">
        <div v-for="(sheet, i) in sheets" :key="i" class="sheet-fields">
          <input type="number" placeholder="Ширина листа" v-model.number="sheet.width" />
          <input type="number" placeholder="Длина листа" v-model.number="sheet.length" />
          <input type="number" placeholder="Количество листов" v-model.number="sheet.quantity" />
        </div>
        <button type="button" @click="addSheet">Добавить лист</button>
        <button type="button" @click="removeSheet">Удалить лист</button>
      </div>
  
      <!-- Назначения -->
      <div class="assignment-container">
        <select v-model="urgency">
          <option value="">Выберите срочность</option>
          <option v-for="u in urgencies" :key="u" :value="u">{{ u }}</option>
        </select>
  
        <label>Назначить цех:</label>
        <select v-model="workshops" multiple>
          <option v-for="ws in allWorkshops" :key="ws.id" :value="ws.id">{{ ws.name }}</option>
        </select>
  
        <label>Назначить сотрудников:</label>
        <select v-model="employees" multiple>
          <option v-for="emp in allEmployees" :key="emp.id" :value="emp.id">{{ emp.name }} {{ emp.firstname }}</option>
        </select>
  
        <textarea v-model="comment" placeholder="Введите комментарий..." rows="3" style="width: 100%"></textarea>
      </div>
    </div>
  </template>
  
  <script setup lang="js">
import { ref, reactive, watch, onMounted } from 'vue';
import api from '@/utils/axios'; // твой axios-инстанс

const emits = defineEmits(['update', 'remove']);

const productData = reactive({
  product_id: '',
  material: '',
  material_type: '',
  thickness: '',
  product_details: {},
  sheets: [],
});

const productOptions = ref([]);
const productFields = ref([]);
const materialForms = ref([]);
const materialTypes = ref([]);
const thicknesses = ref([]);
const showSheets = ref(false);

const sheets = ref([]);

const urgency = ref('');
const comment = ref('');
const workshops = ref([]);
const employees = ref([]);

const urgencies = ref([]);
const allWorkshops = ref([]);
const allEmployees = ref([]);

onMounted(async () => {
  try {
    const [productsRes, urgenciesRes, workshopsRes, employeesRes] = await Promise.all([
      api.get('/products/'),
      api.get('/urgency/'),
      api.get('/workshops/'),
      api.get('/employee/'),
    ]);
    productOptions.value = productsRes.data;
    urgencies.value = urgenciesRes.data;
    allWorkshops.value = workshopsRes.data;
    allEmployees.value = employeesRes.data;
  } catch (error) {
    console.error('Ошибка загрузки данных:', error);
  }
});

watch(
  [productData, urgency, comment, workshops, employees, sheets],
  () => {
    emits('update', {
      ...productData,
      urgency: urgency.value,
      comment: comment.value,
      workshops: [...workshops.value],
      employees: [...employees.value],
      sheets: sheets.value,
    });
  },
  { deep: true }
);

async function handleProductChange() {
  try {
    const pid = productData.product_id;
    const [fieldsRes, formsRes] = await Promise.all([
      api.get(`/products/${pid}/fields`),
      api.get(`/material/forms/${pid}`),
    ]);
    productFields.value = fieldsRes.data;
    materialForms.value = formsRes.data;

    if (['CASSETTE', 'SHEET'].includes(pid)) {
      showSheets.value = true;
    } else {
      showSheets.value = false;
      sheets.value = [];
    }
  } catch (error) {
    console.error('Ошибка при изменении продукта:', error);
  }
}

function handleSpecialField(name) {
  if (name === 'profile_type_id' || name === 'cassette_type_id') {
    // Просто триггерим пересборку данных
  }
}

async function loadMaterialTypes() {
  try {
    const pid = productData.product_id;
    const form = productData.material;
    const res = await api.get(`/material/types/${pid}/${form}`);
    materialTypes.value = res.data;
    if (materialTypes.value.length) {
      productData.material_type = materialTypes.value[0].name;
      await loadThickness();
    }
  } catch (error) {
    console.error('Ошибка загрузки типов материала:', error);
  }
}

async function loadThickness() {
  try {
    const res = await api.get(`/material/thickness/${productData.material_type}`);
    thicknesses.value = res.data;
  } catch (error) {
    console.error('Ошибка загрузки толщин:', error);
  }
}

function addSheet() {
  sheets.value.push({ width: 0, length: 0, quantity: 1 });
}

function removeSheet() {
  sheets.value.pop();
}
</script>

  
  <style scoped>
  .product-container {
    border: 1px solid #ccc;
    padding: 10px;
    margin-bottom: 15px;
    border-radius: 10px;
  }
  </style>
  