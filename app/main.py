from fastapi import FastAPI

from app.database.database import Base, engine

from app.routers.health import router as health_router
from app.routers.sales import router as sales_router

app = FastAPI()

# Create the database tables
Base.metadata.create_all(bind=engine)

# Routers
app.include_router(health_router)
app.include_router(sales_router)
