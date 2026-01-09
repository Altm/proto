# Wine Admin Panel Prototype

This is a prototype for a wine administration panel built with FastAPI (backend) and Vue3 (frontend) with Element Plus UI components.

## Features

- **Wine Management**: Create, update, delete wines with vintage year tracking
- **Inventory Management**: Track bottles and convert to glasses available
- **Sales Management**: Record sales of bottles and glasses
- **Reporting**: Sales by vintage year and inventory by location
- **Responsive UI**: Built with Element Plus for a professional admin experience

## Architecture

- **Backend**: FastAPI with in-memory storage (for prototype)
- **Frontend**: Vue3 with Element Plus components
- **API Communication**: Axios for HTTP requests

## Requirements

- Python 3.8+
- Node.js 16+

## Setup Instructions

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd /workspace/backend
   ```

2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the FastAPI server:
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd /workspace/frontend
   ```

2. Install Node.js dependencies:
   ```bash
   npm install
   ```

3. Start the Vue development server:
   ```bash
   npm run dev
   ```

## API Endpoints

The backend provides the following API endpoints:

- `GET /wines` - Get all wines
- `POST /wines` - Create a new wine
- `PUT /wines/{id}` - Update a wine
- `DELETE /wines/{id}` - Delete a wine
- `GET /inventory` - Get all inventory items
- `PUT /inventory/{wine_id}` - Update inventory for a wine
- `GET /sales` - Get all sales
- `POST /sales` - Record a new sale
- `GET /reports/sales-by-vintage` - Get sales report by vintage
- `GET /reports/inventory-by-location` - Get inventory report by location

## Frontend Views

- **Dashboard**: Overview with key metrics
- **Wines**: Manage wine catalog with vintage tracking
- **Inventory**: Track bottles and glasses by location
- **Sales**: Record and view sales transactions
- **Reports**: View sales and inventory reports

## Key Features Implemented

1. **Vintage Year Tracking**: Each wine is uniquely identified by name and vintage year
2. **Bottle/Glass Conversion**: Track inventory in bottles but show available glasses
3. **Location-based Inventory**: Separate tracking for warehouse, bar, and restaurant
4. **Sale Types**: Support for selling both bottles and glasses
5. **Comprehensive Reporting**: Sales by vintage and inventory by location

## Notes

- This is a prototype implementation with in-memory storage
- In a production environment, you would replace in-memory storage with a proper database
- The frontend connects to the backend API at `http://localhost:8000`
- CORS is enabled to allow frontend-backend communication