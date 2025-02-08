from fastapi import FastAPI
from fastapi import FastAPI
from auth import router as auth_router
from database import Base, engine

app = FastAPI()

# Create tables if they don't exist
Base.metadata.create_all(bind=engine)

# Include auth routes
app.include_router(auth_router, prefix="/auth")

@app.get("/")
def read_root():
    return {"message": "Football WebApp Backend is Up and Running!"}
