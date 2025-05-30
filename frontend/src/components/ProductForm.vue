<script setup>
import { ref, reactive, watch, computed } from 'vue';

const props = defineProps({ referenceData: Object, product: Object });
const emit = defineEmits(['update', 'remove']);

const form = reactive({
  product_name: props.product.value || '',
  product_details: props.product.fields || [],
  material: props.product.materials || {},
  sheets: props.product.sheets || [],
  urgency: props.product.urgency || '',
  workshops: props.product.workshops || [],
  employees: props.product.employees || [],
  color: props.product.color || '',
  quantity: props.product.quantity || '',
  painting: props.product.painting ,
});

const productFields = ref([])
const materialFields = ref([]); 
const showSheets = ref(false);

watch(() => form.product_name, (newPname) => {
  const selectedProduct = props.referenceData.products.find(p => p.value === newPname);

  // Показывать ли листы (showSheets)
  showSheets.value = !!selectedProduct && ['Кассеты', 'Листы'].includes(selectedProduct.value);

  const productFieldSet = selectedProduct?.fields || [];
  productFields.value = productFieldSet;

  // Функция создания пустой позиции с инициализацией по типам полей
  const createEmptyPosition = () => {
    const pos = {};
    productFieldSet.forEach(field => {
      switch (field.type) {
        case 'select':
        case 'number':
          pos[field.name] = '';
          break;
        case 'checkbox':
          pos[field.name] = false;
          break;
        default:
          pos[field.name] = '';
      }
    });
    return pos;
  };

  // Если product_details не массив или пустой — создаём массив с одной позицией
  if (!Array.isArray(form.product_details) || form.product_details.length === 0) {
    form.product_details = [createEmptyPosition()];
  }

  // Инициализация material_details с пустыми значениями по всем полям материалов
  materialFields.value = props.referenceData.materials || [];
  const initialMaterialDetails = {};
  materialFields.value.forEach(field => {
    switch (field.type) {
      case 'select':
        initialMaterialDetails[field.name] = '';
        break;
      case 'checkbox':
        initialMaterialDetails[field.name] = false;
        break;
      default:
        initialMaterialDetails[field.name] = '';
    }
  });
  form.material_details = initialMaterialDetails;

  // Эмитим обновлённую форму
  emit('update', { ...form });

}, { immediate: true });

function addPosition() {
  const pos = {};
  productFields.value.forEach(field => {
    if (field.type === 'checkbox') pos[field.name] = false;
    else pos[field.name] = '';
  });
  form.product_details.push(pos);
  emitUpdate();
}

function removePosition(index) {
  form.product_details.splice(index, 1);
  emitUpdate();
}

// Следим за всем объектом формы и эмитим обновления
watch(form, () => {
  // Создаем новый объект, объединяя product_details и material_details
  const productData = {
    product_name: form.product_name,
    product_details: form.product_details,
    // распаковываем material_details
    material: form.material_details,
    sheets: form.sheets,
    urgency: form.urgency,
    workshops: form.workshops,
    employees: form.employees,
  };

  // Отправляем обновленный объект, где material_details "вышел из тени"
  emit('update', productData);
}, { deep: true });
</script>

<template>
  <div class="product-container">
    <select v-model="form.product_name">
      <option value="">Выберите изделие</option>
      <option v-for="product in props.referenceData.products" :key="product.name" :value="product.value">
        {{ product.value }}
      </option>
    </select>

    <div v-for="(position, i) in form.product_details" :key="i" class="position-block">
  <div v-for="field in productFields" :key="field.name" class="field-wrapper">
    <template v-if="field.type === 'select'">
      <select v-model="form.product_details[i][field.name]">
        <option value="">{{ field.label }}</option>
        <option v-for="opt in field.options" :key="opt.name" :value="opt.name">
          {{ opt.value }}
        </option>
      </select>
    </template>
    <template v-else-if="field.type === 'checkbox'">
      <label>
        <input type="checkbox" v-model="form.product_details[i][field.name]" />
        {{ field.label }}
      </label>
    </template>
    <template v-else>
      <input :type="field.type" :placeholder="field.label" v-model="form.product_details[i][field.name]" />
    </template>
  </div>

  <button type="button" @click="removePosition(i)" v-if="form.product_details.length > 1">Удалить позицию</button>
