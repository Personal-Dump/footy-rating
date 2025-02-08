from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime
from sqlalchemy.orm import relationship
from database import Base
import datetime
from passlib.hash import bcrypt  # Import for password hashing

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)  # Store hashed password
    is_admin = Column(Integer, default=0)  # 0 = Player, 1 = Admin

    def verify_password(self, password: str) -> bool:
        return bcrypt.verify(password, self.hashed_password)

class Game(Base):
    __tablename__ = "games"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime, default=datetime.datetime.utcnow)

class Rating(Base):
    __tablename__ = "ratings"

    id = Column(Integer, primary_key=True, index=True)
    player_id = Column(String, nullable=False)  # Ensure this exists
    game_id = Column(Integer, ForeignKey("games.id"), nullable=False)
    rated_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    rated_player = Column(Integer, ForeignKey("users.id"), nullable=False)
    passing = Column(Float, nullable=False)
    defense_offense = Column(Float, nullable=False)
    stamina = Column(Float, nullable=False)
    rating = Column(Float, nullable=False)

    game = relationship("Game")
    rater = relationship("User", foreign_keys=[rated_by])
    player = relationship("User", foreign_keys=[rated_player])

class Team(Base):
    __tablename__ = "teams"

    id = Column(Integer, primary_key=True, index=True)
    game_id = Column(Integer, ForeignKey("games.id"), nullable=False)
    player_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    position = Column(String, nullable=False)  # Defender, Midfielder, etc.
    team_number = Column(Integer, nullable=False)  # 1 or 2

    game = relationship("Game")
    player = relationship("User")
