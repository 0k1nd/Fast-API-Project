from sqlalchemy import Column, Integer, String, ForeignKey, Float, Boolean, DateTime, CheckConstraint
from sqlalchemy.orm import relationship
from app.database import Base

class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    date_end_of_bets = Column(DateTime, CheckConstraint('date_end_of_bets >= CURRENT_TIMESTAMP'), index=True)
    status = Column(String, default="pending")

    bets = relationship("Bet", back_populates="event", cascade="all, delete-orphan")

class Bet(Base):
    __tablename__ = "bets"

    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, ForeignKey("events.id"))
    amount = Column(Float)
    is_win = Column(Boolean, nullable=True, default=False)

    event = relationship("Event", back_populates="bets")