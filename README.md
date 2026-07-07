CEF488 GROUP 8  Networked Real-Time Temperature Monitoring System

A physical temperature sensor that sends live readings over a network, triggers alerts when things get too hot, and logs everything to a file. Built from scratch — hardware wiring to networked Python scripts running across multiple machines.

What It Does
An LM35 sensor on an Arduino UNO reads room temperature every 2 seconds
A sensor client (Python) reads the Arduino over USB serial and sends the data over UDP to a server
The server tracks a running average, logs every reading to a CSV file, and fires an alert if temperature exceeds 38°C
An alert client on a separate machine receives and displays the alert in real time


Hardware Used
ComponentPurposeArduino UNOMicrocontrollerLM35 SensorReads analog temperatureBreadboard + jumper wiresCircuit connections

Wiring: LM35 VCC → 5V, OUTPUT → A0, GND → GND


Software Stack

ComponentLanguageRuns OnArduino firmwareC++ (Arduino IDE)Arduino UNOsensor_client.pyPython 3Sensor PC (Ubuntu VM)server.pyPython 3Server PC (Ubuntu VM)alert_client.pyPython 3Any PC on the network


**How to Run It**

1. Flash the Arduino
Upload arduino_temp.ino via Arduino IDE. Set board to Arduino UNO, port to your serial port.

2. Set up the sensor client
bashsudo apt install python3-serial -y
cd project
nano sensor_client.py  # set SERVER_IP to your server's IP
python3 sensor_client.py

3. Start the server
bashsudo ufw allow 5005/udp
sudo ufw allow 5006/udp
nano server.py  # set ALERT_CLIENT_IP to your alert client's IP
python3 server.py

4. Start the alert client
bashpython3 alert_client.py


Run order: server first → alert client → sensor client. Always.


Network Setup
All machines must be on the same local network
VMs must use Bridged Adapter (not NAT) in VirtualBox
Sensor data: UDP port 5005
Alerts: UDP port 5006

What We Learned the Hard Way
LM35 is analog it belongs on A0. DHT11 is digital it does not. We found this out the wrong way.
VirtualBox USB passthrough requires the Extension Pack installed separately. Without it, the Arduino is invisible to the VM.
Never run VirtualBox and VMware on the same host and expect them to talk over UDP. They won't.
Ubuntu 24.04 blocks pip install system-wide. Use sudo apt install python3-serial instead.
A floating analog pin gives you readings between 13°C and 124°C. Always check your physical connections before blaming the code.
