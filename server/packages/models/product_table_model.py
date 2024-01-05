# from ..utils.utils import Base
# from sqlalchemy.orm import mapped_column,Mapped
# from sqlalchemy import ForeignKey,String
# from sqlalchemy.sql import sqltypes

# from typing import List
# from sqlalchemy.orm import mapped_column
# from sqlalchemy.orm import relationship
# # 
# class Product(Base):
#     __tablename__ = "Products"
#     id          = mapped_column(type_=sqltypes.Integer,primary_key=True,autoincrement=True)
#     name        = mapped_column(String(100),nullable=False)
#     price       = mapped_column(nullable=False,type_=sqltypes.Integer)
#     category    = mapped_column(String(100),nullable=False)
    
#     # links relations
#     inventory : Mapped[List["Inventory"]]  = relationship("Inventory",back_populates="products")
#     sales : Mapped[List["Sales"]]    = relationship("Sales",back_populates="products")

#     def __repr__(self) -> str:
#         return f"Product(id={self.id}, name={self.name}, price={self.price}, category={self.category})"

        
