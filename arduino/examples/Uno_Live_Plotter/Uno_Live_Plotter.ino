#include <EAVB_Analog.h>

EAVB_ADCScale uno_adc(10, 5.0);
EAVB_VoltageDivider vdiv(10000.0, 4700.0, &uno_adc);

void setup() {
    Serial.begin(115200);
}

void loop() {
    int raw = analogRead(A0);
    float real_voltage = vdiv.decode_raw_adc(raw);
    
    // Fast Telemetry format >V:value
    Serial.print(">V:");
    Serial.println(real_voltage);
    delay(50);
}
