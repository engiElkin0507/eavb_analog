# host_tools/eavb_plotter.py
import serial
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from collections import deque
import sys

class LivePlotter:
    def __init__(self, port, baudrate=115200, max_points=100):
        self.port = port
        self.baudrate = baudrate
        self.max_points = max_points
        self.data_dict = {}
        self.lines = {}
        
        try:
            self.ser = serial.Serial(self.port, self.baudrate, timeout=0.1)
            print(f"Connected to {self.port} at {self.baudrate} baud.")
        except serial.SerialException:
            print(f"Error: Could not open {self.port}. Is it plugged in?")
            sys.exit(1)

        # Setup Matplotlib Plot
        self.fig, self.ax = plt.subplots(figsize=(10, 6))
        self.fig.canvas.manager.set_window_title('EAVB Analog Telemetry Engine')
        self.ax.set_title("Live Sensor Telemetry", fontsize=14, fontweight='bold')
        self.ax.set_xlabel("Samples")
        self.ax.set_ylabel("Amplitude / Voltage")
        self.ax.grid(True, linestyle='--', alpha=0.6)

    def read_serial(self):
        try:
            line = self.ser.readline().decode('utf-8').strip()
            # Expecting format: >Sensor1:4.52,Sensor2:1.11
            if line.startswith(">"):
                pairs = line[1:].split(',')
                for pair in pairs:
                    key, val = pair.split(':')
                    val = float(val)
                    
                    if key not in self.data_dict:
                        self.data_dict[key] = deque([0]*self.max_points, maxlen=self.max_points)
                        line_plot, = self.ax.plot([], [], label=key, linewidth=2)
                        self.lines[key] = line_plot
                        self.ax.legend(loc="upper left")
                        
                    self.data_dict[key].append(val)
        except Exception:
            pass # Ignore malformed packets from serial noise

    def update_plot(self, frame):
        self.read_serial()
        
        for key, line in self.lines.items():
            line.set_data(range(self.max_points), self.data_dict[key])
            
        if self.data_dict:
            # Auto-scale Y-axis based on current data
            all_vals = [val for dq in self.data_dict.values() for val in dq]
            self.ax.set_ylim(min(all_vals) - 0.5, max(all_vals) + 0.5)
            self.ax.set_xlim(0, self.max_points)
            
        return self.lines.values()

    def run(self):
        ani = FuncAnimation(self.fig, self.update_plot, interval=20, cache_frame_data=False)
        plt.tight_layout()
        plt.show()
        self.ser.close()

if __name__ == "__main__":
    # Change COM3 to /dev/ttyUSB0 or your actual port
    plotter = LivePlotter(port="COM3") 
    plotter.run()
