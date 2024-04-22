from __future__ import annotations


import uvicorn
from fastapi import Request, FastAPI, Cookie, Header
from fastapi.responses import HTMLResponse, JSONResponse, Response
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from typing import Annotated
from models.models import User, Feedback, UserCreate


app = FastAPI()
template = Jinja2Templates(directory='templates')


class Item(BaseModel):
    num1: int
    num2: int


fake_users = {
    1: {"username": "john_doe", "email": "john@example.com"},
    2: {"username": "jane_smith", "email": "jane@example.com"},
}


@app.get('/users/{id}')
def get_someone(id: int):
    if id in fake_users:
        return fake_users.get(id)
    return {'error': 'User not found'}


all = []
users = []

@app.post('/messages')
def got_user_message(feedback: Feedback):
    try:
        all.append({"name": feedback.name, 'message': feedback.message})
        return {'result': 'All_ride'}
    except Exception as err:
        return {'error': '{}'.format(err)}


@app.get("/items/")
async def read_items(user_agent: Annotated[str | None, Header()] = None):
    return {"User-Agent": user_agent}


@app.post('/create_user')
def create_user(create_user: UserCreate):
    user = {
        'name': create_user.name,
        'email': create_user.email,
        'age': create_user.age,
        'is_subscribed': create_user.is_subscribed
    }
    users.append(user)
    return JSONResponse(user)

from test import *
@app.get('/products/search')
def search_product(limit:int = 10, keyword: str = None, category:str = None):
    proxy = []
    for product in sample_products:
        if product.get('keyword') == keyword \
                or product.get('category') == category:
            proxy.append({
                "product_id": product.get('product_id'),
                "name": product.get('name'),
                "category": product.get('category'),
                "price": product.get('price')
            })

    return proxy[:limit]


@app.get('/product/{product_id}')
def prod_id(product_id: int):
    proxy = []
    for prod in sample_products:
        if prod.get('product_id') == product_id:
            # proxy.append(prod)
            return prod

    # return proxy

users_login = {"user123": "password123"}

@app.get('/login')
def login(response: Response , username: str, userpass: str):
    if username in users_login and users_login.get(username) == userpass:
        response.set_cookie(key='access_token', value='23114151')



@app.post('/user')
def check_user(user: User):
    if user.age >= 18:
        user.is_adult = True

    return JSONResponse(dict(user))


@app.get('/')
async def get_smth():
    return {'message': "Hello World"}


@app.get("/index")
async def get_index(request: Request):
    return template.TemplateResponse("index.html", {"request": request})


@app.post("/calculate", response_class=HTMLResponse)
async def calculate(item: Item):
    result = item.num1 + item.num2
    return JSONResponse({'result': result})


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.

# Press the green button in the gutter to run the script.
# if __name__ == '__main__':
#     print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
