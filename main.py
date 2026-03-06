from fastapi import FastAPI , Query

app = FastAPI()


### Task_1

# Temporary data 
products = [
    {'id': 1, 'name': 'Bluetooth Headphones', 'price': 1299, 'category': 'Electronics', 'in_stock': True},
    {'id': 2, 'name': 'A4 Writing Notebook', 'price': 120, 'category': 'Stationery', 'in_stock': True},
    {'id': 3, 'name': 'Multiport USB Adapter', 'price': 899, 'category': 'Electronics', 'in_stock': False},
    {'id': 4, 'name': 'Premium Ball Pen Set', 'price': 150, 'category': 'Stationery', 'in_stock': True},
    {'id': 5, 'name': 'Mechanical Keyboard', 'price': 2499, 'category': 'Electronics', 'in_stock': True},
    {'id': 6, 'name': 'Desk Organizer', 'price': 299, 'category': 'Stationery', 'in_stock': True},
    {'id': 7, 'name': 'Laptop Cooling Pad', 'price': 999, 'category': 'Electronics', 'in_stock': False},
]

# Endpoint 0 — Home
@app.get('/')
def home():
    return {'message': 'Welcome to our E-commerce API'}

# Endpoint 1 — Return all products
@app.get('/products')
def get_all_products():
    return {'products': products, 'total': len(products)}

@app.get('/products/filter')
def filter_products(
    category: str = Query(None, description='Electronics or Stationery'),
    max_price: int = Query(None, description='Maximum price'),
    in_stock: bool = Query(None, description='True = in stock only')
):

    result = products   # start with all products

    if category:
        result = [p for p in result if p['category'] == category]

    if max_price:
        result = [p for p in result if p['price'] <= max_price]

    if in_stock is not None:
        result = [p for p in result if p['in_stock'] == in_stock]

    return {'filtered_products': result, 'count': len(result)}


# Endpoint 2 — Return only in-stock products

@app.get("/products/instock")
def get_instock():
    available = [p for p in products if p["in_stock"] == True]
    
    return {
        "in_stock_products": available,
        "count": len(available)
    }
# Endpoint 3 — Return one product by its ID
@app.get('/products/{product_id}')
def get_product(product_id: int):
    for product in products:
        if product['id'] == product_id:
            return {'product': product}
    return {'error': 'Product not found'}

# Endpoint 4 — Store summary
@app.get("/store/summary")
def store_summary():

    total_products = len(products)
    in_stock = len([p for p in products if p["in_stock"] == True])
    out_of_stock = total_products - in_stock
    categories = list(set([p["category"] for p in products]))

    return {
        "store_name": "My E-commerce Store",
        "total_products": total_products,
        "in_stock": in_stock,
        "out_of_stock": out_of_stock,
        "categories": categories
    }
# Endpoint  5 — Search products by name
@app.get("/products/search/{keyword}")
def search_products(keyword: str):

    matched = [p for p in products if keyword.lower() in p["name"].lower()]

    if len(matched) == 0:
        return {"message": "No products matched your search"}

    return {
        "matched_products": matched,
        "count": len(matched)
    }

# Endpoint 6 — Cheapest & Most Expensive Product
@app.get("/products/deals")
def get_deals():

    best_deal = min(products, key=lambda p: p["price"])
    premium_pick = max(products, key=lambda p: p["price"])

    return {
        "best_deal": best_deal,
        "premium_pick": premium_pick
    }