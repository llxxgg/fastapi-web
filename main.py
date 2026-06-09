import uvicorn
from fastapi import FastAPI

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
def get_user(id: int):
    return {"user_id": id}

@app.get("/users")
def page_limit(page: int, limit: int = None):
    if limit:
        return {"page": page, "limit": limit}
    
    return {"page": page}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)