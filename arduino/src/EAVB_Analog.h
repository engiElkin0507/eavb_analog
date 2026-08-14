#ifndef EAVB_ANALOG_H
#define EAVB_ANALOG_H
#include <Arduino.h>

class EAVB_ADCScale {
public:
    EAVB_ADCScale(int resolution_bits, float vref);
    float raw_to_volts(int raw_val);
private:
    int _resolution_bits;
    float _vref;
    int _max_ticks;
};

class EAVB_VoltageDivider {
public:
    EAVB_VoltageDivider(float r1, float r2, EAVB_ADCScale* adc_scale);
    float decode_raw_adc(int raw_val);
private:
    float _r1;
    float _r2;
    float _attenuation;
    EAVB_ADCScale* _adc;
};
#endif
