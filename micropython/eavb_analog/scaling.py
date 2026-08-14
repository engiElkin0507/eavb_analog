from .core import ADCScale

class VoltageDivider:
    def __init__(self, r1: float, r2: float, adc_scale: ADCScale):
        self.r1 = r1
        self.r2 = r2
        self.adc = adc_scale
        self.attenuation = self.r2 / (self.r1 + self.r2)

    def decode_raw_adc(self, raw_val: int) -> float:
        pin_voltage = self.adc.raw_to_volts(raw_val)
        return round(pin_voltage / self.attenuation, 4)
