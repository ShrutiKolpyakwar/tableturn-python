from sqlalchemy import Column, ForeignKey, Integer, String

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