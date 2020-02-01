import mysql.connector
import time
import datetime
from PyQt5.QtWidgets import QMessageBox, QWidget

class dbInterface():

	def __init__(self):
		print("hello from dbInterface constructor")
	
	
	def create_tables(self):
		try:
			self.c.execute('CREATE TABLE IF NOT EXISTS parts(w INT, x INT, y INT, z INT, name TEXT, id INT, grouping TEXT, value TEXT, dataOne TEXT, dataTwo TEXT, dataThree TEXT, mounting TEXT, package TEXT)')

		except mysql.connector.Error as e:
			print("sry m8, no axx")
		
	#add data to table.
	def data_entry(self, textEditArray):
		sqlQuery = f"SELECT MAX(id) FROM parts"
		self.c.execute(sqlQuery)
		result = self.c.fetchall()
		print(f"result: {result}")
		data = str(result).replace("[(","")
		data = data.replace(",)]","")	
		try:
			highestId = int(str(data)) 
			newId = highestId + 1	
			
		except ValueError:
			print("That's not an int!")
			newId = 0

		try:			
			sqlQuery = f"INSERT INTO parts (w, x, y, z, name, id, grouping, value, dataOne, dataTwo, dataThree, mounting, package) VALUES ('{str(textEditArray[0].text())}', '{str(textEditArray[1].text())}', '{str(textEditArray[2].text())}', '{str(textEditArray[3].text())}', '{str(textEditArray[4].text())}', '{newId}', '{str(textEditArray[6].text())}', '{str(textEditArray[7].text())}', '{str(textEditArray[8].text())}', '{str(textEditArray[9].text())}', '{str(textEditArray[10].text())}', '{str(textEditArray[11].text())}', '{str(textEditArray[12].text())}')"
			self.c.execute(sqlQuery)
			self.conn.commit()
			
		except mysql.connector.Error as e:
			print("sry m8, no axx")		
	
	def request_groups(self):
		try:
			sqlQuery = f"SELECT DISTINCT grouping FROM parts"
			self.c.execute(sqlQuery)
			resultSet = self.c.fetchall()
			return resultSet
		except mysql.connector.Error as e:
			print("error");
			
	#read data from table
	def data_request(self, textEditArray):
		try:
			sqlQuery = f"SELECT * FROM parts WHERE w LIKE '{str(textEditArray[0].text())}' AND x LIKE '{str(textEditArray[1].text())}' AND y LIKE '{str(textEditArray[2].text())}' AND z LIKE '{str(textEditArray[3].text())}' AND name LIKE '{str(textEditArray[4].text())}' AND id LIKE '{str(textEditArray[5].text())}' AND grouping LIKE '{str(textEditArray[6].text())}' AND value LIKE '{str(textEditArray[7].text())}' AND dataOne LIKE '{str(textEditArray[8].text())}' AND dataTwo LIKE '{str(textEditArray[9].text())}' AND dataThree LIKE '{str(textEditArray[10].text())}' AND mounting LIKE '{str(textEditArray[11].text())}' AND package LIKE '{str(textEditArray[12].text())}'"
			print(sqlQuery)
			self.c.execute(sqlQuery)
			resultSet = self.c.fetchall()
			return resultSet
		
		except mysql.connector.Error as e:
			print("lost connection")
			print("reconnecting...")
			self.reconnect()

	
	#remove data from table
	def delete_entry(self, textEditArray):
		try:
			sqlQuery = f"DELETE FROM parts WHERE w = '{str(textEditArray[0].text())}' AND x ='{str(textEditArray[1].text())}' AND y = '{str(textEditArray[2].text())}' AND z = '{str(textEditArray[3].text())}' AND name = '{str(textEditArray[4].text())}' AND id = '{str(textEditArray[5].text())}' AND grouping = '{str(textEditArray[6].text())}' AND value = '{str(textEditArray[7].text())}' AND dataOne = '{str(textEditArray[8].text())}' AND dataTwo = '{str(textEditArray[9].text())}' AND dataThree = '{str(textEditArray[10].text())}' AND mounting = '{str(textEditArray[11].text())}' AND package = '{str(textEditArray[12].text())}'"
			self.c.execute(sqlQuery)
			self.conn.commit()
		except mysql.connector.Error as e:
			print("sry m8, no axx")			
		
	#edit existing data row in table
	def edit_entry(self, textEditArray):
		try:
			sqlQuery = f"UPDATE parts SET w = '{str(textEditArray[0].text())}', x ='{str(textEditArray[1].text())}', y = '{str(textEditArray[2].text())}', z = '{str(textEditArray[3].text())}', name = '{str(textEditArray[4].text())}', grouping = '{str(textEditArray[6].text())}', value = '{str(textEditArray[7].text())}', dataOne = '{str(textEditArray[8].text())}', dataTwo = '{str(textEditArray[9].text())}', dataThree = '{str(textEditArray[10].text())}' , mounting = '{str(textEditArray[11].text())}', package = '{str(textEditArray[12].text())}' WHERE id = '{str(textEditArray[5].text())}'"
			self.c.execute(sqlQuery)
			self.conn.commit()
		except mysql.connector.Error as e:
			print("sry m8, no axx")		
			
	def connect(self, ip, user, password, database):
		print("Connecting to sql database...")
		self.ip = ip
		self.user = user
		self.password = password
		self.database = database
		try:
			self.conn = mysql.connector.connect(
				host=self.ip,
			        user=self.user,
				passwd=self.password,
				database=self.database
			)
			#QMessageBox.information(QWidget(), "info", "Connected!")
			self.c = self.conn.cursor()
			self.create_tables()			

		except mysql.connector.Error as e:
			QMessageBox.warning(QWidget(), "info", "MySQL connection failed...")
	
	def reconnect(self):
		self.connect(self.ip)
				
#"83.243.212.20"