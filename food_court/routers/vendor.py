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
def show_vendors(open:bool|None = None, building:Optional[str] = None, floor:int | None = None, db: Session = Depends(database.get_db)):

    if building == None and floor == None and open == None:
        # vendors = db.query(models.Vendor).all()
        vendors = db.execute(text("""SELECT * from Vendors""")).fetchall()

    else:
        # query_list = []
        # d = {"open": open, "building": building, "floor": floor}
        # for check, value in d.items():
        #     if value != None:
        #         query = f" {check}  = '{value}'"
        #         query_list.append(query)
        #
        query_list = []
        if building != None:
            building_query = f" Vendors.building  = '{building}' "
            query_list.append(building_query)

        if floor != None:
            floor_query = f" Vendors.floor = {floor} "
            query_list.append(floor_query)

        if open != None:
            open_query = f" Vendors.open = {open} "
            query_list.append(open_query)

        query = " and ". join(query_list)
        query = f"SELECT * from Vendors where {query}"
        vendors = db.execute(text(f"{query}")).fetchall()

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