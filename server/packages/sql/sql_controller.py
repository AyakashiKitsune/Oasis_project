from os import replace
from sqlalchemy import URL,create_engine, select
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import text

from ..utils.utils import pd
from ..utils.utils import Base

from ..models.product_table_model import Product
from ..models.sales_table_model import Sales
from ..models.inventory_table_model import Inventory


with open("password.txt") as f:
    password = f.readline()

class Database:
    __instance = None
    database_name = "OasisBase"
    sales_columns = ['date','name', 'price','category', 'sale' ]
    inventory_columns = ['date','name', 'price','category',  'current_stock','max_stock','min_stock' ]
    connection = False

    def __new__(cls):
        if cls.__instance == None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

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
                Product.__table__,  # parent 
                Sales.__table__,    # child
                Inventory.__table__ # child
            ]) # type: ignore
        
    #create table and imports the table
    def importTableOriginalTable(self, filename):
        df = pd.read_csv(f'uploads/{filename}',index_col=[0])
        # shortest way to get make csv to sql table
        try:
            df.to_sql(
                name= "original_table",
                con=self.engine.connect()           
            )
        except:
            pass 
        # these are the loss rows because it has null values
        null_value_table = self.get_null_rows(df)
        del(df)
        return null_value_table

    def importTableOasisBase(self,columns):
        # read the old table
        df = pd.read_sql_table(table_name="original_table",con=self.engine.connect())
        # make a diff, whats left will drop
        dropcols = set(df.columns.tolist()) - set(columns.values())
        # drop it
        df.drop(columns=[*dropcols],inplace=True)
        # rename them the rest
        df.rename(columns=columns)
        # save it
        df.to_sql(name="Sales",con=self.engine.connect(),if_exists='replace')
        del(df)


    # return a dictionary/json {column_name, table} 
    def get_null_rows(self,df):
        null_clms = []
        for col in df.columns:
            if df[df[col].isnull()].shape[0] > 0:
                null_clms.append(col)
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
        return tables

    # insert table to any table just make a class like Inventory(), Product(), Sales()
    def insert(self,obj):
        with self.session as con:
            con.add(obj)
            con.commit()
        pass

    # reads the tables in the database
    def readTable(self,tablename="",):
        with self.session as con:
            res = con.scalar(select())
            print(res)
    
    # make custom commands through text
    def custom_command(self, command):
        res = self.session.execute(text(command))
        return res
    
    def show_tables(self):
        return self.custom_command("show tables").all()
