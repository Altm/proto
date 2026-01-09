<template>
  <div class="sales-view">
    <div class="view-header">
      <h2>Sales Management</h2>
      <el-button type="primary" @click="showCreateForm = true">Record Sale</el-button>
    </div>

    <el-table :data="sales" style="width: 100%" v-loading="loading">
      <el-table-column prop="id" label="ID" width="150" show-overflow-tooltip />
      <el-table-column label="Wine" width="200">
        <template #default="{ row }">
          {{ getWineName(row.wine_id) }} ({{ getWineVintage(row.wine_id) }})
        </template>
      </el-table-column>
      <el-table-column prop="product_type" label="Product Type" width="120" />
      <el-table-column prop="quantity" label="Quantity" width="100" />
      <el-table-column prop="unit_price" label="Unit Price" width="120">
        <template #default="{ row }">
          ${{ row.unit_price }}
        </template>
      </el-table-column>
      <el-table-column prop="total_amount" label="Total Amount" width="120">
        <template #default="{ row }">
          ${{ row.total_amount }}
        </template>
      </el-table-column>
      <el-table-column prop="location" label="Location" width="120" />
      <el-table-column prop="customer_name" label="Customer" width="150" />
      <el-table-column prop="sale_date" label="Date" width="150">
        <template #default="{ row }">
          {{ formatDate(row.sale_date) }}
        </template>
      </el-table-column>
    </el-table>

    <!-- Record Sale Dialog -->
    <el-dialog v-model="showCreateForm" title="Record New Sale" width="600px">
      <el-form :model="saleForm" :rules="saleRules" ref="saleFormRef" label-width="140px">
        <el-form-item label="Wine" prop="wine_id">
          <el-select v-model="saleForm.wine_id" placeholder="Select wine" filterable>
            <el-option
              v-for="wine in wines"
              :key="wine.id"
              :label="`${wine.name} (${wine.vintage_year})`"
              :value="wine.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="Product Type" prop="product_type">
          <el-radio-group v-model="saleForm.product_type">
            <el-radio label="bottle">Bottle</el-radio>
            <el-radio label="glass">Glass</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="Quantity" prop="quantity">
          <el-input-number v-model="saleForm.quantity" :min="1" />
        </el-form-item>
        <el-form-item label="Location" prop="location">
          <el-select v-model="saleForm.location" placeholder="Select location">
            <el-option label="Warehouse" value="warehouse" />
            <el-option label="Bar" value="bar" />
            <el-option label="Restaurant" value="restaurant" />
          </el-select>
        </el-form-item>
        <el-form-item label="Customer Name">
          <el-input v-model="saleForm.customer_name" placeholder="Optional" />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="showCreateForm = false">Cancel</el-button>
          <el-button type="primary" @click="submitSale">Confirm</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { apiService } from '../api/apiService.js'
import { ElMessage } from 'element-plus'

// Props
const props = defineProps({
  sales: {
    type: Array,
    default: () => []
  },
  wines: {
    type: Array,
    default: () => []
  }
})

// Emits
const emit = defineEmits(['refresh'])

// State
const loading = ref(false)
const showCreateForm = ref(false)

// Sale form
const saleForm = reactive({
  wine_id: '',
  product_type: 'bottle',
  quantity: 1,
  location: 'bar',
  customer_name: ''
})

// Form validation rules
const saleRules = {
  wine_id: [
    { required: true, message: 'Please select a wine', trigger: 'change' }
  ],
  product_type: [
    { required: true, message: 'Please select product type', trigger: 'change' }
  ],
  quantity: [
    { required: true, message: 'Please enter quantity', trigger: 'blur' }
  ],
  location: [
    { required: true, message: 'Please select location', trigger: 'change' }
  ]
}

// Methods
const recordSale = async () => {
  try {
    loading.value = true
    await apiService.createSale(saleForm)
    ElMessage.success('Sale recorded successfully')
    showCreateForm.value = false
    resetForm()
    emit('refresh')
  } catch (error) {
    console.error('Error recording sale:', error)
    ElMessage.error('Failed to record sale')
  } finally {
    loading.value = false
  }
}

const submitSale = async () => {
  await recordSale()
}

const resetForm = () => {
  Object.assign(saleForm, {
    wine_id: '',
    product_type: 'bottle',
    quantity: 1,
    location: 'bar',
    customer_name: ''
  })
}

const getWineById = (id) => {
  return props.wines.find(wine => wine.id === id)
}

const getWineName = (id) => {
  const wine = getWineById(id)
  return wine ? wine.name : 'Unknown'
}

const getWineVintage = (id) => {
  const wine = getWineById(id)
  return wine ? wine.vintage_year : ''
}

const formatDate = (dateString) => {
  const date = new Date(dateString)
  return date.toLocaleDateString() + ' ' + date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
}
</script>

<style scoped>
.sales-view {
  background: white;
  padding: 20px;
  border-radius: 4px;
  height: calc(100vh - 120px);
  overflow: auto;
}

.view-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}
</style>