from fastapi import FastAPI
from models import Product
from config import session, engine
import db_model

app = FastAPI()

db_model.Base.metadata.create_all(bind=engine)

products = []

@app.get("/health")
def get_health():
    return "app is healthy"

@app.get("/products")
def get_all_products():
    return products

@app.get("/products/{id}")
def get_product_by_id(id: int):
    for prod in products:
        if prod.id == id:
            return prod
    return f"product with id: {id} not found"

@app.post("/products")
def create_product(product: Product):
    products.append(product)
    return product

@app.put("/products/{id}")
def update_product(id: int, product: Product):
    for i in range(len(products)):
        if products[i].id == id:
            products[i] = product
            return products[i]
    return f"product with id: {id} not found"

@app.delete("/products/{id}")
def delete_product_by_id(id: int):
    for prod in products:
        if prod.id == id:
            deleted_product = prod
            del prod
            return deleted_product
    return f"product with id: {id} not found"

@app.get("/products")
def get_all_products():
    return products

@app.get("/products/{id}")
def get_product_by_id(id: int):
    for prod in products:
        if prod.id == id:
            return prod
    return f"product with id: {id} not found"

@app.post("/products")
def create_product(product: Product):
    products.append(product)
    return product

@app.put("/products/{id}")
def update_product(id: int, product: Product):
    for i in range(len(products)):
        if products[i].id == id:
            products[i] = product
            return products[i]
    return f"product with id: {id} not found"

@app.delete("/products/{id}")
def delete_product_by_id(id: int):
    for prod in products:
        if prod.id == id:
            deleted_product = prod
            del prod
            return deleted_product
    return f"product with id: {id} not found"