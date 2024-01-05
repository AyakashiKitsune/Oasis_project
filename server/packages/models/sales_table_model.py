from ..utils.utils import Base
from sqlalchemy.orm import mapped_column,Mapped
from sqlalchemy import String
from sqlalchemy.sql import sqltypes
from typing import List
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship


# remove this relationship
class Sales(Base):
    __tablename__ = "Sales"
    id          = mapped_column(type_=sqltypes.Integer,primary_key=True,autoincrement=True)
    date        = mapped_column(nullable=False,type_=sqltypes.Date)
    name        = mapped_column(String(100),nullable=False)
    category    = mapped_column(String(100),nullable=False)    
    price       = mapped_column(nullable=False,type_=sqltypes.Integer)
    sale        = mapped_column(nullable=False,type_= sqltypes.Double)
    
    products : Mapped[List["Product"]] = relationship("Product",back_populates="sales")
    
    sales_columns = ['date','name', 'price','category', 'sale' ]
    def __repr__(self) -> str:
        return f"Product(id={self.id}, product_id={self.product_id}, date={self.date}, sale={self.sale})"




        
