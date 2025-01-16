from sqlalchemy import Column, Integer, Float, Boolean
from bet_maker.database import Base


class Bet(Base):
    __tablename__ = "bets"

    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, index=True)
    amount = Column(Float)
    is_win = Column(Boolean, nullable=True, default=False)