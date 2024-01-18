from packages.sql.sql_controller import Database

one = Database().readSalesOnDate('2012-01-03') #working
print('one',one)
one = Database().readSalesOnDate('2012-01-03',wholesale=True)#working
print('one',one)

multiple = Database().readSalesBetweendates('2012-01-03','2012-01-04')#working
for i in multiple:
    print('multi',i)
multiple = Database().readSalesBetweendates('2012-01-03','2012-01-04',wholesale=True)#working
for i in multiple:
    print('multi',i)