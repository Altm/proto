import asyncio
import httpx
import json

async def test_api():
    base_url = "http://localhost:8000"
    
    print("Testing FastAPI Wine Admin Panel API...")
    
    # Test 1: Get wines (should return empty list initially)
    print("\n1. Testing GET /wines")
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{base_url}/wines")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
    
    # Test 2: Create a wine
    print("\n2. Testing POST /wines")
    new_wine = {
        "name": "Château Margaux",
        "producer": "Château Margaux",
        "country": "France",
        "region": "Bordeaux",
        "vintage_year": 2018,
        "bottle_size_ml": 750,
        "glasses_per_bottle": 5,
        "wine_type": "still",
        "alcohol_content": 13.5,
        "price_bottle": 250.00,
        "price_glass": 15.00,
        "description": "Premium French red wine"
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{base_url}/wines", json=new_wine)
        print(f"Status: {response.status_code}")
        created_wine = response.json()
        print(f"Created wine ID: {created_wine.get('id')}")
    
    # Test 3: Get wines again (should return the created wine)
    print("\n3. Testing GET /wines after creation")
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{base_url}/wines")
        print(f"Status: {response.status_code}")
        wines = response.json()
        print(f"Number of wines: {len(wines)}")
        if wines:
            print(f"Wine name: {wines[0]['name']}")
    
    # Test 4: Get inventory
    print("\n4. Testing GET /inventory")
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{base_url}/inventory")
        print(f"Status: {response.status_code}")
        inventory = response.json()
        print(f"Number of inventory items: {len(inventory)}")
        if inventory:
            print(f"Inventory for wine ID: {inventory[0]['wine_id']}")
    
    # Test 5: Get reports
    print("\n5. Testing GET /reports/sales-by-vintage")
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{base_url}/reports/sales-by-vintage")
        print(f"Status: {response.status_code}")
        report = response.json()
        print(f"Sales report entries: {len(report)}")
    
    print("\nAPI tests completed successfully!")

if __name__ == "__main__":
    asyncio.run(test_api())