</div>

<button type="button" @click="addPosition">Добавить позицию</button>
    <div v-if="materialFields.length" class="materials-fields">
      <div v-for="field in materialFields" :key="field.name" class="field-wrapper">
        <template v-if="field.type === 'select'">
          <select v-model="form.material_details[field.name]" :name="field.name">
            <option value="">{{ field.label }}</option>
            <option v-for="opt in field.options" :key="opt.name" :value="opt.value">
              {{ opt.value }}
            </option>
          </select>
        </template>

        <template v-else-if="field.type === 'checkbox'">
          <label>
            <input type="checkbox" :name="field.name" v-model="form.material_details[field.name]" />
            {{ field.label }}
          </label>
        </template>

        <template v-else>
          <input :type="field.type" :name="field.name" :placeholder="field.label" v-model="form.material_details[field.name]" />
        </template>
      </div>
    </div>

    <div v-if="showSheets">
      <div v-for="(sheet, i) in form.sheets" :key="i" class="sheet-fields">
        <input type="number" placeholder="Ширина листа" v-model.number="sheet.width" />
        <input type="number" placeholder="Длина листа" v-model.number="sheet.length" />
        <input type="number" placeholder="Количество листов" v-model.number="sheet.quantity" />
      </div>
      <button type="button" @click="form.sheets.push({ width:'', length: '', quantity: '' })">Добавить лист</button>
      <button type="button" @click="form.sheets.pop()">Удалить лист</button>
    </div>

    <div class="assignment-container">
      <select v-model="form.urgency">
        <option value="">Выберите срочность</option>
        <option v-for="u in props.referenceData.urgency" :key="u.name" :value="u.value">{{ u.value }}</option>
      </select>

      <label>Назначить цех:</label>
      <select v-model="form.workshops" multiple>
        <option v-for="ws in props.referenceData.workshops" :key="ws.name" :value="ws.value">{{ ws.value }}</option>
      </select>

      <label>Назначить сотрудников:</label>
      <select v-model="form.employees" multiple>
        <option v-for="emp in props.referenceData.employees" :key="emp.id" :value="emp.id">{{ emp.name }} {{ emp.firstname }}</option>
      </select>

      
    </div>
  </div>
</template>
<style scoped>
.product-fields {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem; /* расстояние между полями */
  margin-top: 1rem;
}

.field-wrapper {
  flex: 1 1 auto;
  min-width: 200px; /* можно менять под нужную ширину */
}
.materials-fields {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  margin-top: 1rem;
}

.materials-fields .field-wrapper {
  flex: 1 1 auto;
  min-width: 200px;
}
.product-container select,
.product-container input,
.product-container button {
  display: block;
  width: 100%;
  padding: 0.5rem 0.75rem;
  margin-top: 0.5rem;
  border: 1px solid #ccc;
  border-radius: 0.5rem;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
  font-size: 1rem;
  transition: border-color 0.2s, box-shadow 0.2s;
}

.product-container select:focus,
.product-container input:focus {
  border-color: #007bff;
  box-shadow: 0 0 0 2px rgba(0, 123, 255, 0.2);
  outline: none;
}

button {
  width: auto;
  margin-top: 0.5rem;
  margin-right: 0.5rem;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 0.5rem;
  padding: 0.5rem 1rem;
  cursor: pointer;
  font-weight: 500;
}

button:hover {
  background-color: #0056b3;
}

.product-fields,
.materials-fields {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  margin-top: 1rem;
}

.field-wrapper {
  flex: 1 1 auto;
  min-width: 200px;
}

.sheet-fields {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 0.5rem;
}

.assignment-container {
  margin-top: 1rem;
  padding: 1rem;
  border: 1px dashed #aaa;
  border-radius: 0.5rem;
  background-color: #f8f9fa;
}
</style>