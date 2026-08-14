# micropython/eavb_analog/telemetry.py
import time

class TelemetryStreamer:
    """Handles non-blocking serial packet streaming at a fixed frequency."""
    
    def __init__(self, hz: int = 50):
        """hz: How many times per second to output data to the serial port."""
        self.interval_ms = int(1000 / hz)
        self.last_send = time.ticks_ms()

    def pack_and_send(self, **kwargs) -> bool:
        """
        Takes keyword arguments and sends them if the time interval has passed.
        Format: >Key1:1.23,Key2:4.56
        """
        now = time.ticks_ms()
        if time.ticks_diff(now, self.last_send) >= self.interval_ms:
            # Build the fast CSV payload
            payload = ",".join([f"{k}:{v}" for k, v in kwargs.items()])
            print(f">{payload}") # The '>' symbol acts as our packet header
            self.last_send = now
            return True
        return False
