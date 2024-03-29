from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from db.database import Base


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, index=True)

    items = relationship("Item", back_populates="category")