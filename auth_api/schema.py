from pydantic import BaseModel

class usercreate(BaseModel):
    username:str
    password:str
    role:str


class loginuser(BaseModel):
    username:str
    password:str

    