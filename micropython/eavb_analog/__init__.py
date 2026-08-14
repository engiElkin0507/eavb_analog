# micropython/eavb_analog/__init__.py

from .core import ADCScale
from .scaling import VoltageDivider, HardwareSolver, ScaledSensor
from .filters import MovingAverage, ExponentialFilter
from .telemetry import TelemetryStreamer

__version__ = "1.0.0"
__author__ = "Elcyn Andrew V. Booc"
