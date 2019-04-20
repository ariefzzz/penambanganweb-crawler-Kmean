# zainal 150411100048
import sqlite3
import re
# import sast
from sqlite3 import Error
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory, StopWordRemover, ArrayDictionary
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

# ======================================_-SQLITE-_======================================
daftarKata = set()

def koneksi(db_file):
	try:
		conn = sqlite3.connect(db_file)
		return conn
	except Error as e:
		print(e)
	return None

def prosesDataTerstruktur(conn):
	cur = conn.cursor()
	cur.execute("SELECT * FROM data")
	# cur.execute("SELECT * FROM data where url = 'https://pta.trunojoyo.ac.id/welcome/detail/140541100017'")
	rows = cur.fetchall()
	print("prosesDataTerstruktur", end="", flush=True)
	for row in rows:
		global daftarKata
		text = keDataTerstruktur(row[0])
		daftarKata = daftarKata.union(set(text))
		
		text = ' '.join(text)
		simpanDataTerstruktur(conn , text ,row[3])	
		print(". ", end="", flush=True)
	print("done")
def prosesVsm (conn):
	cur = conn.cursor()
	cur.execute("SELECT * FROM data")
	# cur.execute("SELECT * FROM data where url = 'https://pta.trunojoyo.ac.id/welcome/detail/140541100017'")
	rows = cur.fetchall()
	print("prosesVsm", end="", flush=True)
	for row in rows:
		kata = keVsm(row[4])
		# print(kata)
		# kata = ''.join(kata)
		kata = ' '.join(str(x) for x in kata)
		simpanDataVsm(conn , kata ,row[3])
		print(". ", end="", flush=True)
	print("done")
def cekKolomDataTerstruktur(conn):
	cur = conn.cursor()
	cur.execute("PRAGMA table_info(data);")
	rows = cur.fetchall()
	for row in rows:
		# print(row[1])
		if row[1] =='dataTerstruktur':
			return True
			end
	cur.execute("ALTER TABLE data ADD COLUMN dataTerstruktur TEXT;")
	return False
def cekKolomVsm(conn):
	cur = conn.cursor()
	cur.execute("PRAGMA table_info(data);")
	rows = cur.fetchall()
	for row in rows:
		# print(row[1])
		if row[1] =='vsm':
			return True
			end
	cur.execute("ALTER TABLE data ADD COLUMN vsm TEXT;")
	return False
def simpanDataTerstruktur(conn , text , url):
	task = (str(text) , str(url))
	sql = "UPDATE data SET dataTerstruktur = ? WHERE url = ?"
	cur = conn.cursor()
	cur.execute(sql,task)
	return cur.lastrowid
def simpanDataVsm(conn , text , url):
	task = (str(text) , str(url))
	
	sql = "UPDATE data SET vsm = ? WHERE url = ?"
	cur = conn.cursor()
	cur.execute(sql,task)
	return cur.lastrowid	

def simpanDaftarKata(conn):
	global daftarKata
	text = list(daftarKata)
	text = (' '.join(text))
	
	# print('daftarKata = ',text)
	# print(type(text))
	sql = "INSERT INTO daftarKata VALUES('"+text+"')"
	cur = conn.cursor()
	cur.execute(sql)
	return cur.lastrowid	

# ====================================_-PROSES VSM-_====================================


def keDataTerstruktur(text):
	text = lowerCase(text)
	text = stopword(text)
	text = stemming(text)
	text = tokenisasi(text)
	return text	
def lowerCase(text):
	text = text.lower()
	return text
def stopword(text):
	# Ambil Stopword bawaan
	stop_factory = StopWordRemoverFactory().get_stop_words()
	print(stop_factory)
	more_stopword = ['diatur', 'perjodohan']
	
	# Merge stopword
	data = stop_factory + more_stopword
	
	dictionary = ArrayDictionary(data)
	str = StopWordRemover(dictionary)
	
	hasil = str.remove(text)
	# print(hasil)
	
	return hasil
def stemming(text):
	# create stemmer
	factory = StemmerFactory()
	stemmer = factory.create_stemmer()
	
	hasil = stemmer.stem(text)
	return hasil
def tokenisasi(text):
	# text = re.sub(r'[^\w]', ' ', text)
	text = text.split()
	return text

def keVsm(text):
	global daftarKata
	text = text.split()
	tmp = []
	# print(type(text))
	# print("text nya = ",text)
	# print("daftar kata",daftarKata)
	for kata in daftarKata:
		jumlahKata = text.count(kata)
		tmp = tmp+[jumlahKata]
		# print(kata," jumlahnya = " ,jumlahKata)
	# print(". ", end="", flush=True)
	# print('panjang  list = ' ,len(tmp))
	print('panjang vsm = ', len(tmp))
	return tmp
def generate_ngrams(text, n):
	tokens = [token for token in text.split(" ") if token != ""]
	ngrams = zip(*[tokens[i:] for i in range(n)])
	return [" ".join(ngram) for ngram in ngrams]
	
# =======================================_-MAIN-_=======================================
def main():
	global daftarKata
	database = "data DUMMY.sqlite"
	# database = "data.sqlite"	
	# create a database connection
	conn = koneksi(database)
	with conn: 
		cekKolomDataTerstruktur(conn)
		cekKolomVsm(conn)
		prosesDataTerstruktur(conn)
		prosesVsm(conn)
		simpanDaftarKata(conn)
		
		# print(generate_ngrams(str(daftarKata),2))
		# print(daftarKata)
		# print(len(daftarKata))
 
if __name__ == '__main__':
	main()