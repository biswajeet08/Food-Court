from datetime import datetime, timedelta
from typing import Annotated, Union

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from .models import User, Vendor
from . import schemas, models, database, JWT
from sqlalchemy.orm import Session
from .routers import authentication


oauth2_scheme_user = OAuth2PasswordBearer(tokenUrl = "/login/user", scheme_name="user")
oauth2_scheme_vendor = OAuth2PasswordBearer(tokenUrl = "/login/vendor", scheme_name="vendor")

# async def get_user_table(user_type:str):
#     table_dict = {
#         "user":models.User,
#         "vendor": models.Vendor
#     }
#     if user_type not in table_dict.keys():
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User type does not exist")
#
#     return table_dict[user_type]


async def get_current_user(token: str = Depends(oauth2_scheme_user), db : Session = Depends(database.get_db)):

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, JWT.SECRET_KEY_USER, algorithms=[JWT.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = schemas.TokenData(email=email)
    except JWTError:
        raise credentials_exception
    vendor = db.query(models.User).filter(models.User.email == token_data.email).first()
    if vendor is None:
        raise credentials_exception
    return vendor


async def get_current_active_user(current_user = Depends(get_current_user)):
    # if current_user.disabled:
    #     raise HTTPException(status_code=400, detail="Inactive user")
    return current_user



async def get_current_vendor(token: str = Depends(oauth2_scheme_vendor), db : Session = Depends(database.get_db)):

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, JWT.SECRET_KEY_USER, algorithms=[JWT.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = schemas.TokenData(email=email)
    except JWTError:
        raise credentials_exception
    vendor = db.query(models.Vendor).filter(models.Vendor.email == token_data.email).first()
    if vendor is None:
        raise credentials_exception
    return vendor


async def get_current_active_vendor(current_user = Depends(get_current_vendor)):
    # if current_user.disabled:
    #     raise HTTPException(status_code=400, detail="Inactive user")
    return current_user