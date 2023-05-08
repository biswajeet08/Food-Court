from fastapi import APIRouter, Depends, status, HTTPException
from .. import schemas, models, database, JWT
from .. utils import Hash
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(
    tags=["Authentication"]
)
#
# async def get_user_table(user_type:str):
#     table_dict = {
#         "user":models.User,
#         "vendor": models.Vendor
#     }
#     if user_type not in table_dict.keys():
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User type does not exist")
#
#     return table_dict[user_type]

# class Form(OAuth2PasswordRequestForm):
#     def __init__(self, user_table = Depends(get_user_table)):
#         self.user_table = user_table

@router.post("/login/user", response_model=schemas.Token,status_code = status.HTTP_200_OK)
async def login(request: OAuth2PasswordRequestForm= Depends(), db : Session = Depends(database.get_db)):

    # table = request.user_table
    end_user = db.query(models.User).filter(models.User.email == request.username).first()

    if not end_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User Not Found")

    if not Hash.verify(end_user.password, request.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Incorrect Password")

    access_token_expires = timedelta(minutes=JWT.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = JWT.create_access_token(
        data={"sub": end_user.email}, expires_delta=access_token_expires
    )
    return {"user": end_user, "access_token": access_token, "token_type": "bearer"}


@router.post("/login/vendor", status_code = status.HTTP_200_OK)
async def login_vendor(request: OAuth2PasswordRequestForm= Depends(), db : Session = Depends(database.get_db)):

    vendor = db.query(models.Vendor).filter(models.Vendor.email == request.username).first()

    if not vendor:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User Not Found")

    if not Hash.verify(vendor.password, request.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Incorrect Password")

    access_token_expires = timedelta(minutes=JWT.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = JWT.create_access_token(
        data={"sub": vendor.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}






