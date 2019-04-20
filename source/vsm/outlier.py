# Import pandas
import pandas as pd
import numpy as np
import math
import itertools as it

master = pd.ExcelFile("a.xls")
data = master.parse("RapidMiner Data")
#writer = pd.ExcelWriter('example.xlsx', engine='xlsxwriter')
out=list([])
#x = list([1,2,3,4,5,6,7,8,9,0])
r = 0
phi = 0
dist = {}
def addColumnOutlier(out):
    if 'Outliers' in data.columns:
        print("kolom sudah ada ")
    else:
        data.insert(loc=6, column='Outliers', value=out)
#    df.insert(loc=idx, column='A', value=new_col)
def creatDistance(a,b):
    jarak = abs(data.iloc[a,0]-data.iloc[b,0])+abs(data.iloc[a,1]-data.iloc[b,1])+abs(data.iloc[a,2]-data.iloc[b,3])+abs(data.iloc[a,3]-data.iloc[b,3])
    return jarak
def kombinasi():
    global data
    bantu = list(range(0,len(data)))
    for subset in it.combinations(bantu,2):
        tmp = "-"+str(subset[0])+"-,-"+str(subset[1])+"-"
        dist[tmp] = creatDistance(subset[0],subset[1])
def cek(x): 
    count = 0
    for key , value in dist.items(): 
        if("-"+str(x)+"-" in key.lower()):
            if(value <= r):
                count+=1
    compareWithPhi = float(count/len(data))
    if(compareWithPhi<=phi):
        return "True"
    else:
        return "False"
#            print(key," = ", value)
def manhattan():
    global out
    kombinasi()
    for x in range(0,len(data)):
        out.append(cek(x))
    addColumnOutlier(out)
    print(data)
    save = input("save file ? [y/n] \n")
    if(save == 'y'):
        writer = pd.ExcelWriter('lof - py.xlsx')
        data.to_excel(writer,'python')
        writer.save()
def menu():
    global r , phi
    r = int(input("masukkan R = "))
    phi = float(input("masukkan phi = "))
    manhattan()


menu()
