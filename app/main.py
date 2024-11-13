from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database.database import Base, engine
from app.routers.health import router as health_router
from app.routers.sales import router as sales_router
from app.routers.expenses import router as expenses_router

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
