# micropython/eavb_analog/filters.py

class MovingAverage:
    """A standard ring-buffer filter for smoothing stable analog signals (e.g., battery rails)."""
    def __init__(self, window_size: int = 10):
        self.window_size = window_size
        self.buffer = []
        self._sum = 0.0

    def update(self, val: float) -> float:
        self.buffer.append(val)
        self._sum += val
        
        if len(self.buffer) > self.window_size:
            self._sum -= self.buffer.pop(0)
            
        return self._sum / len(self.buffer)

class ExponentialFilter:
    """
    A lightweight, memory-efficient low-pass filter for dynamic signals.
    alpha: 0.0 to 1.0. Lower values = smoother but slower response. Higher = faster but noisier.
    """
    def __init__(self, alpha: float = 0.2):
        self.alpha = max(0.0, min(1.0, alpha))
        self.current_value = None

    def update(self, new_val: float) -> float:
        if self.current_value is None:
            self.current_value = new_val # Initialize on first read
        else:
            self.current_value = (self.alpha * new_val) + ((1.0 - self.alpha) * self.current_value)
        return round(self.current_value, 4)
