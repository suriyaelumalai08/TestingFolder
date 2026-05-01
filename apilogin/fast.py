from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class LoginData(BaseModel):
    username: str
    password: str

@app.post("/api/login")
def login(data: LoginData):
    if data.username == "admin" and data.password == "123":
        return {"success": True}
    return {"success": False}

@app.get("/")
def root():
    return {"msg": "FastAPI running"}
