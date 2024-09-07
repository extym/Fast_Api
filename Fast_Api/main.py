from __future__ import annotations

import datetime

import uvicorn
from fastapi import Request, FastAPI, Cookie, Header, HTTPException
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
    # try:
    all.append({"name": feedback.name, 'message': feedback.message})
    return {'result': f'All_ride, {feedback.name}!'}
    # except Exception as err:
    #     return {'error': '{}'.format(err)}


@app.get("/items/")
async def read_items(request: Request,  response: Response,
                     user_agent: Annotated[str | None, Header()] = None):
    response.set_cookie(key="falala", value="oxoxoxo")
    headers = dict(request.headers)
    return {"User-Agent": user_agent, "1": headers}


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
def search_product(keyword: str, limit:int = 10, category:str = None):
    proxy = []
    for product in sample_products:
        if keyword in product.get('name') \
                and product.get('category') == category:
            proxy.append(product)

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


@app.post('/login')
# @app.get('/login')
def login(response: Response , user: User):
    if user.name in users_login and user.password == users_login.get(user.name):
        response.set_cookie(key='access_token', value='23114151')
        return JSONResponse({"message": "all ride"})  #Jinja2Templates('index.html')
    # response.delete_cookie("access_token")
    return Response(content="Unauthorized",
                    status_code=401)


@app.get('/luser')
def luses(response: Response, request: Request):
    response.set_cookie(key="last_visit", value=str(datetime.datetime.now()))


@app.get('/user')
@app.post('/user/{id}')
def check_user(request: Request,
               response: Response, id: int = None):
    if request.cookies.get('access_token'):
        print('xexe')
    # if user.age >= 18:
    #     user.is_adult = True
    # if id in fake_users:
    #     return HTMLResponse('Hi')
        return JSONResponse("dict(user)")
    response.set_cookie(key="last_visit", value=str(datetime.time))
    return Response(content="Unautorized user",
                    status_code=401)


@app.get('/')
async def get_smth(last_visit = Cookie()):
    return  {"last visit": last_visit}


@app.get("/index")
async def get_index(request: Request):
    return template.TemplateResponse("index.html", {"request": request})


@app.post("/calculate", response_class=HTMLResponse)
async def calculate(item: Item):
    result = item.num1 + item.num2
    return JSONResponse({'result': result})


@app.get('/headers')
async def get_headers(user_agent: Annotated[str | None, Header()] = None,
                      accept_language: Annotated[str | None, Header()] = None):
    if accept_language != "en-US,en;q=0.9,es;q=0.8" or not user_agent:
        raise HTTPException(status_code=400, detail="Not found needed headers")
    return JSONResponse({"User-agent": user_agent, "Accept-Language": accept_language})




def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.

# Press the green button in the gutter to run the script.
# if __name__ == '__main__':
#     print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
