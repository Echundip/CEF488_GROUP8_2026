import socket
import struct
import csv
from datetime import datetime

# --- CONFIGURATION ---
SERVER_IP = "0.0.0.0"
SERVER_PORT = 5005
ALERT_CLIENT_IP = "192.168.x.x"  # Replace with alert client IP
ALERT_PORT = 5006
THRESHOLD = 38.0
CSV_FILE = "temperature_log.csv"
# ---------------------

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((SERVER_IP, SERVER_PORT))
alert_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
zone_readings = {}

with open(CSV_FILE, mode="w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Timestamp", "Zone", "Temperature (C)", "Zone Average (C)", "Overall Average (C)", "Alert"])

print(f"Server listening on port {SERVER_PORT}...")

while True:
    try:
        data, addr = sock.recvfrom(1024)
        zone_id, temp = struct.unpack("!Bf", data)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        zone_readings.setdefault(zone_id, []).append(temp)
        zone_avg = sum(zone_readings[zone_id]) / len(zone_readings[zone_id])
        all_temps = [t for r in zone_readings.values() for t in r]
        overall_avg = sum(all_temps) / len(all_temps)

        alert = temp > THRESHOLD
        if alert:
            msg = f"ALERT! Zone {zone_id}: {temp:.2f}C exceeds {THRESHOLD}C threshold!"
            alert_sock.sendto(msg.encode("utf-8"), (ALERT_CLIENT_IP, ALERT_PORT))
            print(f"[ALERT SENT] {msg}")

        with open(CSV_FILE, mode="a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([timestamp, zone_id, f"{temp:.2f}", f"{zone_avg:.2f}", f"{overall_avg:.2f}", "YES" if alert else "NO"])

        print(f"[{timestamp}] Zone {zone_id}: {temp:.2f}°C | Zone Avg: {zone_avg:.2f}°C | Overall Avg: {overall_avg:.2f}°C")

    except struct.error:
        print("Malformed packet received, skipping...")
    except Exception as e:
        print(f"Server error: {e}")
