# micropython/eavb_analog/scaling.py
from .core import ADCScale

class VoltageDivider:
    """Handles reverse-math for analog sensors running through a voltage divider."""
    def __init__(self, r1: float, r2: float, adc_scale: ADCScale):
        self.r1 = r1
        self.r2 = r2
        self.adc = adc_scale
        # The attenuation factor: V_out = V_in * (R2 / (R1 + R2))
        self.attenuation = self.r2 / (self.r1 + self.r2)

    def decode_raw_adc(self, raw_val: int) -> float:
        """Converts raw ADC tick to true voltage at the top of the divider."""
        pin_voltage = self.adc.raw_to_volts(raw_val)
        return round(pin_voltage / self.attenuation, 4)


class HardwareSolver:
    """The 'Junk Drawer' calculator for safe voltage dividing."""
    @staticmethod
    def recommend_resistors(vin_max: float, vout_target: float, available_resistors: list) -> dict:
        best_r1, best_r2, best_vout = None, None, 0.0
        
        for r1 in available_resistors:
            for r2 in available_resistors:
                calc_vout = vin_max * (r2 / (r1 + r2))
                
                # Find the closest voltage that does NOT exceed the MCU's target limit
                if calc_vout <= vout_target and calc_vout > best_vout:
                    best_vout = calc_vout
                    best_r1, best_r2 = r1, r2
                    
        return {"R1": best_r1, "R2": best_r2, "Vout": round(best_vout, 3)}


class ScaledSensor:
    """Maps a physical voltage to a real-world unit (e.g., Voltage -> pH, or Voltage -> Celsius)."""
    def __init__(self, offset: float, slope: float):
        """
        Standard linear equation: y = mx + b
        slope (m): How much the unit changes per 1 Volt.
        offset (b): The baseline unit value when Voltage is 0.
        """
        self.offset = offset
        self.slope = slope

    def compute(self, voltage: float) -> float:
        """Returns the physical engineering unit."""
        unit_value = (self.slope * voltage) + self.offset
        return round(unit_value, 3)
