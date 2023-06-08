from fastapi import APIRouter, Depends, status, HTTPException, Query
from .. import schemas, models, database, oauth2, oauth2
from sqlalchemy.orm import Session
from typing import Annotated
from enum import Enum
from sqlalchemy.sql import text
from typing import TypedDict




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

@router.put("/edit/{id}", status_code = status.HTTP_201_CREATED )
async def edit_menu_item(id:int, request: schemas.Menu, db : Session = Depends(database.get_db),current_user= Depends(oauth2.get_current_active_vendor)):

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

class X(str, Enum):
    # def __init__(self,db: Session = Depends(database.get_db)):
    #     self.buildings = db.execute(text("SELECT Vendors.building from Vendors")).fetchall()
    #     for building in self.buildings:
    #         self.building = building

    # IT01 = "IT01"
    # IT02 = "IT02"
    pass

d = {"a":"x", "b":"y"}

def get_buildings(db:Session = Depends(database.get_db)):
    buildings = db.execute(text("SELECT building from Vendors")).fetchall()
    buildings = [x for x in buildings]


    return buildings


@router.get("", status_code=status.HTTP_200_OK)
async def show_menu(db: Session = Depends(database.get_db), current_user= Depends(oauth2.get_current_active_user)):
    # print(q)
    # buildings = db.execute(text("SELECT building from Vendors")).fetchall()
    # buildings = [x for x in buildings]
    # print(buildings)
    menu = db.query(models.Menu).all()

    if not menu:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No Menu Found")

    return menu


if __name__ =="__main__":
    print(get_buildings())
