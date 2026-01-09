<template>
  <div class="admin-container">
    <el-container>
      <el-aside width="200px" class="sidebar">
        <div class="logo">
          <h3>Wine Admin</h3>
        </div>
        <el-menu
          :default-active="activeMenu"
          class="sidebar-menu"
          @select="handleMenuSelect"
          :collapse="isCollapse"
        >
          <el-menu-item index="dashboard">
            <el-icon><House /></el-icon>
            <span>Dashboard</span>
          </el-menu-item>
          <el-menu-item index="wines">
            <el-icon><List /></el-icon>
            <span>Wines</span>
          </el-menu-item>
          <el-menu-item index="inventory">
            <el-icon><Box /></el-icon>
            <span>Inventory</span>
          </el-menu-item>
          <el-menu-item index="sales">
            <el-icon><Money /></el-icon>
            <span>Sales</span>
          </el-menu-item>
          <el-menu-item index="reports">
            <el-icon><Document /></el-icon>
            <span>Reports</span>
          </el-menu-item>
        </el-menu>
      </el-aside>

      <el-container class="main-container" :class="{ 'el-aside--collapse': isCollapse }">
        <el-header class="header">
          <el-button @click="isCollapse = !isCollapse" size="large">
            <el-icon><Fold v-if="!isCollapse" /><Expand v-else /></el-icon>
          </el-button>
          <div class="header-right">
            <el-button type="primary" @click="refreshData">Refresh</el-button>
          </div>
        </el-header>

        <el-main class="main-content">
          <!-- Dashboard View -->
          <div v-if="activeMenu === 'dashboard'">
            <h2>Dashboard</h2>
            <el-row :gutter="20">
              <el-col :span="6">
                <el-card class="dashboard-card">
                  <div class="card-content">
                    <h3>Total Wines</h3>
                    <p class="count">{{ wines.length }}</p>
                  </div>
                </el-card>
              </el-col>
              <el-col :span="6">
                <el-card class="dashboard-card">
                  <div class="card-content">
                    <h3>Total Bottles</h3>
                    <p class="count">{{ totalBottles }}</p>
                  </div>
                </el-card>
              </el-col>
              <el-col :span="6">
                <el-card class="dashboard-card">
                  <div class="card-content">
                    <h3>Total Sales</h3>
                    <p class="count">{{ sales.length }}</p>
                  </div>
                </el-card>
              </el-col>
              <el-col :span="6">
                <el-card class="dashboard-card">
                  <div class="card-content">
                    <h3>Total Revenue</h3>
                    <p class="count">${{ totalRevenue.toFixed(2) }}</p>
                  </div>
                </el-card>
              </el-col>
            </el-row>
          </div>

          <!-- Wines View -->
          <WinesView v-if="activeMenu === 'wines'" :wines="wines" @refresh="fetchData" />

          <!-- Inventory View -->
          <InventoryView v-if="activeMenu === 'inventory'" :inventory="inventory" :wines="wines" @refresh="fetchData" />

          <!-- Sales View -->
          <SalesView v-if="activeMenu === 'sales'" :sales="sales" :wines="wines" @refresh="fetchData" />

          <!-- Reports View -->
          <ReportsView v-if="activeMenu === 'reports'" :wines="wines" :sales="sales" :inventory="inventory" />
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { House, List, Box, Money, Document, Fold, Expand } from '@element-plus/icons-vue'
import WinesView from './components/WinesView.vue'
import InventoryView from './components/InventoryView.vue'
import SalesView from './components/SalesView.vue'
import ReportsView from './components/ReportsView.vue'

// State
const activeMenu = ref('dashboard')
const isCollapse = ref(false)
const wines = ref([])
const inventory = ref([])
const sales = ref([])

// Тестовые данные
const mockWines = [
  { id: 1, name: 'Château Margaux', producer: 'Château Margaux', country: 'France', region: 'Bordeaux', vintage_year: 2018, wine_type: 'still', bottle_size_ml: 750, glasses_per_bottle: 5, alcohol_content: 13.5, price_bottle: 299.99, price_glass: 15.00, description: 'Premium Bordeaux red wine' },
  { id: 2, name: 'Dom Pérignon', producer: 'Moët & Chandon', country: 'France', region: 'Champagne', vintage_year: 2016, wine_type: 'sparkling', bottle_size_ml: 750, glasses_per_bottle: 6, alcohol_content: 12.0, price_bottle: 199.99, price_glass: 12.00, description: 'Luxury champagne' },
  { id: 3, name: 'Sassicaia', producer: 'Tenuta San Guido', country: 'Italy', region: 'Tuscany', vintage_year: 2019, wine_type: 'still', bottle_size_ml: 750, glasses_per_bottle: 5, alcohol_content: 14.0, price_bottle: 149.99, price_glass: 10.00, description: 'Super Tuscan wine' },
  { id: 4, name: 'Opus One', producer: 'Opus One Winery', country: 'USA', region: 'Napa Valley', vintage_year: 2017, wine_type: 'still', bottle_size_ml: 750, glasses_per_bottle: 5, alcohol_content: 14.5, price_bottle: 249.99, price_glass: 14.00, description: 'Bordeaux-style blend' },
  { id: 5, name: 'Château d\'Yquem', producer: 'Lur-Saluces', country: 'France', region: 'Bordeaux', vintage_year: 2015, wine_type: 'dessert', bottle_size_ml: 375, glasses_per_bottle: 3, alcohol_content: 14.0, price_bottle: 199.99, price_glass: 18.00, description: 'Sweet dessert wine' },
  { id: 6, name: 'Pinot Noir', producer: 'Domaine de la Romanée-Conti', country: 'France', region: 'Burgundy', vintage_year: 2018, wine_type: 'still', bottle_size_ml: 750, glasses_per_bottle: 5, alcohol_content: 13.0, price_bottle: 599.99, price_glass: 25.00, description: 'Exceptional Pinot Noir' },
  { id: 7, name: 'Prosecco', producer: 'Mionetto', country: 'Italy', region: 'Veneto', vintage_year: 2020, wine_type: 'sparkling', bottle_size_ml: 750, glasses_per_bottle: 6, alcohol_content: 11.0, price_bottle: 19.99, price_glass: 4.00, description: 'Light and fruity prosecco' }
]

