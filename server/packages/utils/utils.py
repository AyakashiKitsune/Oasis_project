import numpy as np
import tensorflow as tf
import pandas as pd
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import DateTime,String,Integer,Double, Boolean,Time
from datetime import datetime

class Base(DeclarativeBase):
    pass

def normalizer(dataframe):
    return (dataframe - np.min(dataframe)) / (np.max(dataframe) - np.min(dataframe) )

def get_min_max_of(dataframecolumn):
    maxdate, mindate = np.max(dataframecolumn),np.min(dataframecolumn)
    return mindate, maxdate
