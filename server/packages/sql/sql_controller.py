from sqlalchemy import URL, column ,create_engine, select
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import text
import pandas as pd

from ..models.product_table_model import Product
from ..models.sales_table_model import Sales
from ..models.inventory_table_model import Inventory

from ..utils.utils import Base,prettified_word,is_date,splitRemoveEndline,pandasToSQLdtypes

class Database:
    database_name = "OasisBase"
    sales_columns = ['name', 'price','category', 'date', 'sale' ]
    inventory_columns = ['name', 'price','category', 'date', 'current_stock','max_stock','min_stock' ]
    connection = False

    def __init__(self,host="localhost",password="AyakashiKitsune#9262"):
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
            database= Database.database_name
        ), echo=True
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

    #csv support
    #gets the columns and its formats 
    def getColumnsfromCSVFile(self,filename): 
        df = pd.read_csv(f'uploads/{filename}',index_col=[0])
        columns = prettified_word([col.lower() for col in df.dtypes.keys()])
        df.columns = columns
        df['date'] = pd.to_datetime(df['date'])
        formats = [str(df.dtypes[i]) for i in df.dtypes.keys() ]
        del(df)
        return  columns,formats

    #create table and imports the table
    def importTable(self, filename):
        column,format = self.getColumnsfromCSVFile(filename)
        chaincols = [f"{column[i]} {pandasToSQLdtypes(format[i])}," for i in range(len(column))]
        
        createTableCommand = """create table {}.original_table (id INTEGER NOT NULL AUTO_INCREMENT,{} 
            primary key (id))""".format(Database.database_name,' '.join(chaincols))
        importTableContents = """load data local infile 'uploads/{}' into table original_table 
            fields terminated by ',' enclosed by '\"' 
            lines terminated by '\n' ignore 1 rows;""".format(filename)
        
        try:
            self.custom_command(createTableCommand)
        except: 
            print(f'table original_table already created!!!')
        try:
            self.custom_command(importTableContents)
        except Exception as error:
            print("error {}".format(error))


    # insert table to any table just make a class like Inventory(), Product(), Sales()
    def insert(self,obj):
        with self.session as con:
            con.add(obj)
            con.commit()
        pass

    def readTable(self,tablename="",):
        with self.session as con:
            res = con.scalar(select(Product))
            print(res)

    def custom_command(self, command):
        with self.session as con:
            res = con.execute(text(command))
            print(command)
