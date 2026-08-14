#include "EAVB_Analog.h"

EAVB_ADCScale::EAVB_ADCScale(int resolution_bits, float vref) {
    _resolution_bits = resolution_bits;
    _vref = vref;
    _max_ticks = (1 << resolution_bits) - 1;
}

float EAVB_ADCScale::raw_to_volts(int raw_val) {
    if (raw_val < 0) raw_val = 0;
    if (raw_val > _max_ticks) raw_val = _max_ticks;
    return ((float)raw_val / (float)_max_ticks) * _vref;
}

EAVB_VoltageDivider::EAVB_VoltageDivider(float r1, float r2, EAVB_ADCScale* adc_scale) {
    _r1 = r1;
    _r2 = r2;
    _adc = adc_scale;
    _attenuation = _r2 / (_r1 + _r2);
}

float EAVB_VoltageDivider::decode_raw_adc(int raw_val) {
    float pin_voltage = _adc->raw_to_volts(raw_val);
    return pin_voltage / _attenuation;
}
