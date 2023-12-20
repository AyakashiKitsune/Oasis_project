import numpy as np
import tensorflow as tf
import pandas as pd
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.sql.sqltypes import Date,Time,String,Integer,Float,Boolean
from datetime import datetime

def splitRemoveEndline(words):
    return [line.replace('\n','').split(',') for line in words]
def prettified_word(words):
    # removes ( ) and replaced ' ' as '_'
    return [word.replace('(','').replace(')','') for word in[word.replace(' ','_') if ' ' in word else word for word in words]]

def pandasToSQLdtypes(pandasdtype):
    classifiy = {
        "object" : "VARCHAR(255)",
        "int64" : "INTEGER",
        "float64" : "DOUBLE",
        "bool" : "BOOLEAN",
        "datetime64[ns]" : "DATE",
        "timedelta[ns]" : "TIME"
    }
    return classifiy[pandasdtype]



def is_date(string):
    formats_to_check = [
        "%Y-%m-%d",  # YYYY-MM-DD
        "%Y/%m/%d",  # YYYY/MM/DD
        "%m/%d/%Y",  # MM/DD/YYYY
        "%d-%m-%Y",  # DD-MM-YYYY
        # Add more formats as needed
    ]
    for fmt in formats_to_check:
        try:
            datetime.strptime(string, fmt)
            return True
        except ValueError:
            pass
    return False


class Base(DeclarativeBase):
    pass

def normalizer(dataframe):
    return (dataframe - np.min(dataframe)) / (np.max(dataframe) - np.min(dataframe) )

def get_min_max_of(dataframecolumn):
    maxdate, mindate = np.max(dataframecolumn),np.min(dataframecolumn)
    return mindate, maxdate
