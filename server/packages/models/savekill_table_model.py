from ..utils.utils import Base
from sqlalchemy.orm import mapped_column,Mapped
from sqlalchemy import String
from sqlalchemy.sql import sqltypes

from typing import List
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship


class SaveKill(Base):
    __tablename__ = "Save Kill"
    id           = mapped_column(type_=sqltypes.Integer,primary_key=True,autoincrement=True)
    name         = mapped_column(String(100),nullable=False)
    january      = mapped_column(nullable=False,type_= sqltypes.Integer, default=0)
    february     = mapped_column(nullable=False,type_= sqltypes.Integer, default=0)
    march        = mapped_column(nullable=False,type_= sqltypes.Integer, default=0)
    april        = mapped_column(nullable=False,type_= sqltypes.Integer, default=0)
    may          = mapped_column(nullable=False,type_= sqltypes.Integer, default=0)
    june         = mapped_column(nullable=False,type_= sqltypes.Integer, default=0)
    july         = mapped_column(nullable=False,type_= sqltypes.Integer, default=0)
    august       = mapped_column(nullable=False,type_= sqltypes.Integer, default=0)
    september    = mapped_column(nullable=False,type_= sqltypes.Integer, default=0)
    october      = mapped_column(nullable=False,type_= sqltypes.Integer, default=0)
    november     = mapped_column(nullable=False,type_= sqltypes.Integer, default=0)
    december     = mapped_column(nullable=False,type_= sqltypes.Integer, default=0)
    
    # products : Mapped[List["Product"]] = relationship("Product",back_populates="inventory")
    month_dict = {
        1: 'january',
        2: 'february',
        3: 'march',
        4: 'april',
        5: 'may',
        6: 'june',
        7: 'july',
        8: 'august',
        9: 'september',
        10: 'october',
        11: 'november',
        12: 'december'
    }
    savekill_columns = ['name', 'january', 'february', 'march', 'april','may', 'june', 'july', 'august','september', 'october', 'november', 'december' ]
    # def __init__(self,product_id,current_stock,maximum_stock, minimum_stock):
    #     self.product_id = product_id
    #     self.current_stock = current_stock
    #     self.maximum_stock = maximum_stock
    #     self.minimum_stock = minimum_stock
    def __repr__(self) -> str:
        return f"""\n
            'id' : {self.id},
            'name': {self.name}, 
            'january': {self.january}, 
            'february': {self.february}, 
            'march': {self.march}, 
            'april': {self.april}, 
            'may': {self.may}, 
            'june': {self.june}, 
            'july': {self.july}, 
            'august': {self.august}, 
            'september': {self.september}, 
            'october': {self.october}, 
            'november': {self.november}, 
            'december': {self.december}"""
        


    def to_dict(self) -> dict:
        return {
            'id' : self.id,
            'name': self.name, 
            'january': self.january, 
            'february': self.february, 
            'march': self.march, 
            'april': self.april, 
            'may': self.may, 
            'june': self.june, 
            'july': self.july, 
            'august': self.august, 
            'september': self.september, 
            'october': self.october, 
            'november': self.november, 
            'december': self.december  
        }