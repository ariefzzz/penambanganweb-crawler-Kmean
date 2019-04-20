# Import pandas
import pandas as pd
import numpy as np
import math
import itertools as it

master = pd.ExcelFile("b.xls")
data = master.parse("RapidMiner Data")
out=list([])

dist = {}
def maximum():
    data.fillna(data.max())
    print(data.mean())
    print(data)
def minimum():
    data.fillna(data.min())
    print(data.mean())
    print(data)
def average(column):
    data.fillna(data.mean())
    print(data.mean())
    print(data)
#print(data.iloc[0,1].isnull())