const mockInventory = [
  { id: 1, wine_id: 1, location: 'warehouse', bottles_count: 45 },
  { id: 2, wine_id: 2, location: 'bar', bottles_count: 12 },
  { id: 3, wine_id: 3, location: 'cellar', bottles_count: 30 },
  { id: 4, wine_id: 4, location: 'restaurant', bottles_count: 18 },
  { id: 5, wine_id: 5, location: 'warehouse', bottles_count: 25 },
  { id: 6, wine_id: 6, location: 'vip room', bottles_count: 8 },
  { id: 7, wine_id: 7, location: 'bar', bottles_count: 50 }
]

const mockSales = [
  { id: 1, wine_id: 1, product_type: 'bottle', quantity: 1, unit_price: 299.99, total_amount: 299.99, location: 'restaurant', customer_name: 'John Smith', sale_date: '2023-05-15T18:30:00' },
  { id: 2, wine_id: 2, product_type: 'glass', quantity: 2, unit_price: 12.00, total_amount: 24.00, location: 'bar', customer_name: 'Emma Johnson', sale_date: '2023-05-16T20:15:00' },
  { id: 3, wine_id: 3, product_type: 'bottle', quantity: 1, unit_price: 149.99, total_amount: 149.99, location: 'restaurant', customer_name: 'Michael Brown', sale_date: '2023-05-17T19:45:00' },
  { id: 4, wine_id: 4, product_type: 'glass', quantity: 3, unit_price: 14.00, total_amount: 42.00, location: 'bar', customer_name: 'Sarah Davis', sale_date: '2023-05-18T21:20:00' },
  { id: 5, wine_id: 1, product_type: 'bottle', quantity: 2, unit_price: 299.99, total_amount: 599.98, location: 'restaurant', customer_name: 'Robert Wilson', sale_date: '2023-05-19T17:30:00' },
  { id: 6, wine_id: 7, product_type: 'glass', quantity: 1, unit_price: 4.00, total_amount: 4.00, location: 'bar', customer_name: 'Lisa Miller', sale_date: '2023-05-20T19:10:00' },
  { id: 7, wine_id: 5, product_type: 'bottle', quantity: 1, unit_price: 199.99, total_amount: 199.99, location: 'vip room', customer_name: 'David Taylor', sale_date: '2023-05-21T22:00:00' }
]

// Computed properties
const totalBottles = computed(() => {
  return inventory.value.reduce((sum, item) => sum + item.bottles_count, 0)
})

const totalRevenue = computed(() => {
  return sales.value.reduce((sum, sale) => sum + sale.total_amount, 0)
})

// Methods
const handleMenuSelect = (index) => {
  activeMenu.value = index
}

const fetchData = async () => {
  // Если бэкенд недоступен, используем тестовые данные
  try {
    // Попытка получить данные с API
    const response = await fetch('/api/wines');
    if(response.ok) {
      const [winesRes, inventoryRes, salesRes] = await Promise.all([
        fetch('/api/wines'),
        fetch('/api/inventory'),
        fetch('/api/sales')
      ])
      
      wines.value = await winesRes.json()
      inventory.value = await inventoryRes.json()
      sales.value = await salesRes.json()
    } else {
      // Используем тестовые данные
      wines.value = mockWines
      inventory.value = mockInventory
      sales.value = mockSales
    }
  } catch (error) {
    // При ошибке подключения используем тестовые данные
    console.warn('Backend not available, using mock data:', error.message)
    wines.value = mockWines
    inventory.value = mockInventory
    sales.value = mockSales
  }
}

const refreshData = () => {
  fetchData()
}

onMounted(() => {
  fetchData()
})
</script>

<style>
.admin-container {
  height: 100vh;
}

.sidebar {
  background-color: #545c64;
  color: white;
  height: 100vh;
  /* Убрано position: fixed, теперь используем нормальный поток */
  position: relative;
  top: 0;
  left: 0;
  z-index: 100;
  transition: width 0.3s; /* Добавляем переход для плавного изменения ширины */
}

.logo {
  padding: 20px;
  text-align: center;
  border-bottom: 1px solid #444;
}

.sidebar-menu:not(.el-menu--collapse) {
  width: 200px;
}

.main-container {
  /* Добавлен отступ слева для компенсации ширины боковой панели */
  margin-left: 200px;
  transition: margin-left 0.3s; /* Плавный переход при изменении ширины */
}

.main-container.el-aside--collapse {
  margin-left: 64px; /* ширина свернутого меню */
}

.header {
  background-color: white;
  box-shadow: 0 1px 4px rgba(0,21,41,.08);
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.header-right {
  display: flex;
  gap: 10px;
}

.main-content {
  background-color: #f0f2f5;
  padding: 20px;
}

.dashboard-card {
  text-align: center;
}

.card-content h3 {
  margin: 0 0 10px 0;
  font-size: 14px;
  color: #666;
}

.card-content .count {
  font-size: 24px;
  font-weight: bold;
  color: #333;
  margin: 0;
}
</style>