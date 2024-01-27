from ..utils.utils import Base
from sqlalchemy.orm import mapped_column
from sqlalchemy import String
from sqlalchemy.sql import sqltypes

from typing import List
from sqlalchemy.orm import mapped_column


class Inventory_Analysis(Base):
    __tablename__ = "Inventory_Analysis"
    id           = mapped_column(type_=sqltypes.Integer,primary_key=True,autoincrement=True)
    name         = mapped_column(String(100),nullable=False)
    january      = mapped_column(nullable=False,type_= sqltypes.Double, default=0)
    february     = mapped_column(nullable=False,type_= sqltypes.Double, default=0)
    march        = mapped_column(nullable=False,type_= sqltypes.Double, default=0)
    april        = mapped_column(nullable=False,type_= sqltypes.Double, default=0)
    may          = mapped_column(nullable=False,type_= sqltypes.Double, default=0)
    june         = mapped_column(nullable=False,type_= sqltypes.Double, default=0)
    july         = mapped_column(nullable=False,type_= sqltypes.Double, default=0)
    august       = mapped_column(nullable=False,type_= sqltypes.Double, default=0)
    september    = mapped_column(nullable=False,type_= sqltypes.Double, default=0)
    october      = mapped_column(nullable=False,type_= sqltypes.Double, default=0)
    november     = mapped_column(nullable=False,type_= sqltypes.Double, default=0)
    december     = mapped_column(nullable=False,type_= sqltypes.Double, default=0)
    min          = mapped_column(nullable=False,type_= sqltypes.Double, default=0)
    max          = mapped_column(nullable=False,type_= sqltypes.Double, default=0)
    average      = mapped_column(nullable=False,type_= sqltypes.Double, default=0)
    
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
    inventory_analysis_columns = ['name', 'january', 'february', 'march', 'april','may', 'june', 'july', 'august','september', 'october', 'november', 'december', 'min' , 'max' ,'average' ]
    
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
            'december': {self.december}
            'min' : {self.min}
            'max' : {self.max}
            'average': {self.average}
            """
        


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
            'december': self.december,
            'min' : self.min,
            'max' : self.max,
            'average': self.average
        }