from fastapi import FastAPI

from app.router import friend_router, health_router

app = FastAPI()
app.include_router(friend_router)
app.include_router(health_router)
@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
