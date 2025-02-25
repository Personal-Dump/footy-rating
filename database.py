from sqlalchemy import create_engine, Column, Integer, Float, LargeBinary, String
from sqlalchemy.orm import sessionmaker, declarative_base
from database import Base

DATABASE_URL = "sqlite:///./football.db"  # Change to PostgreSQL later

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Include User model
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)  # Store hashed password

# Rating Model
class Rating(Base):
    __tablename__ = "ratings"

    id = Column(Integer, primary_key=True, index=True)
    player_id = Column(String, unique=True, index=True)
    rating = Column(Float, nullable=False)

    encrypted_rating = Column(LargeBinary, nullable=False)
    encrypted_aes_key = Column(LargeBinary, nullable=False)

# Create DB Tables
Base.metadata.create_all(bind=engine)

# Dependency for database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
