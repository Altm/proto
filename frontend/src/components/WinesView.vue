<template>
  <div class="wines-view">
    <div class="view-header">
      <h2>Wines Management</h2>
      <el-button type="primary" @click="showCreateForm = true">Add Wine</el-button>
    </div>

    <el-table :data="wines" style="width: 100%" v-loading="loading">
      <el-table-column prop="name" label="Name" width="200" />
      <el-table-column prop="producer" label="Producer" width="150" />
      <el-table-column prop="country" label="Country" width="120" />
      <el-table-column prop="region" label="Region" width="120" />
      <el-table-column prop="vintage_year" label="Vintage" width="100" />
      <el-table-column prop="wine_type" label="Type" width="100" />
      <el-table-column prop="bottle_size_ml" label="Size (ml)" width="100" />
      <el-table-column prop="glasses_per_bottle" label="Glasses/Bottle" width="120" />
      <el-table-column prop="price_bottle" label="Price (Bottle)" width="120">
        <template #default="{ row }">
          ${{ row.price_bottle }}
        </template>
      </el-table-column>
      <el-table-column prop="price_glass" label="Price (Glass)" width="120">
        <template #default="{ row }">
          ${{ row.price_glass }}
        </template>
      </el-table-column>
      <el-table-column label="Actions" width="200">
        <template #default="{ row }">
          <el-button size="small" @click="editWine(row)">Edit</el-button>
          <el-button size="small" type="danger" @click="deleteWine(row.id)">Delete</el-button>
        </template>
      </el-table-column>
    </el-table>

    <!-- Create/Edit Wine Dialog -->
    <el-dialog v-model="showCreateForm" :title="isEditing ? 'Edit Wine' : 'Create Wine'" width="600px">
      <el-form :model="wineForm" :rules="wineRules" ref="wineFormRef" label-width="140px">
        <el-form-item label="Name" prop="name">
          <el-input v-model="wineForm.name" />
        </el-form-item>
        <el-form-item label="Producer" prop="producer">
          <el-input v-model="wineForm.producer" />
        </el-form-item>
        <el-form-item label="Country" prop="country">
          <el-input v-model="wineForm.country" />
        </el-form-item>
        <el-form-item label="Region" prop="region">
          <el-input v-model="wineForm.region" />
        </el-form-item>
        <el-form-item label="Vintage Year" prop="vintage_year">
          <el-input-number v-model="wineForm.vintage_year" :min="1900" :max="2030" />
        </el-form-item>
        <el-form-item label="Wine Type" prop="wine_type">
          <el-select v-model="wineForm.wine_type" placeholder="Select type">
            <el-option label="Still" value="still" />
            <el-option label="Sparkling" value="sparkling" />
            <el-option label="Rosé" value="rose" />
            <el-option label="Dessert" value="dessert" />
          </el-select>
        </el-form-item>
        <el-form-item label="Bottle Size (ml)" prop="bottle_size_ml">
          <el-input-number v-model="wineForm.bottle_size_ml" :min="1" />
        </el-form-item>
        <el-form-item label="Glasses per Bottle" prop="glasses_per_bottle">
          <el-input-number v-model="wineForm.glasses_per_bottle" :min="1" />
        </el-form-item>
        <el-form-item label="Alcohol Content (%)" prop="alcohol_content">
          <el-input-number v-model="wineForm.alcohol_content" :min="0" :max="100" :step="0.1" />
        </el-form-item>
        <el-form-item label="Price (Bottle)" prop="price_bottle">
          <el-input-number v-model="wineForm.price_bottle" :min="0" :precision="2" :step="0.01" />
        </el-form-item>
        <el-form-item label="Price (Glass)" prop="price_glass">
          <el-input-number v-model="wineForm.price_glass" :min="0" :precision="2" :step="0.01" />
        </el-form-item>
        <el-form-item label="Description">
          <el-input v-model="wineForm.description" type="textarea" :rows="3" />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="showCreateForm = false">Cancel</el-button>
          <el-button type="primary" @click="submitWine">Confirm</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import axios from 'axios'
