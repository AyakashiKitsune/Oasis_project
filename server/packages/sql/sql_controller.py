from datetime import datetime, timedelta
from flask import jsonify
from sqlalchemy import URL, asc, between,create_engine, desc, func, select
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import text
import numpy as np
from sympy import ordered
from ..utils.utils import get_min_max_of, pd
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
    isrun = False
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
        if not Database.isrun:
            print("database initialization")
            # make a link url to backend
            url = URL.create(
                drivername="mysql+pymysql",
                username= "root",
                password=password,
                host=host,
                port=3306,
            )
            # create a link to back nd
            self.engine = create_engine(url,echo=True)
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

        if not Database.isrun:
            print("database tables initialization")
            Base.metadata.create_all(
            self.engine,
            tables=[
                Sales.__table__,    # child
                Inventory.__table__, # child
                SaveKill.__table__ # child
            ]) # type: ignore
            Database.isrun = True

        
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
        df['category'] = df['category'].astype(str)
        mindate, maxdate = get_min_max_of(df['date'])
        alldates = pd.date_range(mindate,maxdate)
        diffdate = set(alldates)-set(df['date'])

        # save it
        df.reset_index(drop=True,inplace=True)
        print(df.dtypes)
        df.to_sql(name="Sales",con=self.engine.connect(),if_exists='replace',index_label='id',chunksize=int(len(df)/10))
        for i in diffdate:
            self.insert(Sales(
                date = f'{i.year}-{i.month}-{i.day}'
            ))
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
                .order_by(asc(Sales.date))
            ).fetchone()
            return jsonify({"date": request[0],"sum" : request[1]})
        else: 
            request = self.session.execute(
                select(Sales)
                .where(Sales.date == YYYYMMDD)
                .order_by(asc(Sales.date))
            ).scalars()
            return [i.to_dict() for i in request]

    def readSalesRecent(self,wholesale = False):
        recentdate = self.session.execute(
            select(func.max(Sales.date))
        ).scalar()
        if wholesale:
            request = self.session.execute(
                select(Sales.date, func.sum(Sales.sale).label('sum'))
                .where(Sales.date == recentdate)
                .order_by(asc(Sales.date))
            ).fetchone()
            return jsonify([{"date": request[0],"sum" : request[1]}])
        else: 
            request = self.session.execute(
                select(Sales)
                .where(Sales.date == recentdate)
                .order_by(asc(Sales.date))

            ).scalars()
            return [i.to_dict() for i in request]

    # read sales on between dates
    def readSalesBetweendates(self,fromdate,todate,wholesale=False):
        if wholesale:
            request = self.session.execute(
                select(Sales.date, func.sum(Sales.sale))
                .where(between(Sales.date,fromdate,todate))
                .group_by(Sales.date)
                .order_by(asc(Sales.date))
            ).fetchall()
            return [{"date": i[0],"sum" : i[1]}for i in request] #tuple ()
        else:
            request = self.session.execute(
                select(Sales)
                .where(between(Sales.date,fromdate,todate))
                .order_by(asc(Sales.date))
            ).scalars()
            return [i.to_dict() for i in request] #list
        
    def overview_query(self,):
        currentDate = datetime.now()
        recentdate = self.session.execute(
            select(func.max(Sales.date))
        ).scalar()
        fromdate = recentdate - timedelta(days=14)
        
        fourteen_days_wholesales    = self.readSalesBetweendates(fromdate=fromdate,todate=recentdate,wholesale=True)
        seven_days_wholesales       = fourteen_days_wholesales[7:]
        total_sales_year            = self.session.execute(
                                            select(func.sum(Sales.sale)).where(func.year(Sales.date) == currentDate.date)
                                    ).scalar() 
        total_sold_year             = self.session.execute(
                                        select(func.count(Sales.sale)).where(func.year(Sales.date) == currentDate.date)
                                    ).scalar() 
        sold_count_product          = self.session.execute(
                                        select(Sales.name, func.count(Sales.name).label("sold"))
                                        # .where(func.year(Sales.date) == currentDate)
                                        .group_by(Sales.name)
                                        .order_by(desc("sold"))
                                    ).fetchall()
        
        sold_count_product          = [
            {"name" : i[0], "sold" : i[1] } for i in sold_count_product
        ]
        if total_sales_year == None :
            total_sales_year = 0
        return fourteen_days_wholesales,seven_days_wholesales,sold_count_product,total_sales_year,total_sold_year

    def recent_date(self):
        res = self.session.execute(
            select(func.max(Sales.date))
        ).scalar()
        res1 = self.session.execute(
            select(func.min(Sales.date))
        ).scalar()
        return res,res1

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
        products.remove("None")
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

    def makeInventoryAnalysis(self):
        products = Database().session.execute(
            select(Sales.name).distinct()).scalars().fetchall()
        products.remove("None")
        odf = pd.DataFrame(
                    columns = ["name", *[i for i in range(1,13)],"min",'max', "average"]
                )

        for i in products:
            res = Database().session.execute(
                    select(func.month(Sales.date), func.count(Sales.name).label('count'))
                    .where(Sales.name == i)
                    .group_by(func.month(Sales.date))).fetchall()

            df = pd.DataFrame(
                    data = {
                        "month" : [i[0] for i in res],
                        "sold" : [i[1] for i in res],
                    }
                )
            
            if(len(df) != 12):
                old = set(df['month'].tolist())
                total = set([i for i in range(1,13)])
                new = total - old

                for i in list(new):
                    df.loc[len(df)] = [i,0]
                df.sort_values('month', inplace=True)
                df.reset_index(drop=True,inplace=True)

            min = df['sold'].min()
            max = df['sold'].max()
            average = np.round((max+min) / 2)

            l = [str(i),*df['sold'].tolist(), min, max, average]

            odf.loc[len(odf)] = l
            
        odf.to_sql(
            name = "Invetory_analysis",
            con=self.engine.connect(),
            if_exists='replace',
            index=False
        )

