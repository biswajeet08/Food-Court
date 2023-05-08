from fastapi import APIRouter, Depends, status, HTTPException
from .. import schemas, models, database, oauth2, oauth2
from sqlalchemy.orm import Session
from typing import Annotated

router = APIRouter(
    prefix="/menu",
    tags=["Menu"]
)

@router.post("/create", status_code = status.HTTP_201_CREATED, )
async def create_menu_item(request: schemas.Menu, db : Session = Depends(database.get_db),current_user= Depends(oauth2.get_current_active_vendor)):
    new_menu = models.Menu(name = request.name, description = request.desc, price = request.price, vendor_id = current_user.id)
    db.add(new_menu)
    db.commit()
    db.refresh(new_menu)

    return new_menu

@router.put("/edit/{id}", status_code = status.HTTP_201_CREATED, )
async def create_menu_item(id:int, request: schemas.Menu, db : Session = Depends(database.get_db),current_user= Depends(oauth2.get_current_active_vendor)):

    d = dict()
    if request.name != "" : d["name"] = request.name
    if request.desc != "": d["description"] = request.desc
    if request.price > 0 : d["price"] = request.price
    d["out_of_stock"] = request.out_of_stock
    if db.query(models.Menu).filter(models.Menu.id == id).first().__getattribute__("vendor_id") == current_user.id:
        menu = db.query(models.Menu).filter(models.Menu.id == id).update(d)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No Menu Found")

    db.commit()

    return menu


@router.get("", status_code=status.HTTP_200_OK)
async def show_menu(db: Session = Depends(database.get_db), current_user= Depends(oauth2.get_current_active_user)):

    menu = db.query(models.Menu).all()

    if not menu:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No Menu Found")

    return menu
