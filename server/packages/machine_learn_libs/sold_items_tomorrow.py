from joblib import Parallel, delayed
from sqlalchemy import func, select

from ..models.sales_table_model import Sales
from ..utils.utils import pd,np,tf, normalizer, get_min_max_of
from ..sql.sql_controller import Database
import os

def learn_sales_item(replace_models=False):
    # list product name unique/set/distinct
    products = Database().session.execute(select(Sales.name).distinct()).scalars().fetchall()
    products = [str(item) for item in products]
    if not replace_models:
        folder_path = '../models'
        files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
        files =[str(i.replace("-sales.keras",'')) for i in files]
        products = list(set(products) - set(files))

    # list of date in sales table
    dates = Database().session.execute(select(Sales.date).distinct().order_by(Sales.date.asc())).scalars().all()
    # generate date from minimum to max date
    newdates = pd.date_range(
            pd.to_datetime(dates[0]),
            pd.to_datetime(dates[-1]),
            freq='D'
        )
    # original table where to store the sales and dates
    odf = pd.DataFrame(
            data={'date' : newdates}
        )
    

    # for product in products:
    #     # make a table
    #     df = pd.DataFrame(
    #         columns=['date',f'sales {product}']
    #     )
    #     # fetch the date,sum in that date
    #     fetch = Database().session.execute(select(Sales.date,func.sum(Sales.sale).label("sum")).where(Sales.name == product).group_by(Sales.date)).fetchall()
    #     # column date insert
    #     df['date'] = [pd.to_datetime(item[0]) for item in fetch]
    #     # column sales insert
    #     df[f'sales {product}'] =[item[1] for item in fetch]
    #     # find the difference of fulldate and existed dates = missings dates
    #     datediff = sorted(list(set(newdates) - set(dates))) 
    #     # insert rows
    #     for date in datediff:
    #         df.loc[len(df)] = [date, 0]
    #     # sort by dates
    #     df.sort_values('date',inplace=True)
    #     # insert sales of x product in original table
    #     odf[f'{product}'] = df[f'sales {product}']
    
    results = Parallel(n_jobs=-1)(
        delayed(preprocess_product_tablesales)(product, newdates, dates) for product in products
    )
    for i, product in enumerate(products):
        odf[f'{product}'] = results[i][f'sales {product}']
        
    for product in products:
        # diff one
        ndf = odf[f'{product}'].diff().shift(-1)
        avesales = ndf.mean()
        x = pd.DataFrame(
            data = {str(i) : ndf.shift(-i) for i in range(7)} 
        )
        x.replace(0,np.nan,inplace=True)
        x.dropna(inplace=True)
        x = normalizer(x)
        average = [x.iloc[i].mean() for i in range(len(x))]
        abovemean = [1 if average[i] > avesales else 0 for i in range(len(x))]
        goingup = [1 if x.iloc[i,0] < x.iloc[i,-1] else 0 for i in range(len(x))]
        x['ans'] = x['6'].shift(-1)
        x['abovemean'] = abovemean
        x['average'] = average
        x['goingup'] = goingup
        x.dropna(inplace=True)
        y =  x.pop('ans')
        x = x.to_numpy().reshape(x.shape[0],x.shape[1],1)
        model = tf.keras.models.Sequential([
            tf.keras.layers.Input(shape=(x.shape[1],1)),#,1
            tf.keras.layers.Dense(256,activation='relu'),
            tf.keras.layers.Dense(256,activation='selu'),
            tf.keras.layers.LeakyReLU(0.8),
            tf.keras.layers.Dropout(0.3),
            tf.keras.layers.Dense(256,activation='selu'),
            tf.keras.layers.ELU(),
            tf.keras.layers.Dropout(0.3),
            tf.keras.layers.LSTM(256,dropout=0.1),
            tf.keras.layers.Dense(1)
        ])
        model.compile(
            optimizer=tf.optimizers.Adam(learning_rate=0.001),
            loss=tf.keras.losses.MeanSquaredError(),
            metrics=[
                tf.keras.metrics.MeanSquaredError(),
                'accuracy',
                tf.keras.metrics.R2Score(),
            ])
        eval = 0
        train = 30
        while True:
            model.fit(x,y.to_numpy(),epochs=train,batch_size=16)
            eval = model.evaluate(x,y)[-1]
            if eval >= 0.8 and eval <= 1.0:
                break
            if train > 100:
                break
            train = train + 1

        model.save(f'model/{product}-sales.keras',)
        print(f'model/{product}-sales.keras')


