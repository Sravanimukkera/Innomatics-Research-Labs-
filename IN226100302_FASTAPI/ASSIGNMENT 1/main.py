from fastapi import FastAPI

app = FastAPI()

products = [
    {"id": 1, "name": "Wireless Mouse", "price": 599, "category": "Electronics", "in_stock": True},
    {"id": 2, "name": "Notebook", "price": 49, "category": "Stationery", "in_stock": True},
    {"id": 3, "name": "Pen Set", "price": 99, "category": "Stationery", "in_stock": False},
    {"id": 4, "name": "USB Cable", "price": 199, "category": "Electronics", "in_stock": True},

    {"id": 5, "name": "Laptop Stand", "price": 899, "category": "Electronics", "in_stock": True},
    {"id": 6, "name": "Mechanical Keyboard", "price": 2499, "category": "Electronics", "in_stock": True},
    {"id": 7, "name": "Webcam", "price": 1499, "category": "Electronics", "in_stock": False}
]

@app.get("/products")
def get_products():
    return {"products": products, "total": len(products)}

@app.get("/products/category/{category_name}")
def category(category_name: str):
    result = [p for p in products if p["category"].lower() == category_name.lower()]
    if not result:
        return {"error": "No products found in this category"}
    return result

@app.get("/products/instock")
def instock():
    data = [p for p in products if p["in_stock"]]
    return {"in_stock_products": data, "count": len(data)}

@app.get("/store/summary")
def summary():
    total = len(products)
    instock = len([p for p in products if p["in_stock"]])
    outstock = total - instock
    categories = list(set([p["category"] for p in products]))

    return {
        "store_name": "My E-commerce Store",
        "total_products": total,
        "in_stock": instock,
        "out_of_stock": outstock,
        "categories": categories
    }

@app.get("/products/search/{keyword}")
def search(keyword: str):
    result = [p for p in products if keyword.lower() in p["name"].lower()]
    if not result:
        return {"message": "No products matched your search"}
    return {"matched_products": result, "count": len(result)}

@app.get("/products/deals")
def deals():
    cheapest = min(products, key=lambda x: x["price"])
    expensive = max(products, key=lambda x: x["price"])
    return {"best_deal": cheapest, "premium_pick": expensive}