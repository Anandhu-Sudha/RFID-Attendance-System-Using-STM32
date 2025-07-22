import csv
import serial
import re

# Configure serial port
ser = serial.Serial('COM7', 115200, timeout=1)

# CSV file
csv_filename = 'attendance_log.csv'

# Initialize CSV file with header (overwrite on each run)
with open(csv_filename, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Direction', 'Name', 'Employee ID', 'Time'])

# Write function
def write_to_csv(direction, name, emp_id, device_time):
    with open(csv_filename, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([direction, name, emp_id, device_time])

# Regex to match the pattern: IN/OUT - Name (EMPxxx) at HH:MM:SS
log_pattern = re.compile(r'^(IN|OUT) - (.+) \((EMP\d+)\) at (\d{2}:\d{2}:\d{2})$')

try:
    while True:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8', errors='ignore').strip()
            match = log_pattern.match(line)
            if match:
                direction = match.group(1)
                name = match.group(2)
                emp_id = match.group(3)
                device_time = match.group(4)
                write_to_csv(direction, name, emp_id, device_time)
                print(f"{direction}, {name}, {emp_id}, {device_time}")
except KeyboardInterrupt:
    print("Logging stopped by user.")
finally:
    ser.close()
