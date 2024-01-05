from ..utils.utils import Base
from sqlalchemy.orm import mapped_column,Mapped
from sqlalchemy import String
from sqlalchemy.sql import sqltypes

from typing import List
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship


class Inventory(Base):
    __tablename__ = "Inventory"
    id          = mapped_column(type_=sqltypes.Integer,primary_key=True,autoincrement=True)
    name        = mapped_column(String(100),nullable=False)
    price       = mapped_column(nullable=False,type_=sqltypes.Integer)
    category    = mapped_column(String(100),nullable=False)
    current_stock        = mapped_column(nullable=False,type_= sqltypes.Integer)
    maximum_stock        = mapped_column(nullable=False,type_= sqltypes.Integer)
    minimum_stock        = mapped_column(nullable=False,type_= sqltypes.Integer)
    
    # products : Mapped[List["Product"]] = relationship("Product",back_populates="inventory")
    
    inventory_columns = ['name', 'price','category', 'date', 'current_stock','max_stock','min_stock' ]
    # def __init__(self,product_id,current_stock,maximum_stock, minimum_stock):
    #     self.product_id = product_id
    #     self.current_stock = current_stock
    #     self.maximum_stock = maximum_stock
    #     self.minimum_stock = minimum_stock
    def __repr__(self) -> str:
        return f"Product(id={self.id}, product_id={self.product_id}, current_stock={self.current_stock}, maximum_stock={self.maximum_stock}, minimum_stock={self.minimum_stock})"


        
