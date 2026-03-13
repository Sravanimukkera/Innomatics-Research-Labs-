from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

# Product Database
products = {
    1: {"name": "Wireless Mouse", "price": 499, "stock": True},
    2: {"name": "Notebook", "price": 99, "stock": True},
    3: {"name": "USB Hub", "price": 299, "stock": False},
    4: {"name": "Pen Set", "price": 49, "stock": True}
}

# Cart and Orders
cart = []
orders = []
order_id_counter = 1


class Checkout(BaseModel):
    customer_name: str
    delivery_address: str


# Add item to cart
@app.post("/cart/add")
def add_to_cart(product_id: int, quantity: int = 1):
    if product_id not in products:
        raise HTTPException(status_code=404, detail="Product not found")

    product = products[product_id]

    if not product["stock"]:
        raise HTTPException(status_code=400, detail=f"{product['name']} is out of stock")

    for item in cart:
        if item["product_id"] == product_id:
            item["quantity"] += quantity
            item["subtotal"] = item["quantity"] * product["price"]
            return {
                "message": "Cart updated",
                "cart_item": item
            }

    cart_item = {
        "product_id": product_id,
        "product_name": product["name"],
        "quantity": quantity,
        "unit_price": product["price"],
        "subtotal": quantity * product["price"]
    }

    cart.append(cart_item)

    return {
        "message": "Added to cart",
        "cart_item": cart_item
    }


# View cart
@app.get("/cart")
def view_cart():
    if not cart:
        return {"message": "Cart is empty"}

    grand_total = sum(item["subtotal"] for item in cart)

    return {
        "items": cart,
        "item_count": len(cart),
        "grand_total": grand_total
    }


# Remove item from cart
@app.delete("/cart/{product_id}")
def remove_item(product_id: int):
    for item in cart:
        if item["product_id"] == product_id:
            cart.remove(item)
            return {"message": "Item removed from cart"}

    raise HTTPException(status_code=404, detail="Item not found in cart")


# Checkout
@app.post("/cart/checkout")
def checkout(order: Checkout):
    global order_id_counter

    if not cart:
        raise HTTPException(status_code=400, detail="Cart is empty")

    order_list = []

    for item in cart:
        new_order = {
            "order_id": order_id_counter,
            "customer_name": order.customer_name,
            "product": item["product_name"],
            "quantity": item["quantity"],
            "subtotal": item["subtotal"]
        }

        orders.append(new_order)
        order_list.append(new_order)
        order_id_counter += 1

    grand_total = sum(item["subtotal"] for item in cart)

    cart.clear()

    return {
        "orders_placed": order_list,
        "grand_total": grand_total
    }


# View orders
@app.get("/orders")
def view_orders():
    return {
        "orders": orders,
        "total_orders": len(orders)
    }