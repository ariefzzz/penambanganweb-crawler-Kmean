# zainal 150411100048

import sqlite3
import re
import math
import random as rn
# import sast
from sqlite3 import Error
centerCluster=[]
centerDataCluster=[]
clushter=[]
vsm , url = "",""
# ======================================_-SQLITE-_======================================
def koneksi(db_file):
	try:
		conn = sqlite3.connect(db_file)
		return conn
	except Error as e:
		print(e)
	return None
def getVsm(conn):
	aList = list()
	aUrl = list()
	tmp = ""
	cur = conn.cursor()
	cur.execute("SELECT url,vsm FROM data")
	rows = cur.fetchall()
	for row in rows:
		# print("row[0]",row[0])
		# print("row[1]",row[1])
		# print(type(row[1]))
		# print(row[1])
		tmp = row[1].split()
		# print('panjang vsm = ' , len(tmp))
		aList.append(tmp)
		aUrl.append(row[0])
	return aUrl , aList

def getCenterData(conn,rowNumber):
	tmp = ""
	# task = list([rowNumber])
	sql = str("SELECT vsm from data LIMIT 1 OFFSET "+str(rowNumber))
	
	cur = conn.cursor()
	cur.execute(sql)
	rows = cur.fetchall()

	tmp = " ".join(list(rows[0]))
	
	return tmp.split()
def cekKolomCluster(conn):
	cur = conn.cursor()
	cur.execute("PRAGMA table_info(data);")
	rows = cur.fetchall()
	for row in rows:
		# print(row[1])
		if row[1] =='cluster':
			return True
			end
	cur.execute("ALTER TABLE data ADD COLUMN cluster TEXT;")
	return False	
def simpanCluster(conn,clus,url):
	task = (str(text) , str(url))
	
	sql = "UPDATE data SET vsm = ? WHERE url = ?"
	cur = conn.cursor()
	cur.execute(sql,task)
	return cur.lastrowid

def manhattanDistance(dokumen1,dokumen2):
	dokumen1 = list(map(int, dokumen1))
	dokumen2 = list(map(int, dokumen2))
	jarak = 0
	for x,y in zip(dokumen1,dokumen2):
		tmp = abs(x-y)
		jarak = jarak +tmp
	return jarak
def EuclideanDistance(dokumen1,dokumen2):
	dokumen1 = list(map(int, dokumen1))
	dokumen2 = list(map(int, dokumen2))
	jarak = 0
	for x,y in zip(dokumen1,dokumen2):
		tmp = abs(x-y)**2
		jarak = jarak +tmp
	return math.sqrt(jarak)
def random(Jclushter,panjangData):
	# return rn.sample(range(0,len(data)),k)
	return rn.sample(range(0,panjangData),Jclushter)
def kmean(conn,k,url,vsm):
	global centerCluster , clushter , centerDataCluster
	newClushter=[]
	iterasi = 0
	centerCluster = list(random(k,len(vsm)))
	print("centerCluster = ",centerCluster)
	for x in range(0,k):  
		centerDataCluster.append(getCenterData(conn,centerCluster[x]))
	while(True): 
		iterasi+=1
		# jdata = 0
		for dataKe in vsm:
			#tmp jarak menampung jarak data ke masing masing center
			tmpJarak=[]
			# jdata+=1
			# print("dataKe",jdata)
			jcenter=0
			for centerKe in centerDataCluster:
				# jcenter+=1
				# print("centerKe",jcenter)
				tmpJarak.append(manhattanDistance(dataKe,centerKe))
			#kemudian diambil jarak terendah
			cls = tmpJarak.index(min(tmpJarak))
			newClushter.append(cls+1)
		# print("iterasi ke ",iterasi)
		# print("newClushter = ",newClushter)
		# print("clushter = ",clushter)
		if(newClushter == clushter):
			break
		else:
			clushter = newClushter
			newClushter = []
			print("-----------------------------------------------------------------")
			# print(len(centerCluster) , len(clushter) , len(centerDataCluster))
			# print(centerCluster)
			print(clushter)
			# print(centerDataCluster)
			NewCenter = []
			for x in range(1,k+1):			
				tmp = [0] * len(vsm[0])
				jumlah = 0
				for y in clushter:
					if(y==x):
						# print(y)
						# print(len(tmp),len(vsm[0]))
						tmp = aPlusB(tmp,vsm[y]) 
						jumlah+=1
				NewCenter.append(mean(tmp,jumlah))
			centerDataCluster = NewCenter
			# print('panjang centerDataCluster = ',len(centerDataCluster))
	return clushter
# def strToint(vsm):
def aPlusB(a,b):
	# print('len a = ',len(a),'len b = ', len(b))
	for x in range(len(a)):
		
		a[x] = a[x]+int(b[x])
	return a
def mean(data,jumlahData):
	# print(len(data), jumlahData)
	if(jumlahData != 0):
		for x in range(len(data)):
			# print('panjangData = ',len(data) , ' index ke  = ' , x)
			data[x] = data[x] / jumlahData
			
	return data
	
def main(): 
	global url ,vsm
	database = "data DUMMY.sqlite"
	# database = "data.sqlite"	
	# create a database connection
	conn = koneksi(database)
	with conn: 
		# url , vsm = getVsm(conn)
		# print(url)
		# print(vsm)
		
		url , vsm = getVsm(conn)
		jumlahCluster = 5
		a = kmean(conn,jumlahCluster,url,vsm)
		# print(a)
if __name__ == '__main__':
	main()
