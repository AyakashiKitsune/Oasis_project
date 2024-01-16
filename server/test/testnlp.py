# from packages.machine_learn_libs.Unitable import auto_column_test_predict
from packages.sql.sql_controller import Database
from Server_Paths.Setup.setup_path import setup_auto_columns
# import table
# result = Database().importTableOriginalTable('Iowa_Liquor_Sales_year2012.csv')

# print()
# print(result)

# res = setup_auto_columns()
# print(res)
db={ 
    'Date': 'date',
    'Category Name' : 'name', 
    'State Bottle Retail' : 'price',
    'Category': 'category', 
    'Sale (Dollars)':'sale'}
Database().importTableOasisBase(db)
# print()