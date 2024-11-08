from fastapi import FastAPI

from app.database.database import Base, engine

from app.routers.item import router as item_router

app = FastAPI()

# Create the database tables
Base.metadata.create_all(bind=engine)

# Routers
app.include_router(item_router)
