# SmartParts
Smart storage system for electronic components.

Ever since I started working with electronics, the pile of parts has been growing to the point where it took forever to find the correct part. The first step in solving this madnes was to get a cabinet and labelmaker. 
With the cabinet stacked with components, and each drawer labeled, I saw the problem as history.

As a few months passed by, the cabinet was full and i needed another cabinet to store more parts. Bought another cabinet, labeled each drawer with the components that was inside. This repeated itself until i had six cabinets all labeled. 

Now instead of searching in a desk drawer filled with all kinds of parst, i searched 6 cabinets for the correct labeled drawer. This became a pain. So i started thinking of a system that could indicate the correct drawer based on a search. This is when the SmartParts system was born.

![](images/Cabinets.png)

The hardware requirements:  
-Raspberry Pi (for running the MySql and MQTT server)  
-Esp8266 controller (one controller for each cabinet)  
-WS2812b LED (one for each drawer)  
-LED PCB (one for each row in the cabinet)  
  
The LED PCB is optional. You could always buy a roll of the WS2812b leds on ebay and cut it to length. Just a warning, this is what i did in the first cabinet and why i designed the PCB, it is alot of work, the double sided tape falls off and it is a bitch to cut and solder each led.

Cabinet layout
![](images/CabinetLayout.png)

How it all works  
  
  All the parts are stored in a MySql database. Each part has coordinates coresponding to the placement in the cabinets, like an address. This address is composed of four values (W,X,Y,Z).  
W -The cabinet coordinate. 1 = cabinet 1, 2 = cabinet 2, and so on.  
X -The column coordinate. 1 = column 1, 2 = column 2, and so on. I only have 5 columns in my cabinets.  
Y -The row coordinate. 1 = row 1, 2 = row 2, and so on.   
Z -The compartment coordinate. Each drawer can be devided into 4 compartments.   


The Flow of data.  

![](images/FlowChart.png)
