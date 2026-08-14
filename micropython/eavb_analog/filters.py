class MovingAverage:
    def __init__(self, window_size=10):
        self.window_size = window_size
        self.buffer = []

    def update(self, val: float) -> float:
        self.buffer.append(val)
        if len(self.buffer) > self.window_size:
            self.buffer.pop(0)
        return sum(self.buffer) / len(self.buffer)
