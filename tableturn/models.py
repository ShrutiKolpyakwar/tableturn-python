
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime

from tableturn.db import Base


class DiningTable(Base):
    __tablename__ = "tables"

    no = Column(String(10), primary_key=True, index=True)
    seats = Column(Integer, nullable=False)
    section = Column(String(20), nullable=False)


class Seating(Base):
    __tablename__ = "seatings"

    id = Column(String(36), primary_key=True)
    table_no = Column(
        String(10),
        ForeignKey("tables.no"),
        nullable=False,
        index=True,
    )
    party_size = Column(Integer, nullable=False)
    status = Column(String(20), nullable=False, default="seated")


class Party(Base):
    __tablename__ = "parties"

    id = Column(String(36), primary_key=True)
    name = Column(String(60), nullable=False)
    covers = Column(Integer, nullable=False)
    phone = Column(String(16), nullable=False)
    state = Column(String(20), nullable=False, default="waiting")
    position = Column(Integer, nullable=False)
    joined_at = Column(DateTime, nullable=False)