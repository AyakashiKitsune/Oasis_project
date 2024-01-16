# import requests
# import base64
# url = 'http://127.0.0.1:5000/'
# destination = f'{url}setup'

data = {
    "message" : "do something",
    'error' : "something went wrong"
}

# response = requests.post(destination,json=data,)
# print(response)

# from sqlalchemy import text
# from packages.sql import sql_controller

# db = sql_controller.Database()
# db.importTableOriginalTable('aa.csv')
json = {
    'name' : 'val',
    'key' : 'val'
}

# print(set(json.values()))





from joblib import Parallel, delayed
from matplotlib.pylab import stem
from sqlalchemy import desc, func, insert, select,text
from packages.models.sales_table_model import Sales
from packages.sql.sql_controller import Database
import pandas as pd
import tensorflow as tf
import numpy as np
from packages.utils.utils import normalizer
from packages.machine_learn_libs.Unitable import auto_column_test_predict
import os

# column_list = Database().custom_command(command="""SELECT column_name FROM information_schema.columns WHERE table_schema = 'OasisBase' AND table_name = 'original_table';""").scalars().fetchall()
# print(column_list)
# print(auto_column_test_predict(column_list))
# print("Word".lower())

# stmt = Sales(
#     date="2022-05-04",
#     name="ice",
#     category="water",
#     price=500,
#     sale=300
# )
# # Database().insert(stmt)
folder_path = 'model'
files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
files =[i.replace("-sales.keras",'') for i in files]
products = Database().session.execute(select(Sales.name).distinct()).scalars().fetchall()

a = [str(i) for i in products]
b = [str(i) for i in files]
c = sorted(list(set(a)- set(b)))
print(a,len(a))
print(b,len(b))
print(c,len(c))

# fetch = Database().session.execute(select(Sales.date,func.sum(Sales.sale).label("sum")).where(Sales.name == products[0]).group_by(Sales.date)).fetchall()
# print(fetch[0])
# dates = Database().session.execute(select(Sales.date).distinct().order_by(Sales.date.asc())).scalars().all()

# newdates = pd.date_range(
#         pd.to_datetime(dates[0]),
#         pd.to_datetime(dates[-1]),
#         freq='D'
#     )
# print(dates)
# odf = pd.DataFrame(
#         data={'date' : newdates}
#     )
# # for product in products:
# product = products[0]
# df = pd.DataFrame(
#     columns=['date',f'sales {product}']
# )




# df['date'] = [pd.to_datetime(item[0]) for item in fetch]
# df[f'sales {product}'] =[item[1] for item in fetch]
# datediff = sorted(list(set(newdates) - set(dates))) 
# for date in datediff:
#     df.loc[len(df)] = [date, 0]
# df.sort_values('date',inplace=True)
# odf[f'{product}'] = df[f'sales {product}']

# # for product in products:
# # diff one
# ndf = odf[product].diff().shift(-1)
# avesales = ndf.mean()
# x = pd.DataFrame(
#     data = {str(i) : ndf.shift(-i) for i in range(7)} 
# )
# x.replace(0,np.nan,inplace=True)
# x.dropna(inplace=True)
# x = normalizer(x)
# average = [x.iloc[i].mean() for i in range(len(x))]
# abovemean = [1 if average[i] > avesales else 0 for i in range(len(x))]
# goingup = [1 if x.iloc[i,0] < x.iloc[i,-1] else 0 for i in range(len(x))]
# x['ans'] = x['6'].shift(-1)
# x['abovemean'] = abovemean
# x['average'] = average
# x['goingup'] = goingup
# x.dropna(inplace=True)
# # x.to_csv("lookme.csv",index=False)
# print(x)
# y =  x.pop('ans')
# x = x.to_numpy().reshape(x.shape[0],x.shape[1],1)
# model = tf.keras.models.Sequential([
#     tf.keras.layers.Input(shape=(x.shape[1],1)),#,1
#     tf.keras.layers.Dense(256,activation='relu'),
#     tf.keras.layers.Dense(256,activation='selu'),
#     tf.keras.layers.LeakyReLU(0.8),
#     tf.keras.layers.Dropout(0.3),
#     tf.keras.layers.Dense(256,activation='selu'),
#     tf.keras.layers.ELU(),
#     tf.keras.layers.Dropout(0.3),
#     tf.keras.layers.LSTM(256,dropout=0.1),
#     tf.keras.layers.Dense(1)
# ])
# model.compile(
#     optimizer=tf.optimizers.Adam(learning_rate=0.001),
#     loss=tf.keras.losses.MeanSquaredError(),
#     metrics=[
#         tf.keras.metrics.MeanSquaredError(),
#         'accuracy',
#         tf.keras.metrics.R2Score(),
#     ])
# eval = 0
# train = 30
# while True:
#     model.fit(x,y.to_numpy(),epochs=train,batch_size=16)
#     eval = model.evaluate(x,y)[-1]
#     if eval >= 0.8 and eval <= 1.0:
#         break 
#     train+=1

# model.save(f'model/{product}-sales.keras',)



# print(pd)


# for k in res.keys:
#     print(k,':',res[k]) 




# res = db.session.execute(text("""SELECT label,name FROM original_table limit 10;""")).fetchall()
# for i in res:
#     print(res[0])
# def line_analysis(lines):
#     chopped = [line.replace('\n','').split(',') for line in lines]
#     return chopped

# def prettified_word(words):
#     return [word.replace('(','').replace(')','') for word in[word.replace(' ','_') if ' ' in word else word for word in words]]

# from datetime import datetime

# def is_date(string):
#     formats_to_check = [
#         "%Y-%m-%d",  # YYYY-MM-DD
#         "%Y/%m/%d",  # YYYY/MM/DD
#         "%m/%d/%Y",  # MM/DD/YYYY
#         "%d-%m-%Y",  # DD-MM-YYYY
#         # Add more formats as needed
#     ]
#     for fmt in formats_to_check:
#         try:
#             datetime.strptime(string, fmt)
#             return True
#         except ValueError:
#             pass
#     return False
# with open('newlongIowaLiqourfixed.csv') as input_file:
#     head = [next(input_file) for _ in range(2)]
#     head = line_analysis(head)
#     columns = prettified_word(head[0])
#     data = head[1]
#     date = [is_date(i) for i in data]
#     print(date.index(True))
#     print(columns)
    


# # import subprocess
# # test = subprocess.Popen(["ls","-l"], stdout=subprocess.PIPE)
# # output = test.communicate()[0]
# # print(output)

# # from subprocess import call
# # call(["mkdir","chunked"])
# # call(["split","--verbose","-l","50000","newlongIowaLiqourfixed.csv", "chunked/"])

# # print(columns)