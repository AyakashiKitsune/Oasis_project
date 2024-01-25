from datetime import datetime, timedelta
from re import S
import numpy

from sqlalchemy import asc, between, desc, func, select
from packages.sql.sql_controller import Database
from packages.models.sales_table_model import Sales
import pandas as pd
import tensorflow as tf
import numpy as np
from packages.utils.utils import normalizer, denormalizer
duration = 7

wholesales = Database().session.execute(
    select(Sales.date,func.sum(Sales.sale))
    .group_by(Sales.date)
).all()

df = pd.DataFrame(
    columns = ['dates','sales']
)
olddates = [pd.to_datetime(i[0]) for i in wholesales]
df['dates'] = olddates
df['sales'] = [i[1] for i in wholesales]


newdates = pd.date_range(np.min(olddates), np.max(olddates))
diffdate = set(newdates) - set(olddates)
for i in list(diffdate):
    df.loc[len(df)] = [i, 0]
df.sort_values('dates',inplace=True)
df.reset_index(drop=True,inplace=True)

odf = df.copy(True)
df['sales'] = normalizer(df['sales'])
averagesales =  df['sales'].mean()
df['sales'] = df['sales'].diff()

df = df.tail(14)
logger = []
logger.append(df['sales'][-7:].to_numpy())
results = []
for row in range(duration):
    takelastseven = logger[row]
    x = [*takelastseven,
        1 if np.mean(takelastseven)  > averagesales else 0,
        np.mean(takelastseven),
        1 if takelastseven[0] < takelastseven[-1] else 0]

    model = tf.keras.models.load_model('model/wholesales.keras')
    pred = model.predict(np.reshape(x,(1,10,1)))
    result = pred[0][0]
    results.append(result)
    logger.append([*takelastseven[1:],result])
# for row in logger:
    # print('-',["{:>10}".format(denormalizer(i,odf['sales'])) for i in row])


