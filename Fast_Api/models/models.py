from pydantic import BaseModel, EmailStr


class User(BaseModel):
    name: str
    age: int
    is_adult: bool = False


class Feedback(BaseModel):
    name: str
    message: str


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    age: int = 0
    is_subscribed: bool = False


# class Product(BaseModel):
#     keyword: str
#     name: str
#     category: str = None
#     price: float = 0.00
#     product_id: int