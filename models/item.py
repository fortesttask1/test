from sqlalchemy import Column, ForeignKey, Integer, String, Text, Numeric
from sqlalchemy.orm import relationship
from db.database import Base

class Item(Base):
    __tablename__ = 'items'

    id = Column(Integer, primary_key=True)
    name = Column(String, index=True, unique=True)
    description = Column(Text)
    category_id = Column(Integer, ForeignKey('categories.id'))
    quantity = Column(Integer)
    price = Column(Numeric(10, 2))

    category = relationship("Category", back_populates="items")
    owner_id = Column(Integer, ForeignKey('users.id'))
    owner = relationship("User", back_populates="items")

