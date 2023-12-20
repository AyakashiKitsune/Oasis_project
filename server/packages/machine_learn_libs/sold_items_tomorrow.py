from ..utils.utils import pd,np,tf, normalizer, get_min_max_of

def learn_sold_item(training_size,database,):
        date = 'date'
        name = 'Category Name'
        # validate date column
        database[date] = pd.to_datetime(database[date])

        # get the products in the table
        products_list = database[name].value_counts().keys().sort_values()

        # get the mindate and maxdate
        mindate, maxdate = get_min_max_of(database[date])

        # make table of [date , ... item_name_count]
        ndf = pd.DataFrame(
            columns=[date, *products_list]
        )

        # get list of dates to list
        current_day = mindate
        stop_day =  maxdate + pd.Timedelta(days=1)
        days = []
        while current_day != stop_day:
            days.append(current_day)
            current_day += pd.Timedelta(days=1)
        ndf[date] = days
        ndf.set_index(date,inplace=True)
        
        # count item sold per day
        for day in ndf.index:
            curr = database[database[date] == day]
            curr_count = curr[name].value_counts()
            if not len(curr_count.keys()) == 0:
                for key in curr_count.keys():
                    ndf.loc[day][key] = curr_count[key] 

        ndf.fillna(0, inplace=True)

        # find max and minimum value
        minsold, maxsold = get_min_max_of(ndf)
        # normalize the dataset
        normalize_db = normalizer(ndf)
        
        #shift the label db up, youll have null values after that
        label_db = normalize_db.shift(-1)
        
        # drop NA value of shifted table 
        label_db.dropna(inplace=True)
        
        # remove the very last row of the normalized table
        normalize_db = normalize_db.iloc[:-1,:]
        
        # split the test and training datasets
        target_range = int(len(normalize_db) * training_size)
        xtrain =  normalize_db[: target_range]   # 0 -> target
        xtest = normalize_db[target_range : ]      # target -> max
        
        ytrain = label_db[: target_range  ]
        ytest = label_db[target_range : ]
        # create model
        model = tf.keras.Sequential([
            tf.keras.layers.Dense(normalize_db.columns.__len__()),
            tf.keras.layers.Dense(256, activation='relu'),
            # tf.keras.layers.LeakyReLU(alpha=0.1),#512
            tf.keras.layers.Dense(normalize_db.columns.__len__(),activation='relu')
        ],)
        model.compile(
                optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
                loss=tf.keras.losses.MeanAbsoluteError(),
                metrics=['accuracy']
            )
        model.fit(xtrain.to_numpy() ,ytrain.to_numpy(),epochs=10)
        evaluate = model.evaluate(xtest,ytest)
