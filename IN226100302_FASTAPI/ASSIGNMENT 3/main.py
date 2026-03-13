from fastapi import FastAPI, HTTPException

app = FastAPI()

# Initial Products
products = [
    {"id": 1, "name": "Keyboard", "price": 499, "category": "Electronics", "in_stock": True},
    {"id": 2, "name": "Notebook", "price": 99, "category": "Stationery", "in_stock": True},
    {"id": 3, "name": "USB Hub", "price": 799, "category": "Electronics", "in_stock": False},
    {"id": 4, "name": "Pen Set", "price": 49, "category": "Stationery", "in_stock": True}
]

# Home API
@app.get("/")
def home():
    return {"message": "FastAPI Assignment 3 Running"}

# Get all products
@app.get("/products")
def get_products():
    return {"products": products, "total": len(products)}

# Add product
@app.post("/products")
def add_product(product: dict):

    # check duplicate name
    for p in products:
        if p["name"].lower() == product["name"].lower():
            raise HTTPException(status_code=400, detail="Product already exists")

    new_id = max(p["id"] for p in products) + 1
    product["id"] = new_id

    products.append(product)

    return {"message": "Product added", "product": product}

# Update product
@app.put("/products/{product_id}")
def update_product(product_id: int, price: int = None, in_stock: bool = None):

    for p in products:

        if p["id"] == product_id:

            if price is not None:
                p["price"] = price

            if in_stock is not None:
                p["in_stock"] = in_stock

            return {"message": "Product updated", "product": p}

    raise HTTPException(status_code=404, detail="Product not found")

# Delete product
@app.delete("/products/{product_id}")
def delete_product(product_id: int):

    for p in products:

        if p["id"] == product_id:

            products.remove(p)

            return {"message": f"Product '{p['name']}' deleted"}

    raise HTTPException(status_code=404, detail="Product not found")

# Inventory audit summary
@app.get("/products/audit")
def product_audit():

    total_products = len(products)

    in_stock_products = [p for p in products if p["in_stock"]]

    out_of_stock = [p["name"] for p in products if not p["in_stock"]]

    total_stock_value = sum(p["price"] * 10 for p in in_stock_products)

    most_expensive = max(products, key=lambda x: x["price"])

    return {
        "total_products": total_products,
        "in_stock_count": len(in_stock_products),
        "out_of_stock_names": out_of_stock,
        "total_stock_value": total_stock_value,
        "most_expensive": {
            "name": most_expensive["name"],
            "price": most_expensive["price"]
        }
    }

# Get single product
@app.get("/products/{product_id}")
def get_product(product_id: int):

    for p in products:

        if p["id"] == product_id:
            return p

    raise HTTPException(status_code=404, detail="Product not found")