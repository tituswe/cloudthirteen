from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database.database import Base, engine
from app.routers.health import router as health_router
from app.routers.sales import router as sales_router
from app.routers.expenses import router as expenses_router
from app.routers.inventory import router as inventory_router
from app.routers.balance_sheet import router as balance_sheet_router
from app.routers.customer_segmentation import router as customer_segmentation_router
from app.routers.sales_and_inventory import router as sales_and_inventory_router

app = FastAPI()

# Create the database tables
Base.metadata.create_all(bind=engine)

# Set up CORS
origins = [
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(health_router)
app.include_router(sales_router)
app.include_router(expenses_router)
app.include_router(inventory_router)
app.include_router(balance_sheet_router)
app.include_router(customer_segmentation_router)
app.include_router(sales_and_inventory_router)
