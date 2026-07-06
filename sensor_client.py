import socket
import serial
import struct
import time

# --- CONFIGURATION ---
SERIAL_PORT = "/dev/ttyUSB0"  # or ttyACM0"   # Change to /dev/ttyACM0 if ttyUSB0 doesn't work
BAUD_RATE = 9600
SERVER_IP = "192.168.8.105"      # Replace with your server PC's IP address
SERVER_PORT = 5005
ZONE_ID = 1                     # Zone 1
SEND_INTERVAL = 2               # seconds
# ---------------------

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
arduino = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=3)

print(f"Sensor client started → sending to {SERVER_IP}:{SERVER_PORT}")
time.sleep(2)  # Wait for Arduino to initialize

while True:
    try:
        line = arduino.readline().decode("utf-8").strip()
        if not line:
            continue

        temp = float(line)

        # Binary format: zone_id (1 byte unsigned) + temperature (4 bytes float)
        packet = struct.pack("!Bf", ZONE_ID, temp)
        sock.sendto(packet, (SERVER_IP, SERVER_PORT))

        print(f"Sent → Zone {ZONE_ID}: {temp:.2f} °C")

    except ValueError:
        print("Bad reading from Arduino, skipping...")
    except Exception as e:
        print(f"Error: {e}")

    time.sleep(SEND_INTERVAL)
