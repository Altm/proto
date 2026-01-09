<template>
  <div class="reports-view">
    <div class="view-header">
      <h2>Reports</h2>
    </div>

    <el-tabs v-model="activeTab">
      <el-tab-pane label="Sales by Vintage" name="salesByVintage">
        <h3>Sales by Vintage Year</h3>
        <el-table :data="salesByVintage" style="width: 100%" v-loading="loading">
          <el-table-column prop="wine_name" label="Wine Name" width="200" />
          <el-table-column prop="vintage_year" label="Vintage Year" width="120" />
          <el-table-column prop="bottles_sold" label="Bottles Sold" width="120" />
          <el-table-column prop="glasses_sold" label="Glasses Sold" width="120" />
          <el-table-column prop="total_revenue" label="Total Revenue" width="120">
            <template #default="{ row }">
              ${{ row.total_revenue.toFixed(2) }}
            </template>
          </el-table-column>
        </el-table>
      </el-tab-pane>

      <el-tab-pane label="Inventory by Location" name="inventoryByLocation">
        <h3>Inventory by Location</h3>
        <el-collapse accordion>
          <el-collapse-item 
            v-for="(locationItems, location) in inventoryByLocation" 
            :key="location" 
            :title="location"
          >
            <el-table :data="locationItems" style="width: 100%">
              <el-table-column prop="wine_name" label="Wine Name" width="200" />
              <el-table-column prop="vintage_year" label="Vintage Year" width="120" />
              <el-table-column prop="producer" label="Producer" width="150" />
              <el-table-column prop="bottles_count" label="Bottles" width="100" />
              <el-table-column prop="glasses_available" label="Glasses Avail" width="120" />
            </el-table>
          </el-collapse-item>
        </el-collapse>
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

// Props
const props = defineProps({
  wines: {
    type: Array,
    default: () => []
  },
  sales: {
    type: Array,
    default: () => []
  },
  inventory: {
    type: Array,
    default: () => []
  }
})

// State
const loading = ref(false)
const activeTab = ref('salesByVintage')
const salesByVintage = ref([])
const inventoryByLocation = ref({})

// Methods
const fetchSalesByVintage = async () => {
  try {
    loading.value = true
    const response = await axios.get('http://localhost:8000/reports/sales-by-vintage')
    salesByVintage.value = response.data
  } catch (error) {
    console.error('Error fetching sales by vintage:', error)
  } finally {
    loading.value = false
  }
}

const fetchInventoryByLocation = async () => {
  try {
    loading.value = true
    const response = await axios.get('http://localhost:8000/reports/inventory-by-location')
    inventoryByLocation.value = response.data
  } catch (error) {
    console.error('Error fetching inventory by location:', error)
  } finally {
    loading.value = false
  }
}

const refreshData = async () => {
  await Promise.all([
    fetchSalesByVintage(),
    fetchInventoryByLocation()
  ])
}

onMounted(() => {
  refreshData()
})
</script>

<style scoped>
.reports-view {
  background: white;
  padding: 20px;
  border-radius: 4px;
}

.view-header {
  margin-bottom: 20px;
}

.el-table {
  margin-top: 10px;
}
</style>