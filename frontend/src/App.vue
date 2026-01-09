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
            <el-icon><Glass /></el-icon>
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

      <el-container>
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
import { House, Glass, Box, Money, Document, Fold, Expand } from '@element-plus/icons-vue'
import axios from 'axios'
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
  try {
    const [winesRes, inventoryRes, salesRes] = await Promise.all([
      axios.get('http://localhost:8000/wines'),
      axios.get('http://localhost:8000/inventory'),
      axios.get('http://localhost:8000/sales')
    ])
    
    wines.value = winesRes.data
    inventory.value = inventoryRes.data
    sales.value = salesRes.data
  } catch (error) {
    console.error('Error fetching data:', error)
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
  position: fixed;
  top: 0;
  left: 0;
  z-index: 100;
}

.logo {
  padding: 20px;
  text-align: center;
  border-bottom: 1px solid #444;
}

.sidebar-menu:not(.el-menu--collapse) {
  width: 200px;
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