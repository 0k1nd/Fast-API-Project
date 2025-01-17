from sqlalchemy import Column, Integer, DECIMAL, String, DateTime, CheckConstraint
from line_provider.database import Base

class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    cof = Column(DECIMAL(10, 2), CheckConstraint('cof >= 0'),index=True)
    date_end_of_bets = Column(DateTime, CheckConstraint('date_end_of_bets >= CURRENT_TIMESTAMP'), index=True)
    status = Column(String, default="pending")
