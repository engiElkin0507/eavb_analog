# host_tools/eavb_plotter.py
import serial
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from collections import deque
import sys
import math
import random
import time

class LivePlotter:
    def __init__(self, port, baudrate=115200, max_points=100):
        self.port = port
        self.baudrate = baudrate
        self.max_points = max_points
        self.data_dict = {}
        self.lines = {}
        self.test_mode = (self.port == "TEST")
        self.start_time = time.time()
        
        if not self.test_mode:
            try:
                self.ser = serial.Serial(self.port, self.baudrate, timeout=0.1)
                print(f"Connected to {self.port} at {self.baudrate} baud.")
            except serial.SerialException:
                print(f"Error: Could not open {self.port}. Is it plugged in?")
                sys.exit(1)
        else:
            print("RUNNING IN TEST MODE: Generating simulated analog data...")

        # Setup Matplotlib Plot
        self.fig, self.ax = plt.subplots(figsize=(10, 6))
        self.fig.canvas.manager.set_window_title('EAVB Analog Telemetry Engine')
        self.ax.set_title("Live Sensor Telemetry", fontsize=14, fontweight='bold')
        self.ax.set_xlabel("Samples")
        self.ax.set_ylabel("Amplitude / Voltage")
        self.ax.grid(True, linestyle='--', alpha=0.6)

    def read_serial(self):
        try:
            if self.test_mode:
                # Generate a noisy sine wave and a clean sine wave
                t = time.time() - self.start_time
                noisy_signal = math.sin(t * 2) * 5 + random.uniform(-1.5, 1.5)
                clean_signal = math.sin(t * 2) * 5
                line = f">Noisy_Sensor:{noisy_signal:.2f},Clean_Filter:{clean_signal:.2f}"
                time.sleep(0.05) # Simulate 20Hz baud delay
            else:
                line = self.ser.readline().decode('utf-8').strip()
                
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
            pass 

    def update_plot(self, frame):
        self.read_serial()
        
        for key, line in self.lines.items():
            line.set_data(range(self.max_points), self.data_dict[key])
            
        if self.data_dict:
            all_vals = [val for dq in self.data_dict.values() for val in dq]
            self.ax.set_ylim(min(all_vals) - 1.0, max(all_vals) + 1.0)
            self.ax.set_xlim(0, self.max_points)
            
        return self.lines.values()

    def run(self):
        ani = FuncAnimation(self.fig, self.update_plot, interval=20, cache_frame_data=False)
        plt.tight_layout()
        plt.show()
        if not self.test_mode:
            self.ser.close()

if __name__ == "__main__":
    # Set to "TEST" to run without a microcontroller, or "COM3" when plugged in
    plotter = LivePlotter(port="TEST") 
    plotter.run()
