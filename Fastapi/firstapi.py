from fastapi import Fastapi

app=Fastapi()


@app.get("/")
async def index():
    return {'hello':'suriya'}