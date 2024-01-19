from os import replace
from sqlalchemy import URL, between,create_engine, func, select
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import text
import numpy as np
from ..utils.utils import pd
from ..utils.utils import Base

from ..models.sales_table_model import Sales
from ..models.inventory_table_model import Inventory
from ..models.savekill_table_model import SaveKill


with open("password.txt") as f:
    password = f.readline()

class Database:
    __instance = None
    database_name = "OasisBase"
    SALES__ = "Sales"
    INVENTORY__ = "Inventory"
    # sales_columns = ['date','name', 'price','category', 'sale' ]
    # inventory_columns = ['date','name', 'price','category',  'current_stock','max_stock','min_stock' ]
    # connection = False
    
    # sigleton class 
    def __new__(cls):
        if cls.__instance == None:
            cls.__instance = super().__new__(cls)
        return cls.__instance
    
    # constructor
    def __init__(self,host="localhost",password=password):
        # make a link url to backend
        url = URL.create(
            drivername="mysql+pymysql",
            username= "root",
            password=password,
            host=host,
            port=3306,
        )
        # create a link to back nd
        self.engine = create_engine(url,echo=True,)
        # execute a sql code, to make OasisBase database
        try:
            with self.engine.connect() as session:
                session.execute(text("create database {}".format(Database.database_name)))
        except:
            print(f"{Database.database_name} is already created!!!")
        # remodify the engine with new link for safe connection
        self.engine = create_engine(
            URL.create(
            drivername="mysql+pymysql",
            username= "root",
            password= "AyakashiKitsune#9262",
            host="localhost",
            port=3306,
            database= Database.database_name,
            query={"local_infile":'1'}
        ), echo=True,connect_args={"local_infile":'1'}
        ) 
        Session = sessionmaker(self.engine,)
        self.session = Session()
        Base.metadata.create_all(
            self.engine,
            tables=[
                Sales.__table__,    # child
                Inventory.__table__, # child
                SaveKill.__table__ # child
            ]) # type: ignore
        
    # import the original table to original_table table as old table
    def importTableOriginalTable(self, filename):
        df = pd.read_csv(f'uploads/{filename}',index_col=[0])
        df.reset_index(drop=True,inplace=True)
        # these are the loss rows because it has null values
        null_value_table = self.get_null_rows(df)
        df.dropna(inplace=True,)
        # shortest way to get make csv to sql table
        
        df.to_sql(
            name="original_table",
            con=self.engine.connect(),
            if_exists='replace',
            chunksize=int(len(df)/10),
            index=False    
        )
        del(df)
        return null_value_table

    # original_table to sales table
    def importTableOasisBaseSales(self,columns):
        # ['date','name', 'price','category', 'sale' ]
        # read the old table
        df = pd.read_sql_table(table_name="original_table",con=self.engine.connect())
        # make a diff, whats left will drop
        dropcols = set(df.columns.tolist()) - set(list(columns.keys()))
        # drop it
        df.drop(columns=[*dropcols],inplace=True)
        # rename them the rest
        df.rename(columns=columns,inplace=True)
        df['date']  = pd.to_datetime(df["date"])
        # save it
        df.reset_index(drop=True,inplace=True)
        df.to_sql(name="Sales",con=self.engine.connect(),if_exists='replace',index_label='id',chunksize=int(len(df)/10))
        self.makesavekilltable()
        del(df)

    # return a dictionary/json {column_name, table} 
    def get_null_rows(self,df):
        null_clms = []
        loss = 0
        for col in df.columns:
            check = df[df[col].isnull()].shape[0]
            if check > 0:
                null_clms.append(col)
                if loss <= check:
                    loss = check
        tables = []
        for col in null_clms:
            tables.append(
                {
                    "column_name" : col,
                    "table" : df[df[col].isnull()].to_dict()
                }
            )
        print(tables)
        del(null_clms)
        return {'tables' : tables, 'loss' : loss }

    # insert table to any table just make a class like Inventory(), Sales()
    def insert(self,obj):
        with self.session as con:
            con.add(obj)
            con.commit()
        pass
    
    # read sales on specific date 
    def readSalesOnDate(self, YYYYMMDD,wholesale=False):
        if wholesale:
            request = self.session.execute(
                select(Sales.date, func.sum(Sales.sale).label('sum'))
                .where(Sales.date == YYYYMMDD)
            ).fetchone()
            return request
        else: 
            request = self.session.execute(
                select(Sales)
                .where(Sales.date == YYYYMMDD)
            ).scalars()
            return [i.to_dict() for i in request]

    # read sales on between dates
    def readSalesBetweendates(self,fromdate,todate,wholesale=False):
        if wholesale:
            request = self.session.execute(
                select(Sales.date, func.sum(Sales.sale))
                .where(between(Sales.date,fromdate,todate))
                .group_by(Sales.date)
            ).fetchall()
            return request #tuple ()
        else:
            request = self.session.execute(
                select(Sales)
                .where(between(Sales.date,fromdate,todate))
            ).scalars()
            return [i.to_dict() for i in request] #list

    def distinctValuesColumn(self):
        return self.session.execute(
            select(Sales.name).distinct()
        ).scalars().all()

    # make custom commands through text
    def custom_command(self, command):
        res = self.session.execute(text(command))
        return res
    
    def makesavekilltable(self):
        products = self.session.execute(select(Sales.name).distinct()).scalars().fetchall()
        for product in products:
            fetch =  self.session.execute(select(func.month(Sales.date), func.count(Sales.sale)).where(Sales.name == product).group_by(func.month(Sales.date))).fetchall()
            arg = np.median([i[1] for i in fetch])
            months = {
                f'{SaveKill.month_dict[i[0]]}': 1 if i[1] >= arg else 0  for i in fetch
            }
            json = {
                'name' : product,
                **months
            }
            self.insert(SaveKill(**json))

