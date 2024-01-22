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

def denormalizer(normalized_dataframe, original_dataframe):
    
    min_val = np.min(original_dataframe)
    max_val = np.max(original_dataframe)
    return normalized_dataframe * (max_val - min_val) + min_val

def get_min_max_of(dataframecolumn):
    maxdate, mindate = np.max(dataframecolumn),np.min(dataframecolumn)
    return mindate, maxdate
