class ADCScale:
    def __init__(self, resolution_bits=12, vref=3.3):
        self.resolution_bits = resolution_bits
        self.vref = vref
        self.max_ticks = (1 << resolution_bits) - 1

    def raw_to_volts(self, raw_val: int) -> float:
        raw_val = max(0, min(raw_val, self.max_ticks))
        return (raw_val / self.max_ticks) * self.vref
