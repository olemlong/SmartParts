import paho.mqtt.client as mqtt #import the client1
import threading

class mqttInterface():
    
    def __init__(self):
        
        print("hello from mqttInterface constructor")
            
    #TODO: 
    #Make whatch dog for each controller. this may help with the application loosing connection to the MQTT broker.
    #errorhandling for the esp8266 led controller.
    #when the controller receives coordinates that does not exist in the led array, the controller crashes. implement some error handling where the controller sends the bad coordinates
    #to the host software to be used for debuging.
        
    
    def setLedFrame(self, ledWXYZ):        #ledWXYZ = string array! 
        for x in range(0, len(ledWXYZ)):
            cabinet = int(ledWXYZ[x].split(" ",1)[0]) #put the first number in the string in the cabinet variable (W coordinate)
            xyz = ledWXYZ[x].split(" ",1)[1] #put the rest in the xyz variable.         
            self.client.publish(self.cabinetTopic[cabinet], xyz) #publish the coordinates to the correct topic.
            
        for x in range(0, len(self.cabinetTopic)):
            self.client.publish(self.cabinetTopic[x],"E") #send end of frame to all topics to clear empty arrays in all led controllers.
        
    def setOneLed(self, ledWXYZ):          #ledWXYZ = single string!
        cabinet = int(ledWXYZ.split(" ",1)[0])
        xyz = ledWXYZ.split(" ",1)[1]        
        self.client.publish(self.cabinetTopic[cabinet], xyz) #send single led xyz 
        for x in range(0, len(self.cabinetTopic)):
            self.client.publish(self.cabinetTopic[x],"E") #send end of frame to all topics to clear empty arrays in led controllers
            
    def watchdog(self):
        threading.Timer(5.0, self.watchdog).start()
        print("woff, woff...")
        for x in range(0, len(self.watchdogTopic)):
            self.client.publish(self.watchdogTopic[x],"woff, woff...")
    
    def blinkTest(self):
        for x in range(0, len(self.watchdogTopic)):
            self.client.publish(self.watchdogTopic[x],"test")
            
    #same as the setLedFrame function, but only prints the data to console.
    def checkArray(self, ledWXYZ):
        for x in range(0, len(ledWXYZ)):
            cabinet = ledWXYZ[x].split(" ",1)[0]
            xyz = ledWXYZ[x].split(" ",1)[1]
            print(f"cabinet: {self.cabinetTopic[int(cabinet)]} xyz: {xyz}")
            
    def connect(self, ip, numberOfCabinets):
        print(f"Connecting to MQTT broker IP: {ip}")
        self.client = mqtt.Client("basementOfficeComputer") #create new instance
        self.client.connect(ip) #connect to broker
     
        #make topics for publishing coordinates to the cabinets and put them into the topic array. one topic pr cabinet.
        self.cabinetTopic = []
        self.watchdogTopic = []
        for x in range(0, numberOfCabinets):
            self.cabinetTopic.append(f"parts/cabinet{x}")
            self.watchdogTopic.append(f"parts/watchdog{x}")
            print(self.cabinetTopic[x])
            print(self.watchdogTopic[x])
            
        
        self.watchdog()        