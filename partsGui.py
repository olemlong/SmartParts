import sys
import dbInterface
import mqttInterface
from PyQt5 import  QtCore
from PyQt5.QtWidgets import QApplication, QDialog, QMessageBox, QTableWidgetItem, QTreeWidgetItem
from PyQt5.uic import loadUi


class MainGui(QDialog):
	def __init__(self):
		#config. to be implemented in GUI
		ip = "192.168.1.32"
		user = "olemlong"
		password = "123456123"
		database = "testdb"
		numberOfCabinets = 9
		self.useMqtt = 1
		
		#load GUI for userinterface file made in QT designer.
		super(MainGui, self).__init__()
		loadUi('parts.ui',self) 
		self.setWindowTitle('parts Database')
		self.groupingArray =  []
		
		#put all lineeditobject in array to make it easy for later use.
		self.lineEditArray = [ self.lineEdit_22,#W
		                       self.lineEdit,#x
		                       self.lineEdit_2,#y
		                       self.lineEdit_3,#z
		                       self.lineEdit_4,#name
		                       self.lineEdit_5,#id
		                       self.lineEdit_6,#grouping
		                       self.lineEdit_7,#value
		                       self.lineEdit_8,#data1
		                       self.lineEdit_9,#data2
		                       self.lineEdit_10,#data3
		                       self.lineEdit_23,#mounting
		                       self.lineEdit_24,#package
		                       ]
		
		self.lineEditArray_2 = [ self.lineEdit_21,#W
		                         self.lineEdit_11,#x
		                         self.lineEdit_12,#y
		                         self.lineEdit_13,#z
		                         self.lineEdit_14,#name
		                         self.lineEdit_15,#id
		                         self.lineEdit_16,#grouping
		                         self.lineEdit_17, #value
		                         self.lineEdit_18,#data1
		                         self.lineEdit_19,#data2
		                         self.lineEdit_20,#data3
		                         self.lineEdit_25,#mounting
		                         self.lineEdit_26,#package
		                         ]
		
		
		self.labelArray = [ self.label_22,
		                    self.label,
		                    self.label_2,
		                    self.label_3,
		                    self.label_4,
		                    self.label_5,
		                    self.label_6,
		                    self.label_7,
		                    self.label_8,
		                    self.label_9,
		                    self.label_10,
		                    self.label_24,
		                    self.label_25,
		                    ]
		
		self.labelArray_2 = [ self.label_21,
			              self.label_13,
		                      self.label_12,
		                      self.label_15,
		                      self.label_17,
		                      self.label_14,
		                      self.label_16,	          
		                      self.label_11,
		                      self.label_19,
		                      self.label_20,
		                      self.label_18,
		                      self.label_26,
		                      self.label_27,
		                      ]	
		self.tw = self.treeWidget
		self.tw_2 = self.treeWidget_2
		self.tw.setHeaderLabels(["Groups"])
		self.tw_2.setHeaderLabels(["Groups"])
		#array for the lineEdit arrays
		self.lineEditArrayArray = [ self.lineEditArray,  #search/add tab lineEdits
		                            self.lineEditArray_2,] #delete/edit tab lineEdits
		
		
		self.tableWidgetArray = [ self.tableWidget, #search/add tab table
		                          self.tableWidget_2] #delete/edit tab table		
		
		self.labelArrayArray = [ self.labelArray, #labels on the search/add tab
		                         self.labelArray_2,] #labels on the delete/edit tab		
		
		#align all the lineEdits in the GUI
		#the first for loop iterates over number of groups that holds lineedits (only two, search/add and edit/remove)
		#the second for loop iterates over the number of lineedits. (w,x,y,z and so on)
		#example: lineEditArrayArray[0][2] would refere to the Z lineEdit in the tab search/add
		#example: lineEditArrayArray[1][7] would refere to the Value lineEdit in the tab edit/remove.
		for x in range (0, len(self.lineEditArrayArray)):			
			for y in range(0, len(self.lineEditArray)):
			
				if(y == 0):
					
					self.lineEditArrayArray[x][y].move(45,100) #move the first lineedit in both tabs to 45x and 100y.
				else:
					self.lineEditArrayArray[x][y].move(self.lineEditArrayArray[x][y-1].x() + self.lineEditArrayArray[x][y-1].width() +9, self.lineEditArrayArray[x][y-1].y()) #moving the rest of the array in relation to the first.										
				if(y > 4):
					self.lineEditArrayArray[x][y].resize(91,self.lineEditArrayArray[x][y].height()) #set W X Y Z column to 91px whide and use the same hight as set in the QT designer.
				if(y == 4):
					self.lineEditArrayArray[x][y].resize(110,self.lineEditArrayArray[x][y].height()) #set name column 110px whide and use the same hight as set in the QT designer.						
				if(y == 10):
					self.lineEditArrayArray[x][y].resize(250,self.lineEditArrayArray[x][y].height()) #set data3 column 250px whide and use the same hight as set in the QT designer.

		#align all the labels to the lineEdits			
		for x in range (0, len(self.labelArrayArray)):
			for y in range(0, len(self.labelArray)):
				self.labelArrayArray[x][y].resize(self.lineEditArrayArray[x][y].width(), self.labelArrayArray[x][y].height()) #resize labels to the same x sizes as the lineEdits, but no change to y size.
				self.labelArrayArray[x][y].setAlignment(QtCore.Qt.AlignCenter) #align text to center of label object
				self.labelArrayArray[x][y].move(self.lineEditArrayArray[x][y].x(), self.lineEditArrayArray[x][y].y() -20) #move all the labels to the same X and Y as their respective lineEdits.
				
		for x in range(0, len(self.tableWidgetArray)):
			self.tableWidgetArray[x].setColumnCount(13) #setting total columns in all tablewidgets
			self.tableWidgetArray[x].setRowCount(150) #setting total rows in all tablewidgets
			
			for y in range(0, self.tableWidgetArray[0].columnCount()):
				self.tableWidgetArray[x].setColumnWidth(y,self.lineEditArray[y].width()+9) #align columns to the lineEdits.

		
		self.attachEvents()#attach events to functions

		self.show()#show gui
		
		self.dbObject = dbInterface.dbInterface() #make MySql database object.
		self.dbObject.connect(ip, user, password, database) #connect to the MySql server
		
		if(self.useMqtt != 0):
			self.ledFrame = mqttInterface.mqttInterface() #make mqtt server object
			self.ledFrame.connect(ip, numberOfCabinets) #connect to mqtt server
		
		#self.updateTableWidgetOne()
		#self.updateTableWidgetTwo()
	
	#When table 1 is clicked, select entire row.
	def QTableWidget_clicked(self, clickedIndex):
		self.tableWidget.selectRow(clickedIndex.row())
		for x in range(0, len(self.lineEditArray)):
			self.lineEditArray[x].setText(self.tableWidget.item(clickedIndex.row(), x).text()) #put all data in the row back in the lineEdits for editing.
			
		if(self.useMqtt != 0):
			self.ledFrame.setOneLed(f"{self.lineEditArray[0].text()} {self.lineEditArray[1].text()} {self.lineEditArray[2].text()} {self.lineEditArray[3].text()}") #light up one led with data from W X Y Z
		
	
	#When table 2 is clicked, select entire row.
	def QTableWidget_2_clicked(self, clickedIndex):
		self.tableWidget_2.selectRow(clickedIndex.row())
		for x in range(0, len(self.lineEditArray_2)):
			self.lineEditArray_2[x].setText(self.tableWidget_2.item(clickedIndex.row(),x).text()) #put all data in the row back in the lineEdits for editing.
			
		if(self.useMqtt != 0):
			self.ledFrame.setOneLed(f"{self.lineEditArray_2[0].text()} {self.lineEditArray_2[1].text()} {self.lineEditArray_2[2].text()} {self.lineEditArray_2[3].text()}")#light up one led with data from W X Y Z
		
	
	
	#Search button, uses all texts in lineedit object to search sqlite DB	
	def button_clicked(self):
		print("button1 click...")
		

		leds = []
		for x in range(0, len(self.lineEditArray)):
			if not self.lineEditArray[x].text(): #if the search parameter is null
				self.lineEditArray[x].setText("%")  #set it to be % ( sql wildcard) 
		self.tableWidget.setRowCount(0) #clear table widget.
		self.tableWidget.setColumnCount(len(self.lineEditArray_2)) #set number of columns with the number of lineedits 
		
		for rowcount, result in enumerate(self.dbObject.data_request(self.lineEditArray)):
			print(f"{rowcount} , {result}")
			#print(rowcount)
			self.tableWidget.insertRow(rowcount)
			temp =""
			for column_number, data in enumerate(result):			
				self.tableWidget.setItem(rowcount, column_number, QTableWidgetItem(str(data)))

				if(column_number in range(0,4)):	
					#print(column_number)
					temp += f"{str(data)} " #add column data to data string. this happens for the first 4 data columns ( W X Y Z ) data.

				if(column_number == 4):
					#print(temp)
					leds.append(temp)
		self.groupingArray = []
		self.sortingArray = []
		self.tw.clear() #clear treewidget
		for result in self.dbObject.request_groups():
			strResult = str(result)
			strResult = strResult[2:-3]
			self.sortingArray.append(strResult) #sort all group 
			
		self.sortedArray = sorted(self.sortingArray)
		for x in range(0, len(self.sortingArray)):
		                QTreeWidgetItem(self.tw,[self.sortedArray[x]]) #display sorted groups in tree
			
			
		if(self.useMqtt != 0):#when both of the for loops are completed, the leds array is full off coordinates for leds that will be on if we use MQTT.
			self.ledFrame.setLedFrame(leds)
			#self.ledFrame.checkArray(leds)
					
				
	#Clear button. clear all lineedit objects
	def button_2_clicked(self):		
		for x in range(0, len(self.lineEditArray)):
			self.lineEditArray[x].setText("")
		print("button2 click...")
			
			
	#Add new data endtry to DB		
	def button_3_clicked(self):
		self.dbObject.data_entry(self.lineEditArray)
	
	
	#delete/edit tab add button
	def button_4_clicked(self):
		self.dbObject.data_entry(self.lineEditArray_2)

			
	#Edit/delete tab clear button		
	def button_5_clicked(self):
		for x in range(0, len(self.lineEditArray_2)):
			self.lineEditArray_2[x].setText("")
			
	#Edit/delete tab search button
	def button_6_clicked(self):
		leds = []
		for x in range(0, len(self.lineEditArray_2)):
			if not self.lineEditArray_2[x].text(): #if the search parameter is null
				self.lineEditArray_2[x].setText("%")  #set it to be % ( sqlite wildcard) 
				
		self.tableWidget_2.setRowCount(0) #We start off at 0 rows
		self.tableWidget_2.setColumnCount(len(self.lineEditArray_2)) #set number of columns to the number of lineEdit objects.		
		
		for rowcount, result in enumerate(self.dbObject.data_request(self.lineEditArray_2)): # for each row
			self.tableWidget_2.insertRow(rowcount) #insert rownumber
			temp =""
			for column_number, data in enumerate(result): #for each column we have data		
				self.tableWidget_2.setItem(rowcount, column_number, QTableWidgetItem(str(data))) #insert data into column		
				
				if(column_number in range(0,4)):	
					#print(column_number)
					temp += f"{str(data)} " #add column data to data string. this happens for the first 4 data columns ( W X Y Z ) data.
					
				if(column_number == 4): #if for loop is at 4 indicating that there is no more coordinate data and adding the W X Y Z stored in temp to the leds array.
					#print(temp)
					leds.append(temp)
			
		if(self.useMqtt != 0):#when both of the for loops are completed, the leds array is full off coordinates for leds that will be on if we use MQTT.
			self.ledFrame.setLedFrame(leds) 
			#self.ledFrame.checkArray(leds)		
			
		self.groupingArray = []
		self.sortingArray = []
		self.tw_2.clear() #clear treewidget
		for result in self.dbObject.request_groups():
			strResult = str(result)
			strResult = strResult[2:-3]
			self.sortingArray.append(strResult) #sort all group 

		self.sortedArray = sorted(self.sortingArray)
		for x in range(0, len(self.sortingArray)):
			QTreeWidgetItem(self.tw_2,[self.sortedArray[x]]) #display sorted groups in tree

				
	#Delete button event		
	def button_7_clicked(self):
		print("Delete button")
		self.dbObject.delete_entry(self.lineEditArray_2)
		self.updateTableWidgetTwo()
	
	
	#Edit button event
	def button_8_clicked(self):
		print("Edit button")
		self.dbObject.edit_entry(self.lineEditArray_2)
		self.updateTableWidgetTwo()
		

	def updateTableWidgetOne(self):
		self.button_2_clicked()
		self.button_clicked()
		
	def updateTableWidgetTwo(self):
		self.button_5_clicked()
		self.button_6_clicked()	
	
	def treeWidget_clicked(self, it, col):
		self.lineEditArray[6].setText(it.text(col))
		self.button_clicked()
		
	def treeWidget_2_clicked(self, it, col):
		self.lineEditArray_2[6].setText(it.text(col))
		self.button_6_clicked()		
	
	def attachEvents(self):
		self.pushButton.clicked.connect(self.button_clicked) #search button event attach
		self.pushButton_2.clicked.connect(self.button_2_clicked) #search/add clear button event attach
		self.pushButton_3.clicked.connect(self.button_3_clicked) #search/add tab add button event attach	
		self.pushButton_4.clicked.connect(self.button_4_clicked) #delete/edit tab add button event attach
		self.pushButton_5.clicked.connect(self.button_5_clicked) #delete/edit tab clear button event attach
		self.pushButton_6.clicked.connect(self.button_6_clicked) #Delete/edit search button event attach
		self.pushButton_7.clicked.connect(self.button_7_clicked) #delete button event attach		
		self.pushButton_8.clicked.connect(self.button_8_clicked) #delete/edit tab Edit button event attach			
		self.tableWidget.itemClicked.connect(self.QTableWidget_clicked) #Search/add table clicked event attach
		self.tableWidget_2.itemClicked.connect(self.QTableWidget_2_clicked)#Delete/edit table clicked event attach		
		self.treeWidget.itemClicked.connect(self.treeWidget_clicked) #treewidget clicked.
		self.treeWidget_2.itemClicked.connect(self.treeWidget_2_clicked) #treewidget clicked.
		
def run():
	app = QApplication(sys.argv)
	GUI = MainGui()

	sys.exit(app.exec())
	
run()