def preprocess_product_tablesales(product, newdates, dates,):
    df = pd.DataFrame(columns=['date', f'sales {product}'])

    fetch = Database().session.execute(select(Sales.date, func.sum(Sales.sale).label("sum")).where(Sales.name == product).group_by(Sales.date)).fetchall()

    df['date'] = [pd.to_datetime(item[0]) for item in fetch]
    df[f'sales {product}'] = [item[1] for item in fetch]

    datediff = sorted(list(set(newdates) - set(dates)))

    for date in datediff:
        df.loc[len(df)] = [date, 0]

    df.sort_values('date', inplace=True)
    return df

def learn_wholesales():
    # list of date in sales table
    dates = Database().session.execute(select(Sales.date).distinct().order_by(Sales.date.asc())).scalars().all()
    # generate date from minimum to max date
    newdates = pd.date_range(
            pd.to_datetime(dates[0]),
            pd.to_datetime(dates[-1]),
            freq='D'
        )
    # original table where to store the sales and dates
    odf = pd.DataFrame(
            columns=['date','sales']
        )
    fetch = Database().session.execute(select(Sales.date,func.sum(Sales.sale).label("sum")).group_by(Sales.date)).fetchall()
    odf['date'] = [pd.to_datetime(item[0]) for item in fetch]
    odf['sales'] = [item[1] for item in fetch]
    datediff = sorted(list(set(newdates) - set(odf['date'].tolist())))
    for date in datediff:
        odf.loc[len(odf)] = [date, 0]
    
    odf['sales'] = normalizer(odf['sales'])
    ndf = odf['sales'].diff().shift(-1)
    avesales = ndf.mean()
    x = pd.DataFrame(
        data = {str(i) : ndf.shift(-i) for i in range(7)} 
    )
    x.dropna(inplace=True)
    x = normalizer(x)
    average = [x.iloc[i].mean() for i in range(len(x))]
    abovemean = [1 if average[i] > avesales else 0 for i in range(len(x))]
    goingup = [1 if x.iloc[i,0] < x.iloc[i,-1] else 0 for i in range(len(x))]
    x['ans'] = x['6'].shift(-1)
    x['abovemean'] = abovemean
    x['average'] = average
    x['goingup'] = goingup
    x.dropna(inplace=True)
    y =  x.pop('ans')
    x = x.to_numpy().reshape(x.shape[0],x.shape[1],1)

    model = tf.keras.models.Sequential([
            tf.keras.layers.Input(shape=(x.shape[1],1)),#,1
            tf.keras.layers.Dense(256,activation='relu'),
            tf.keras.layers.Dense(256,activation='selu'),
            tf.keras.layers.LeakyReLU(0.8),
            tf.keras.layers.Dropout(0.3),
            tf.keras.layers.Dense(256,activation='selu'),
            tf.keras.layers.ELU(),
            tf.keras.layers.Dropout(0.3),
            tf.keras.layers.LSTM(256,dropout=0.1),
            tf.keras.layers.Dense(1)
        ])
    model.compile(
        optimizer=tf.optimizers.Adam(learning_rate=0.001),
        loss=tf.keras.losses.MeanSquaredError(),
        metrics=[
            tf.keras.metrics.MeanSquaredError(),
            'accuracy',
            tf.keras.metrics.R2Score(),
        ])
    eval = 0
    train = 30
    while True:
        model.fit(x,y.to_numpy(),epochs=train,batch_size=16)
        eval = model.evaluate(x,y)[-1]
        if eval >= 0.8 and eval <= 1.0:
            break 
        train = train + 1
    
    model.save(f'model/wholesales.keras',)
