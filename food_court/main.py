from fastapi import FastAPI
from .import models
from .database import engine, SessionLocal
from .routers import menu, user, vendor, authentication, orders

app = FastAPI()

models.Base.metadata.create_all(engine)

app.include_router(authentication.router)
app.include_router(menu.router)
app.include_router(user.router)
app.include_router(vendor.router)
app.include_router(orders.router)



