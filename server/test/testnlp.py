# from packages.machine_learn_libs.Unitable import auto_column_test_predict
from packages.sql.sql_controller import Database
from Server_Paths.Setup.setup_path import setup_auto_columns

# import the database
# result = Database().importTableOriginalTable('Iowa_Liquor_Sales_year2012.csv') # not compatible with the dataset
# print(result)

# auto // the nlp  
# res = setup_auto_columns()
# print(res)


db={ 
    'Date': 'date',
    'Category Name' : 'name', 
    'State Bottle Retail' : 'price',
    'Category': 'category', 
    'Sale (Dollars)':'sale'}

# # manual base import
Database().importTableOasisBaseSales(db)
