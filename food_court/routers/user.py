from fastapi import APIRouter, Depends, status, HTTPException
from .. import schemas, models, database
from .. utils import Hash
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/user",
    tags=["User"]
)


@router.post("/create", response_model=schemas.ShowUser, status_code = status.HTTP_201_CREATED)
def create_user(request: schemas.User, db : Session = Depends(database.get_db)):
    hashed_passwd = Hash.bcrypt(request.password)
    try:
        new_user = models.User(name = request.name, phone = request.phone, email = request.email, password = hashed_passwd)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"User Already Exists")

    return new_user