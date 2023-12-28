import numpy as np
import tensorflow as tf
import pandas as pd
from sqlalchemy.orm import DeclarativeBase

class Constants:
    supported_data = ['csv','xls']
    UPLOAD_FOLDER = 'uploads/'
    MODELS = 'datamodels/'
    DATABASE = 'database/'

class Base(DeclarativeBase):
    pass

def normalizer(dataframe):
    return (dataframe - np.min(dataframe)) / (np.max(dataframe) - np.min(dataframe) )

def get_min_max_of(dataframecolumn):
    maxdate, mindate = np.max(dataframecolumn),np.min(dataframecolumn)
    return mindate, maxdate
