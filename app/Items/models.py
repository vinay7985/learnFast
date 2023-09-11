from sqlalchemy import Boolean, Column, ForeignKey, Integer, String,DateTime
from database import Base



class Items(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)
    tax = Column(String)