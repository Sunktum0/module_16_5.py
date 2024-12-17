
from fastapi import FastAPI, HTTPException, Request
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, conint
from typing import List, Annotated
from fastapi.responses import HTMLResponse

app = FastAPI()

# Создание объекта Jinja2Templates
templates = Jinja2Templates(directory="templates")

# Пустой список пользователей
users = []

# Класс модели пользователя
class User(BaseModel):
    id: int
    username: str
    age: conint(ge=0)  # Возраст должен быть неотрицательным

# Создание нескольких пользователей при запуске
users.append(User(id=1, username="UrbanUser", age=24))
users.append(User(id=2, username="UrbanTest", age=22))
users.append(User(id=3, username="Capybara", age=60))

# Главная страница, отображающая всех пользователей
@app.get("/", response_class=HTMLResponse)
async def read_users(request: Request):
    return templates.TemplateResponse("users.html", {"request": request, "users_list": users, "title": "User List"})

# GET запрос для получения конкретного пользователя по ID
@app.get("/user/{user_id}", response_class=HTMLResponse)
async def get_user(request: Request, user_id: int):
    for user in users:
        if user.id == user_id:
            return templates.TemplateResponse("users.html", {"request": request, "user": user, "title": f"User: {user.username}"})
    raise HTTPException(status_code=404, detail="User was not found")

# Прочие CRUD запросы ...

# POST запрос для добавления нового пользователя
@app.post("/user/", response_model=User)
async def create_user(user: Annotated[User, ...]):  # Используем Annotated для валидации
    user_id = 1 if not users else users[-1].id + 1
    new_user = User(id=user_id, username=user.username, age=user.age)
    users.append(new_user)
    return new_user

# PUT запрос для обновления существующего пользователя
@app.put("/user/{user_id}", response_model=User)
async def update_user(user_id: int, user: Annotated[User, ...]):
    for existing_user in users:
        if existing_user.id == user_id:
            existing_user.username = user.username
            existing_user.age = user.age
            return existing_user
    raise HTTPException(status_code=404, detail="User was not found")

# DELETE запрос для удаления пользователя
@app.delete("/user/{user_id}", response_model=User)
async def delete_user(user_id: int):
    for index, existing_user in enumerate(users):
        if existing_user.id == user_id:
            removed_user = users.pop(index)
            return removed_user
    raise HTTPException(status_code=404, detail="User was not found")