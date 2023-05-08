from fastapi import APIRouter, Depends, status, HTTPException
from .. import schemas, models, database, utils, oauth2
from sqlalchemy.orm import Session
from sqlalchemy.sql import text
from typing import Optional

router = APIRouter(
    prefix="/vendor",
    tags=["Vendor"]
)


@router.post("/create", response_model=schemas.ShowVendor, status_code = status.HTTP_201_CREATED)
def create_vendor(request: schemas.Vendor, db : Session = Depends(database.get_db)):
    hashed_passwd = utils.pwd_cxt.hash(request.password)
    new_vendor = models.Vendor(name = request.name, building = request.building, floor = request.floor,
                               phone = request.phone, email = request.email, password = hashed_passwd, open = False)
    db.add(new_vendor)
    db.commit()
    db.refresh(new_vendor)
    return new_vendor

from enum import Enum
# class VendorIds(Enum):
#     def __init__(self, db: Session = Depends(database.get_db)):
#         db.query(models.Vendor).values

@router.get("/",response_model=list[schemas.ShowVendor], status_code=status.HTTP_200_OK)
def show_vendors(building:Optional[str] = None, floor:int | None = None, status:bool | None = True, db: Session = Depends(database.get_db)):

    if building == None and floor == None and status == None:
        # vendors = db.query(models.Vendor).all()
        vendors = db.execute(text("""SELECT * from Vendors""")).fetchall()

    else:
        if building != None:
            building_query = f"SELECT * from Vendors where Vendors.building = {building}"
        else:
            building_query = f"SELECT * from Vendors"
        if floor != None:
            floor_query = f"SELECT * from Vendors where Vendors.floor = {floor}"
        else:
            floor_query = f"SELECT * from Vendors"

        vendors = db.execute(text(f"({building_query}), ({floor_query})")).fetchall()
        # vendors = vendors.execute(text(f"{floor_query}")).fetchall()
        # vendors = db.execute(text("""SELECT * from Vendors""")).fetchall()
        # d = dict()
        # if building !=  None: d["building"] = models.Vendor.building == building
        # if floor != None: d["floor"] = models.Vendor.floor == floor
        # if status != None: d["status"] = models.Vendor.open == status
        # vendors = db.query(models.Vendor).whereclause(building exist in models.Vendor.building), d.get("floor",models.Vendor.floor),
        #                                          d.get("status",models.Vendor.open)).all()

    if not vendors:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No Vendor Found")

    return vendors

@router.get("/showall",response_model=list[schemas.ShowVendor], status_code=status.HTTP_200_OK)
def show_all_vendors(db: Session = Depends(database.get_db)):

    vendors = db.query(models.Vendor).all()

    if not vendors:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No Vendor Found")

    return vendors



@router.put("/update_status", status_code=status.HTTP_202_ACCEPTED)
def update_vendor_status(request: schemas.UpdateVendor, db: Session = Depends(database.get_db),current_user= Depends(oauth2.get_current_active_vendor)):

    vendor = db.query(models.Vendor).filter(models.Vendor.id == current_user.id).update({"open":request.status})
    # if not vendor:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No Vendor Found")
    db.commit()
    return vendor