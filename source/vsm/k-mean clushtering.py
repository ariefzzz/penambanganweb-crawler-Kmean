# Import pandas
import pandas as pd
import numpy as np
import math
import itertools as it
import random as rn
from statistics import mean

master = pd.ExcelFile("a.xls")
data = master.parse("RapidMiner Data")
#writer = pd.ExcelWriter('example.xlsx', engine='xlsxwriter')
out=list([])
center=[]
clushter=[]
dist = {}
a=[1,2,3,4]
c=[1,2,3,4]

def addColumnOutlier(out):
    if 'Outliers' in data.columns:
        print("kolom sudah ada ")
    else:
        data.insert(loc=6, column='Clushter', value=out)
#    df.insert(loc=idx, column='A', value=new_col)
def euclideanDist(a,b):
    jarak = float((abs(a[0]-b[0])**2+abs(a[1]-b[1])**2+abs(a[2]-b[2])**2+abs(a[3]-b[3])**2)**0.5)
    return jarak
def manhattanDist(a,b):
    jarak = abs(a[0]-b[0])+abs(a[1]-b[1])+abs(a[2]-b[2])+abs(a[3]-b[3])
    return jarak
def getData(x):
    return [[data.iloc[x,0]],[data.iloc[x,1]],[data.iloc[x,2]],[data.iloc[x,3]]]
def random(k):
    return rn.sample(range(0,len(data)),k)
def getMean():
    
    return x
def kmean(k):
    global center , clushter
    newClushter=[]
    iterasi = 0
    center = list(random(k))
    for x in range(0,k):  
#        clushter.append([center[x]])
        center[x] = getData(center[x])
    while(True): 
        iterasi+=1
        for x in range(0,len(data)):    
            tmpJarak=[]
            for y in range(0,k):
                tmpJarak.append(euclideanDist(center[y],list(data.iloc[x,:])))
            cls = tmpJarak.index(min(tmpJarak))
            newClushter.append(cls+1)
        if(newClushter == clushter):
            break
        else:
            clushter = newClushter
            newClushter = []
        
#        
    addColumnOutlier(clushter)
    print(data)
    print("jumlah iterasi = " ,iterasi)
    save = input("save file ? [y/n] \n")
    if(save == 'y'):
        writer = pd.ExcelWriter('kmean - py.xlsx')
        data.to_excel(writer,'python')
        writer.save()
def menu():
    k = float(input("masukkan jumlah clushter = "))
    kmean(k)

menu()
a = []
b = [[1,2],[3],[4,5]]
c = [[3],[1,2],[4,5]]
