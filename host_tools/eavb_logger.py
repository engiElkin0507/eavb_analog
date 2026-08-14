import serial
import time

def log_data(port, baudrate=115200, filename="analog_log.csv"):
    with serial.Serial(port, baudrate) as ser, open(filename, 'w') as f:
        print(f"Logging telemetry from {port} to {filename}...")
        while True:
            try:
                line = ser.readline().decode('utf-8').strip()
                if line:
                    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
                    f.write(f"{timestamp},{line}\n")
                    print(line)
            except KeyboardInterrupt:
                break

if __name__ == "__main__":
    log_data("COM3") # Change to your port
