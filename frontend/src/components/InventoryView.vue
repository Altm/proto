<template>
  <div class="inventory-view">
    <div class="view-header">
      <h2>Inventory Management</h2>
    </div>

    <el-table :data="inventory" style="width: 100%" v-loading="loading">
      <el-table-column label="Wine Details" width="300">
        <template #default="{ row }">
          <div>
            <strong>{{ getWineName(row.wine_id) }}</strong><br>
            <small>{{ getWineVintage(row.wine_id) }} | {{ getWineProducer(row.wine_id) }}</small>
          </div>
        </template>
      </el-table-column>
      <el-table-column prop="location" label="Location" width="120" />
      <el-table-column prop="bottles_count" label="Bottles" width="100" />
      <el-table-column label="Glasses Available" width="130">
        <template #default="{ row }">
          {{ row.bottles_count * getWineGlassesPerBottle(row.wine_id) }}
        </template>
      </el-table-column>
      <el-table-column label="Actions" width="200">
        <template #default="{ row }">
          <el-button size="small" @click="adjustInventory(row)">Adjust</el-button>
        </template>
      </el-table-column>
    </el-table>

    <!-- Adjust Inventory Dialog -->
    <el-dialog v-model="showAdjustForm" title="Adjust Inventory" width="500px">
      <el-form :model="adjustForm" label-width="120px">
        <el-form-item label="Current Bottles">
          <el-input :value="selectedInventory?.bottles_count" readonly />
        </el-form-item>
        <el-form-item label="New Bottle Count" prop="bottles_count">
          <el-input-number v-model="adjustForm.bottles_count" :min="0" />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="showAdjustForm = false">Cancel</el-button>
          <el-button type="primary" @click="confirmAdjust">Confirm</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'
import { ElMessage } from 'element-plus'

// Props
const props = defineProps({
  inventory: {
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
const showAdjustForm = ref(false)
const selectedInventory = ref(null)

// Adjust form
const adjustForm = ref({
  bottles_count: 0
})

// Methods
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

const getWineProducer = (id) => {
  const wine = getWineById(id)
  return wine ? wine.producer : ''
}

const getWineGlassesPerBottle = (id) => {
  const wine = getWineById(id)
  return wine ? wine.glasses_per_bottle : 0
}

const adjustInventory = async (inventoryItem) => {
  selectedInventory.value = inventoryItem
  adjustForm.value.bottles_count = inventoryItem.bottles_count
  showAdjustForm.value = true
}

const confirmAdjust = async () => {
  try {
    loading.value = true
    await axios.put(`/api/inventory/${selectedInventory.value.wine_id}`, {
      bottles_count: adjustForm.value.bottles_count
    })
    ElMessage.success('Inventory adjusted successfully')
    showAdjustForm.value = false
    emit('refresh')
  } catch (error) {
    console.error('Error adjusting inventory:', error)
    ElMessage.error('Failed to adjust inventory')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.inventory-view {
  background: white;
  padding: 20px;
  border-radius: 4px;
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