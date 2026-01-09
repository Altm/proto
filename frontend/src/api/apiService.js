import axios from 'axios'

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

let winesData = [...mockWines]
let inventoryData = [...mockInventory]
let salesData = [...mockSales]

// Вспомогательная функция для проверки доступности бэкенда
const isBackendAvailable = async () => {
  try {
    const response = await axios.get('/api/wines', { timeout: 2000 })
    return response.status === 200
  } catch (error) {
    return false
  }
}

// Функция для генерации ID
const generateId = (data) => {
  return data.length > 0 ? Math.max(...data.map(item => item.id)) + 1 : 1
}

export const apiService = {
  // Wines API
  getWines: async () => {
    const backendAvailable = await isBackendAvailable()
    
    if (backendAvailable) {
      try {
        const response = await axios.get('/api/wines')
        return response.data
      } catch (error) {
        console.warn('Backend not available, using mock data:', error.message)
        return winesData
      }
    }
    
    return winesData
  },

  createWine: async (wineData) => {
    const backendAvailable = await isBackendAvailable()
    
    if (backendAvailable) {
      try {
        const response = await axios.post('/api/wines', wineData)
        return response.data
      } catch (error) {
        console.warn('Backend not available, using mock data:', error.message)
        const newWine = { ...wineData, id: generateId(winesData) }
        winesData.push(newWine)
        return newWine
      }
    }
    
    const newWine = { ...wineData, id: generateId(winesData) }
    winesData.push(newWine)
    return newWine
  },

  updateWine: async (id, wineData) => {
    const backendAvailable = await isBackendAvailable()
    
    if (backendAvailable) {
      try {
        const response = await axios.put(`/api/wines/${id}`, wineData)
        return response.data
      } catch (error) {
        console.warn('Backend not available, using mock data:', error.message)
        const index = winesData.findIndex(wine => wine.id === id)
        if (index !== -1) {
          winesData[index] = { ...winesData[index], ...wineData }
          return winesData[index]
        }
        throw new Error('Wine not found')
      }
    }
    
    const index = winesData.findIndex(wine => wine.id === id)
    if (index !== -1) {
      winesData[index] = { ...winesData[index], ...wineData }
      return winesData[index]
    }
    throw new Error('Wine not found')
  },

  deleteWine: async (id) => {
    const backendAvailable = await isBackendAvailable()
    
    if (backendAvailable) {
      try {
        await axios.delete(`/api/wines/${id}`)
        return
      } catch (error) {
        console.warn('Backend not available, using mock data:', error.message)
        const index = winesData.findIndex(wine => wine.id === id)
        if (index !== -1) {
          winesData.splice(index, 1)
        }
        return
      }
    }
    
    const index = winesData.findIndex(wine => wine.id === id)
    if (index !== -1) {
      winesData.splice(index, 1)
    }
  },

  // Inventory API
  getInventory: async () => {
    const backendAvailable = await isBackendAvailable()
    
    if (backendAvailable) {
      try {
        const response = await axios.get('/api/inventory')
        return response.data
      } catch (error) {
        console.warn('Backend not available, using mock data:', error.message)
        return inventoryData
      }
    }
    
    return inventoryData
  },

  updateInventory: async (wineId, inventoryData) => {
    const backendAvailable = await isBackendAvailable()
    
    if (backendAvailable) {
      try {
        const response = await axios.put(`/api/inventory/${wineId}`, inventoryData)
        return response.data
      } catch (error) {
        console.warn('Backend not available, using mock data:', error.message)
        const index = inventoryData.findIndex(item => item.wine_id === wineId)
        if (index !== -1) {
          inventoryData[index] = { ...inventoryData[index], ...inventoryData }
          return inventoryData[index]
        } else {
          const newItem = { ...inventoryData, wine_id: wineId, id: generateId(inventoryData) }
          inventoryData.push(newItem)
          return newItem
        }
      }
    }
    
    const index = inventoryData.findIndex(item => item.wine_id === wineId)
    if (index !== -1) {
      inventoryData[index] = { ...inventoryData[index], ...inventoryData }
      return inventoryData[index]
    } else {
      const newItem = { ...inventoryData, wine_id: wineId, id: generateId(inventoryData) }
      inventoryData.push(newItem)
      return newItem
    }
  },

  // Sales API
  getSales: async () => {
    const backendAvailable = await isBackendAvailable()
    
    if (backendAvailable) {
      try {
        const response = await axios.get('/api/sales')
        return response.data
      } catch (error) {
        console.warn('Backend not available, using mock data:', error.message)
        return salesData
      }
    }
    
    return salesData
  },

  createSale: async (saleData) => {
    const backendAvailable = await isBackendAvailable()
    
    if (backendAvailable) {
      try {
        const response = await axios.post('/api/sales', saleData)
        return response.data
      } catch (error) {
        console.warn('Backend not available, using mock data:', error.message)
        const newSale = { 
          ...saleData, 
          id: generateId(salesData),
          sale_date: new Date().toISOString(),
          total_amount: saleData.quantity * (saleData.product_type === 'bottle' ? 
            winesData.find(w => w.id === saleData.wine_id)?.price_bottle : 
            winesData.find(w => w.id === saleData.wine_id)?.price_glass || 0)
        }
        salesData.push(newSale)
        return newSale
      }
    }
    
    const newSale = { 
      ...saleData, 
      id: generateId(salesData),
      sale_date: new Date().toISOString(),
      total_amount: saleData.quantity * (saleData.product_type === 'bottle' ? 
        winesData.find(w => w.id === saleData.wine_id)?.price_bottle : 
        winesData.find(w => w.id === saleData.wine_id)?.price_glass || 0)
    }
    salesData.push(newSale)
    return newSale
  }
}