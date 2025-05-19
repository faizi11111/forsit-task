from fastapi import FastAPI
from . import models
from .database import engine
from .routers import products, inventory, sales
from .db_seed import seed_database

# Create database tables
models.Base.metadata.create_all(bind=engine)

# Seed the database
seed_database()

# Create FastAPI app
app = FastAPI(title="FastAPI CRUD API")

# Include routers
app.include_router(products.router)
app.include_router(inventory.router)
app.include_router(sales.router) 