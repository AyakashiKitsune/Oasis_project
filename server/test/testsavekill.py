from sqlalchemy import select
from packages.sql.sql_controller import Database
from packages.machine_learn_libs.savekillanalysis import analyze_savekill
from packages.models.sales_table_model import Sales

products = Database().session.execute(select(Sales.name).distinct()).scalars().fetchall()
res = analyze_savekill(product=products[0])
print(res)