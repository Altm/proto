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
import { ref, onMounted, computed } from 'vue'

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

const fetchSalesByVintage = async () => {
  try {
    loading.value = true
    
    // Создаем отчет по продажам по винтажам на основе имеющихся данных
    const salesReportMap = {}
    
    props.sales.forEach(sale => {
      const wine = getWineById(sale.wine_id)
      if (wine) {
        const key = `${wine.id}-${wine.vintage_year}`
        
        if (!salesReportMap[key]) {
          salesReportMap[key] = {
            wine_id: wine.id,
            wine_name: wine.name,
            vintage_year: wine.vintage_year,
            bottles_sold: 0,
            glasses_sold: 0,
            total_revenue: 0
          }
        }
        
        if (sale.product_type === 'bottle') {
          salesReportMap[key].bottles_sold += sale.quantity
        } else if (sale.product_type === 'glass') {
          salesReportMap[key].glasses_sold += sale.quantity
        }
        
        salesReportMap[key].total_revenue += sale.total_amount
      }
    })
    
    salesByVintage.value = Object.values(salesReportMap)
  } catch (error) {
    console.error('Error generating sales report:', error)
  } finally {
    loading.value = false
  }
}

const fetchInventoryByLocation = async () => {
  try {
    loading.value = true
    
    // Группируем инвентарь по локациям
    const locationMap = {}
    
    props.inventory.forEach(item => {
      const wine = getWineById(item.wine_id)
      if (wine && item.location) {
        if (!locationMap[item.location]) {
          locationMap[item.location] = []
        }
        
        locationMap[item.location].push({
          ...item,
          wine_name: wine.name,
          vintage_year: wine.vintage_year,
          producer: wine.producer,
          glasses_available: item.bottles_count * wine.glasses_per_bottle
        })
      }
    })
    
    inventoryByLocation.value = locationMap
  } catch (error) {
    console.error('Error generating inventory report:', error)
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
  height: calc(100vh - 120px); /* компенсируем высоту заголовка и отступов */
  overflow: auto;
}

.view-header {
  margin-bottom: 20px;
}

.el-table {
  margin-top: 10px;
}

/* Добавляем отступы для вкладок */
:deep(.el-tabs__content) {
  padding: 20px 0;
}
</style>