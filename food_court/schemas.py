from pydantic import BaseModel
from enum import Enum

class Vendor(BaseModel):
    name: str
    building: str
    floor: int
    phone: str
    email: str
    password: str

class ShowVendor(BaseModel):
    name: str
    phone: str
    email: str
    open : bool

    class Config():
        orm_mode = True

class UpdateVendor(BaseModel):
    status: bool

class Menu(BaseModel):
    name: str = ""
    desc: str = ""
    price: int
    out_of_stock: bool = False

class ShowMenu(BaseModel):
    name: str
    description: str
    price: int
    vendor: ShowVendor

    class Config():
        orm_mode = True

class User(BaseModel):
    name: str
    phone: str
    email: str
    password: str

class ShowUser(BaseModel):
    name: str
    phone: str
    email: str

    class Config():
        orm_mode = True

class Login(BaseModel):
    email: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
    user: ShowUser

    class Config():
        orm_mode = True

class TokenData(BaseModel):
    email: str | None = None


