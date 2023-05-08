from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from .database import Base

class Vendor(Base):

    __tablename__ = "Vendors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    building = Column(String)
    floor = Column(Integer)
    phone = Column(String, unique=True)
    email = Column(String, unique=True)
    password = Column(String)
    open = Column(Boolean)

    items = relationship("Menu", back_populates="vendor")

class Menu(Base):

    __tablename__ = "menu"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)
    price = Column(Integer)
    out_of_stock = Column(Boolean, default= False)
    vendor_id = Column(Integer, ForeignKey("Vendors.id"))

    vendor = relationship("Vendor", back_populates= "items")


class User(Base):

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    phone = Column(String, unique=True)
    email = Column(String, unique=True)
    password = Column(String)




