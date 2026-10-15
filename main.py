from fastapi import Depends, FastAPI
from models import Product
from config import session, engine
import db_model

from sqlalchemy.orm import Session

app = FastAPI()

db_model.Base.metadata.create_all(bind=engine)

products = [
    Product(id=1, category="Electronics", price=999, quantity=10),
    Product(id=2, category="Accessories", price=25, quantity=50),
    Product(id=3, category="Office", price=80, quantity=25),
]

# a function to pouplate the db initially
def populate_db():
    db = session()  #open a db session
    count = db.query(db_model.Product).count

    if count == 0:  # if db is empty, add each product
        for product in products:
            db.add(db_model.Product(**product.model_dump()))
        db.commit()

    db.close()

def get_db():
    db = session()
    try:
        yield db    # wait for db work by others
    finally:
        db.close()  # close the session


@app.get("/health")
def get_health():
    return "app is healthy"

@app.get("/products")
def get_all_products(db: Session = Depends(get_db)):    # this is dependency injection

    # fetch from the db
    products = db.query(db_model.Product).all()
    return products

@app.get("/products/{id}")
def get_product_by_id(id: int, db: Session = Depends(get_db)):

    #find the product with the id from the db
    product = db.query(db_model.Product).filter(db_model.Product.id == id).first()
    if product:
        return product
    return f"product with id: {id} not found"

@app.post("/products")
def create_product(product: Product, db: Session = Depends(get_db)):
    # add the product to the db
    db.add(db_model.Product(**product.model_dump()))    # convert from pydantic to db_model type and then add to db
    db.commit()
    return product

@app.put("/products/{id}")
def update_product(id: int, product: Product, db: Session = Depends(get_db)):
    #fetch the product with id from the db
    db_product = db.query(db_model.Product).filter(db_model.Product.id == id).first()
    
    if db_product:  # if it exists, update the fields as per the request
        updated_product = product.model_dump(exclude_unset=True) # only the provided ones are updated
        for k, v in updated_product.items():
            setattr(db_product, k, v)
        db.commit()
        return db_product
        
    return f"product with id: {id} not found"

@app.delete("/products/{id}")
def delete_product_by_id(id: int, db: Session = Depends(get_db)):

    product = db.query(db_model.Product).filter(db_model.Product.id == id).first()
    if product:
            db.delete(product)
            db.commit()
            return f"deleted the product with id: {id} successfully"
    return f"product with id: {id} not found"