import { ElMessage, ElMessageBox } from 'element-plus'

// Props
const props = defineProps({
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
const isEditing = ref(false)
const currentWineId = ref(null)

// Wine form
const wineForm = reactive({
  name: '',
  producer: '',
  country: '',
  region: '',
  vintage_year: new Date().getFullYear(),
  wine_type: 'still',
  bottle_size_ml: 750,
  glasses_per_bottle: 5,
  alcohol_content: 12.5,
  price_bottle: 20.00,
  price_glass: 5.00,
  description: ''
})

// Form validation rules
const wineRules = {
  name: [
    { required: true, message: 'Please enter wine name', trigger: 'blur' }
  ],
  producer: [
    { required: true, message: 'Please enter producer', trigger: 'blur' }
  ],
  country: [
    { required: true, message: 'Please enter country', trigger: 'blur' }
  ],
  vintage_year: [
    { required: true, message: 'Please enter vintage year', trigger: 'blur' }
  ],
  wine_type: [
    { required: true, message: 'Please select wine type', trigger: 'change' }
  ],
  bottle_size_ml: [
    { required: true, message: 'Please enter bottle size', trigger: 'blur' }
  ],
  glasses_per_bottle: [
    { required: true, message: 'Please enter glasses per bottle', trigger: 'blur' }
  ],
  alcohol_content: [
    { required: true, message: 'Please enter alcohol content', trigger: 'blur' }
  ],
  price_bottle: [
    { required: true, message: 'Please enter bottle price', trigger: 'blur' }
  ],
  price_glass: [
    { required: true, message: 'Please enter glass price', trigger: 'blur' }
  ]
}

// Methods
const createWine = async () => {
  try {
    loading.value = true
    await axios.post('/api/wines', wineForm)
    ElMessage.success('Wine created successfully')
    showCreateForm.value = false
    resetForm()
    emit('refresh')
  } catch (error) {
    console.error('Error creating wine:', error)
    ElMessage.error('Failed to create wine')
  } finally {
    loading.value = false
  }
}

const updateWine = async () => {
  try {
    loading.value = true
    await axios.put(`/api/wines/${currentWineId.value}`, wineForm)
    ElMessage.success('Wine updated successfully')
    showCreateForm.value = false
    resetForm()
    emit('refresh')
  } catch (error) {
    console.error('Error updating wine:', error)
    ElMessage.error('Failed to update wine')
  } finally {
    loading.value = false
  }
}

const deleteWine = async (id) => {
  try {
    await ElMessageBox.confirm('Are you sure you want to delete this wine?', 'Warning', {
      confirmButtonText: 'OK',
      cancelButtonText: 'Cancel',
      type: 'warning'
    })
    
    await axios.delete(`/api/wines/${id}`)
    ElMessage.success('Wine deleted successfully')
    emit('refresh')
  } catch (error) {
    if (error !== 'cancel') {
      console.error('Error deleting wine:', error)
      ElMessage.error('Failed to delete wine')
    }
  }
}

const editWine = (wine) => {
  Object.assign(wineForm, wine)
  currentWineId.value = wine.id
  isEditing.value = true
  showCreateForm.value = true
}

const submitWine = async () => {
  if (isEditing.value) {
    await updateWine()
  } else {
    await createWine()
  }
}

const resetForm = () => {
  Object.assign(wineForm, {
    name: '',
    producer: '',
    country: '',
    region: '',
    vintage_year: new Date().getFullYear(),
    wine_type: 'still',
    bottle_size_ml: 750,
    glasses_per_bottle: 5,
    alcohol_content: 12.5,
    price_bottle: 20.00,
    price_glass: 5.00,
    description: ''
  })
  isEditing.value = false
  currentWineId.value = null
}
</script>

<style scoped>
.wines-view {
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