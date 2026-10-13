from pydantic import BaseModel

class Product(BaseModel):
    id: int
    category: str
    price: int
    quantity: int
