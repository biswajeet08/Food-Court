from fastapi import APIRouter, Depends, status, HTTPException
from .. import schemas, models, database, oauth2, oauth2
from sqlalchemy.orm import Session
from typing import Annotated, TypedDict
from datetime import datetime


router = APIRouter(
    prefix="/order",
    tags=["Order"]
)

@router.post("/create",
             status_code = status.HTTP_201_CREATED,
             description= "Provide menu item IDs  and quantity in integer." )
async def create_order(request:schemas.Order, db : Session = Depends(database.get_db)):
    order = request.dict()
    menu_summary = {}
    menu_summary["grand total"] = 0
    for item_id, quantity in order["items"].items():
        menu_item = db.query(models.Menu).filter_by(id = item_id).first()
        vendor = db.query(models.Vendor).filter_by(id = menu_item.vendor_id).first()
        if menu_item is not None and menu_item.out_of_stock is False:
            d = {}
            d["quantity"] = quantity
            d["price"] = menu_item.price
            d["amount"] = quantity * menu_item.price
            if vendor.name not in menu_summary.keys():
                menu_summary[vendor.name] = {}
                menu_summary[vendor.name]["building"] = vendor.building
                menu_summary[vendor.name]["floor"] = vendor.floor
                menu_summary[vendor.name][menu_item.name] = d
                menu_summary[vendor.name]["total amount"] = d["amount"]
                pin = datetime.now().timestamp()
                menu_summary[vendor.name]["pin"] = str(pin)[-6:]
            else:
                menu_summary[vendor.name][menu_item.name] = d
                menu_summary[vendor.name]["total amount"] = menu_summary[vendor.name]["total amount"] + d["amount"]

            menu_summary["grand total"] = menu_summary["grand total"]+d["amount"]


        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No Menu Found for {item_id}")

    return menu_summary