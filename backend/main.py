from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import uuid
from datetime import datetime
from enum import Enum

app = FastAPI(title="Wine Admin Panel API", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Enums
class WineType(str, Enum):
    STILL = "still"
    SPARKLING = "sparkling"
    ROSE = "rose"
    DESSERT = "dessert"

class ProductType(str, Enum):
    BOTTLE = "bottle"
    GLASS = "glass"

# Models
class WineBase(BaseModel):
    name: str
    producer: str
    country: str
    region: str
    vintage_year: int
    bottle_size_ml: int
    glasses_per_bottle: int
    wine_type: WineType
    alcohol_content: float
    description: Optional[str] = None
    price_bottle: float
    price_glass: float

class WineCreate(WineBase):
    pass

class WineUpdate(BaseModel):
    name: Optional[str] = None
    producer: Optional[str] = None
    country: Optional[str] = None
    region: Optional[str] = None
    vintage_year: Optional[int] = None
    bottle_size_ml: Optional[int] = None
    glasses_per_bottle: Optional[int] = None
    wine_type: Optional[WineType] = None
    alcohol_content: Optional[float] = None
    description: Optional[str] = None
    price_bottle: Optional[float] = None
    price_glass: Optional[float] = None

class Wine(WineBase):
    id: str
    created_at: datetime
    updated_at: datetime

class InventoryItem(BaseModel):
    wine_id: str
    bottles_count: int
    location: str  # warehouse, bar, restaurant
    created_at: datetime
    updated_at: datetime

class InventoryUpdate(BaseModel):
    bottles_count: int

class Sale(BaseModel):
    id: str
    wine_id: str
    product_type: ProductType
    quantity: int
    unit_price: float
    total_amount: float
    location: str
    sale_date: datetime
    customer_name: Optional[str] = None

class SaleCreate(BaseModel):
    wine_id: str
    product_type: ProductType
    quantity: int
    location: str
    customer_name: Optional[str] = None

# In-memory storage (in real app, use database)
wines_db: List[Wine] = []
inventory_db: List[InventoryItem] = []
sales_db: List[Sale] = []

def generate_id():
    return str(uuid.uuid4())

@app.get("/")
async def root():
    return {"message": "Wine Admin Panel API"}

@app.get("/wines", response_model=List[Wine])
async def get_wines():
    return wines_db

@app.post("/wines", response_model=Wine)
async def create_wine(wine: WineCreate):
    wine_obj = Wine(
        id=generate_id(),
        **wine.dict(),
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    wines_db.append(wine_obj)
    # Initialize inventory for this wine
    inventory_item = InventoryItem(
        wine_id=wine_obj.id,
        bottles_count=0,
        location="warehouse",
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    inventory_db.append(inventory_item)
    return wine_obj

@app.get("/wines/{wine_id}", response_model=Wine)
async def get_wine(wine_id: str):
    for wine in wines_db:
        if wine.id == wine_id:
            return wine
    raise HTTPException(status_code=404, detail="Wine not found")

@app.put("/wines/{wine_id}", response_model=Wine)
async def update_wine(wine_id: str, wine_update: WineUpdate):
    for i, wine in enumerate(wines_db):
        if wine.id == wine_id:
            update_data = wine_update.dict(exclude_unset=True)
            updated_wine = wine.copy(update={**update_data, "updated_at": datetime.now()})
            wines_db[i] = updated_wine
            return updated_wine
    raise HTTPException(status_code=404, detail="Wine not found")

@app.delete("/wines/{wine_id}")
async def delete_wine(wine_id: str):
    global wines_db
    wines_db = [wine for wine in wines_db if wine.id != wine_id]
    # Also remove related inventory
    global inventory_db
    inventory_db = [item for item in inventory_db if item.wine_id != wine_id]
    # Also remove related sales
    global sales_db
    sales_db = [sale for sale in sales_db if sale.wine_id != wine_id]
    return {"message": "Wine deleted successfully"}

@app.get("/inventory", response_model=List[InventoryItem])
async def get_inventory():
    return inventory_db

@app.get("/inventory/{wine_id}", response_model=InventoryItem)
async def get_inventory_by_wine(wine_id: str):
    for item in inventory_db:
        if item.wine_id == wine_id:
            return item
    raise HTTPException(status_code=404, detail="Inventory item not found")

@app.put("/inventory/{wine_id}", response_model=InventoryItem)
async def update_inventory(wine_id: str, inventory_update: InventoryUpdate):
    for i, item in enumerate(inventory_db):
        if item.wine_id == wine_id:
            # Update the bottles count
            updated_item = item.copy(update={
                "bottles_count": inventory_update.bottles_count,
                "updated_at": datetime.now()
            })
            inventory_db[i] = updated_item
            return updated_item
    raise HTTPException(status_code=404, detail="Inventory item not found")

@app.get("/sales", response_model=List[Sale])
async def get_sales():
    return sales_db

@app.post("/sales", response_model=Sale)
async def create_sale(sale: SaleCreate):
    # Find the wine
    wine = None
    for w in wines_db:
        if w.id == sale.wine_id:
            wine = w
            break
    
    if not wine:
        raise HTTPException(status_code=404, detail="Wine not found")
    
    # Check inventory if selling bottles
    if sale.product_type == ProductType.BOTTLE:
        inventory_item = None
        for item in inventory_db:
            if item.wine_id == sale.wine_id and item.location == sale.location:
                inventory_item = item
                break
        
        if not inventory_item or inventory_item.bottles_count < sale.quantity:
            raise HTTPException(status_code=400, detail="Not enough bottles in inventory")
        
        # Update inventory
        for i, item in enumerate(inventory_db):
            if item.wine_id == sale.wine_id and item.location == sale.location:
                inventory_db[i] = item.copy(update={
                    "bottles_count": item.bottles_count - sale.quantity,
                    "updated_at": datetime.now()
                })
                break
    
    # Calculate prices
    unit_price = wine.price_bottle if sale.product_type == ProductType.BOTTLE else wine.price_glass
    total_amount = unit_price * sale.quantity
    
    sale_obj = Sale(
        id=generate_id(),
        wine_id=sale.wine_id,
        product_type=sale.product_type,
        quantity=sale.quantity,
        unit_price=unit_price,
        total_amount=total_amount,
        location=sale.location,
        sale_date=datetime.now(),
        customer_name=sale.customer_name
    )
    sales_db.append(sale_obj)
    return sale_obj

@app.get("/reports/sales-by-vintage")
async def get_sales_by_vintage():
    """Get sales grouped by wine vintage year"""
    report = {}
    for sale in sales_db:
        # Get wine info
        wine = next((w for w in wines_db if w.id == sale.wine_id), None)
        if wine:
            key = f"{wine.name} {wine.vintage_year}"
            if key not in report:
                report[key] = {
                    "wine_name": wine.name,
                    "vintage_year": wine.vintage_year,
                    "bottles_sold": 0,
                    "glasses_sold": 0,
                    "total_revenue": 0.0
                }
            
            if sale.product_type == ProductType.BOTTLE:
                report[key]["bottles_sold"] += sale.quantity
            else:
                report[key]["glasses_sold"] += sale.quantity
            
            report[key]["total_revenue"] += sale.total_amount
    
    return list(report.values())

@app.get("/reports/inventory-by-location")
async def get_inventory_by_location():
    """Get inventory grouped by location"""
    report = {}
    for item in inventory_db:
        if item.location not in report:
            report[item.location] = []
        
        # Get wine info
        wine = next((w for w in wines_db if w.id == item.wine_id), None)
        if wine:
            report[item.location].append({
                "wine_name": wine.name,
                "vintage_year": wine.vintage_year,
                "producer": wine.producer,
                "bottles_count": item.bottles_count,
                "glasses_available": item.bottles_count * wine.glasses_per_bottle
            })
    
    return report