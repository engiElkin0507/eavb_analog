# micropython/examples/pico_live_ph_read.py
from machine import ADC, Pin
import time

# Import your custom EAVB ecosystem seamlessly!
from eavb_analog import (
    ADCScale, 
    VoltageDivider, 
    ScaledSensor, 
    MovingAverage, 
    TelemetryStreamer
)

# 1. Hardware Setup (Raspberry Pi Pico)
ph_adc_pin = ADC(Pin(26))
pico_adc = ADCScale(resolution_bits=12, vref=3.3) # Pico has 12-bit ADC

# 2. Define the Circuit (Sensor -> 10k -> 4.7k -> Ground)
divider = VoltageDivider(r1=10000, r2=4700, adc_scale=pico_adc)

# 3. Define the Sensor Math (Example pH probe calibration)
# Let's say 0V = pH 7.0, and it drops 59.16mV per pH step
ph_mapper = ScaledSensor(offset=7.0, slope=-16.9) 

# 4. Signal Conditioning & Telemetry
# A 15-sample moving average to kill power supply ripple
filter_ph = MovingAverage(window_size=15) 
# Stream to the laptop at exactly 20Hz
streamer = TelemetryStreamer(hz=20) 

print("Starting EAVB Analog Engine... Open eavb_plotter.py on Host.")

while True:
    # A. Read Raw Hardware
    raw_val = ph_adc_pin.read_u16() >> 4  # Shift 16-bit to 12-bit for Pico
    
    # B. Reverse the Voltage Divider
    true_voltage = divider.decode_raw_adc(raw_val)
    
    # C. Map Voltage to Physical pH Unit
    raw_ph = ph_mapper.compute(true_voltage)
    
    # D. Filter out the noise
    clean_ph = filter_ph.update(raw_ph)
    
    # E. Pack and stream to the host plotter
    streamer.pack_and_send(Raw_Volts=true_voltage, Clean_pH=clean_ph)
    
    # Run loop as fast as possible; TelemetryStreamer handles the 20Hz timing natively
    time.sleep_ms(2)
