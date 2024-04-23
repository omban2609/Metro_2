# Metro_2

Algorithm of code or model:
1.	There are only 4 stations on the track: Chattrapati Shivaji Terminal (CST), Grand Central Terminal (GCT), Dadar Railway Station (DRT), Terminus.
2.	People enter the metro boggie, there is ultrasonic sensor place on left inside of the door which monitors distance whenever a person passes by 3cm distance from it to inside of metro and it counts it as person, else no person.
3.	There is a flame sensor in boggie, if there is fire, the buzzer buzzes loudly high for 10 seconds and low for 10 seconds this buzzing happens 3 times.
4.	The four stations are in forward direction.
5.	There are no sensors used to see current status of the boggie on which station it is…so we monitor it by manually starting and stopping the boggie for 30 seconds at each station, this station number is calculated value we also store this with us.The boggie drives for 5 seconds only to get to next station the demo rail is short and motors used are 12V 10Rpm.
6.	The value of people count, boggie fire alert status is sent live to web page  created using flask on raspberry pi 4.
7.	After the 4th last station the motors go in full reverse mode for 20 seconds and stop again at 1st station. Motors are controlled using L298N  motor driver with raspberry pi
8.	At each station when boggie stops the buzzer beeps for twice 2 seconds loudly indicating public to climb into boggie and beeps once for 3 times for 1 seconds to alert that its leaving for next station.
9.	The live station name status is displayed on website in green color and which we will be next station is also mentioned at website in red color.
10.	After going station 1 to 4 the boggie comes in reverse to station one and the program continues in loop endlessly

Update my code accordingly…to algo do not do any mistake and also explain me the code.
I am giving you the flask python main code so handle it carefully.
Components:
1.	Raspberry Pi 3
2.	Any temperature sensor
3.	Ultrasonic sensor
4.	DC motors-4
5.	L298N motor driver or relays to drive it
6.	Webserver or Blynk
