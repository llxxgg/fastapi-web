from enum import Enum

import uvicorn
from fastapi import FastAPI, Query
from pydantic import BaseModel
from typing import Union

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "你好"}

# 路径参数
@app.get("/args/{id}")
def path_args(id: int):
    return {"id": id}

# 请求参数
@app.get("/user")
def get_user(id: Union[int,str]):
    return {"user_id": id}

@app.get("/users")
def page_limit(page: int, limit: int = None):
    if limit:
        return {"page": page, "limit": limit}
    
    return {"page": page}

class User(BaseModel):
    id: int
    name: str
    password: str | None = None
    sex: str = "男"

@app.post("/user")
def create_user(user: User):
    return user

@app.get("/get_item")
def get_item(id: str = Query("123")):
    return {"id": id}

class ModelName(str, Enum):
    alexa = "alexa"
    reuters = "reuters"
    lenet = "lenet"

@app.get("/item2/{model}")
def get_item2(model: ModelName):
    return {"model": model}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)