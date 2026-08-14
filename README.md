# eavb_analog

An industrial-grade Analog Front-End (AFE) conditioning, sensor scaling, and telemetry library designed for high-performance embedded systems, precision sensor arrays, and custom robotics.

Developed by Elcyn Andrew V. Booc

---

## Architecture & Ecosystem Overview

`eavb_analog` bridges the gap between raw hardware analog signals and high-level microcontroller logic. It is built to be cross-platform, sharing identical math models across **Standard Python (Host)**, **MicroPython / CircuitPython (Edge)**, and **Arduino C++ (Edge)**.

```text
eavb_analog/
│
├── README.md                   # Master documentation and API guide
├── LICENSE                     # MIT License
│
├── host_tools/                 # Runs on Laptop / Raspberry Pi (Standard Python)
│   ├── eavb_plotter.py         # Real-time multi-axis live oscilloscope grapher
│   ├── eavb_logger.py          # CSV data streaming utility for research
│   └── requirements.txt        # Python host dependencies (pyserial, matplotlib)
│
├── micropython/                # Runs on RP2040 / ESP32 (MicroPython)
│   ├── eavb_analog/
│   │   ├── __init__.py         # Package root & namespace loader
│   │   ├── core.py             # ADC resolution mapping and raw-to-voltage conversion
│   │   ├── scaling.py          # Voltage divider math and resistor recommendation solver
│   │   ├── filters.py          # Signal smoothing (moving averages, exponential low-pass)
│   │   └── telemetry.py        # Fast serial packet string builder
│   └── examples/
│       └── pico_live_ph_read.py# Complete end-to-end sensor reading example
│
└── arduino/                    # Runs on standard Arduino / Teensy (C++)
    ├── library.properties      # Metadata for the Arduino Library Manager
    ├── src/
    │   ├── EAVB_Analog.h       # C++ Header for ADC & Scaling logic
    │   ├── EAVB_Analog.cpp     # C++ Implementation
    │   ├── EAVB_Filters.h      # C++ Smoothing math
    │   └── EAVB_Telemetry.h    # Fast serial packing
    └── examples/
        └── Uno_Live_Plotter/
            └── Uno_Live_Plotter.ino

```

---

## Core Features

1. **Reverse Voltage Divider & Resistor Solver:**
* Automatically calculates attenuation ratios to reverse-engineer true physical sensor voltages from divided microcontroller ADC readings.
* Built-in "Junk Drawer" hardware solver to determine the optimal resistor pair ($R_1$ and $R_2$) for stepping down high-voltage sensors (e.g., 12V or 5V) safely into 3.3V or 5V MCU logic limits.


2. **Sensor Calibration Layer:**
* Linear mapping (`ScaledSensor`) to instantly translate voltages into engineering units ($y = mx + b$), such as pH levels, thermistor temperatures, or current draw.


3. **Advanced Signal Conditioning:**
* Ring-buffer **Moving Average** filters to eliminate baseline jitter and power supply ripple.
* Lightweight **Exponential Low-Pass Filters** optimized for dynamic, high-speed signals.


4. **High-Speed Telemetry & Live Plotting:**
* Non-blocking serial packet streaming (`>Key:Value\n`) designed to prevent execution lag on microcontrollers.
* A host-side Python live plotter (`eavb_plotter.py`) built on `matplotlib` that auto-scales axes and renders multi-axis waveforms in real time.



---

## Quick Start Guide

### 1. Installation (MicroPython / Edge)

Copy the `eavb_analog/` folder into your microcontroller's filesystem (using Thonny, `ampy`, or `rshell`).

### 2. Basic Usage Example (MicroPython)

```python
from machine import ADC, Pin
from eavb_analog import ADCScale, VoltageDivider, ScaledSensor, MovingAverage, TelemetryStreamer

# Hardware setup (e.g., Raspberry Pi Pico)
adc = ADC(Pin(26))
pico_adc = ADCScale(resolution_bits=12, vref=3.3)

# Define a voltage divider circuit (10k top, 4.7k bottom)
divider = VoltageDivider(r1=10000, r2=4700, adc_scale=pico_adc)

# Map voltage to physical units (e.g., pH sensor calibration)
ph_mapper = ScaledSensor(offset=7.0, slope=-16.9)

# Filter noise and setup telemetry stream at 20Hz
smooth_filter = MovingAverage(window_size=15)
streamer = TelemetryStreamer(hz=20)

while True:
    raw_val = adc.read_u16() >> 4  # Scale 16-bit to 12-bit
    voltage = divider.decode_raw_adc(raw_val)
    raw_unit = ph_mapper.compute(voltage)
    clean_unit = smooth_filter.update(raw_unit)
    
    # Stream packet to host
    streamer.pack_and_send(Voltage=voltage, Clean_pH=clean_unit)

```

### 3. Running the Host Live Plotter

On your host laptop, install the required dependencies and run the live grapher:

```bash
pip install -r host_tools/requirements.txt
python host_tools/eavb_plotter.py

```

*(Note: Set `port="TEST"` inside `eavb_plotter.py` to run a simulated waveform test without physical hardware connected).*

---

## Arduino Installation

1. Move the `arduino/` folder contents into your Arduino libraries directory (e.g., `Documents/Arduino/libraries/eavb_analog`).
2. Open the Arduino IDE, navigate to **File > Examples > eavb_analog > Uno_Live_Plotter**, and flash it to your board.

---

## License

Distributed under the MIT License. See `LICENSE` for more information.
