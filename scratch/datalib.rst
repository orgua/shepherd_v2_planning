
https://github.com/geissdoerfer/shepherd-datalib
curve-recording / IVonne -> 50 Hz Measurement with Short-Circuit-Current and two other parameters -> diode based model parameters but no real "curves"?
    -> my understanding of curve: ie repeating curve-trace -> 128 datapoints with 5V-to-0V voltage-ramp (for solar-cell) and resulting harvested current
    -
db_curves -> initial proto-i-curve and proto-v-ramp, and parameters to every discrete time-sample to scale the curve in each dimension
    -? why not use normed proto-curves, ie, 1V, 1mA -> would result in cleaner coefficients
    -
db_traces -> curve after a converter / tracker, I+V-Value to every discrete timesample
db_voltage -> just a very long ramp
    -? why let voltage ramp down over 300 s?
    -? just an example for custom target voltage?

-? are artificial curves what we want?
- more general approach:
    - harvester records currents of repeating 250-Step Voltage ramp with 100 kHz
        - 20 mV Resolution for 0 to 5 V
        - 400 curves per second (or 200 if two timeslots are needed for settling)
    - emulator gets windowsize-config and that exact data in a stream
        - timestep-calculation for some generic MPPT consists of ::

    static: age_new = age_old = p_max_new = p_max_old = 0, window_size = 250

    p_atm = v * c
    age_new++
    age_old++
    if p_atm > p_max_new:
        p_max_new = p_atm
        age_new = 0
    if (age_old > window_size) or (p_max_new >= p_max_current):
        p_max_old = p_max_new
        age_old = age_new
        p_max_new = 0
        age_new = 0
    return p_max_old


calibrate.py measure sheep0 -u hans --smu-ip 10.0.0.41 --emulation -o sheep0_meas.yml
calibrate.py convert sheep0_meas.yml -o sheep0_cal.yml

calibrate.py write sheep0 -c sheep0_cal.yml -v 22A0 -s 2021w28i0001 -u hans
calibrate.py read sheep0 -u hans

sudo shepherd-sheep eeprom read
