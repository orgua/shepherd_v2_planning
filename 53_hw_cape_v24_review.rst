Shepherd Cape v2.4b
==================

Hardware
--------

- 15 Capes with Emu & Hrv, produced by Egas
- Serialnumbers

    - 1270053 -> initial test subject
    - 1270057

- to solder:

    - 2x 2x46 Pinheader,
    - 2x 2x9 Pinheader,
    - 2Pin VoltageInput Screwed,
    - 4Pin ButtonConn,
    - 2x2Pin HrvPort


Initial Test for Functionality
------------------------------

PCB 1270053
~~~~~~~~~~~

- visual: OK

    - all ICs and diodes correct orientation
    - no visible shorts or other defects

- 5V In: 0mA, OK
- EN-Pin: 105 mA, OK, but 3x higher than before, but with hrv (was 71 mA on hw-v2.1)
- voltages:

    - L5V ->    5.000 V
    - L3V3 ->   3.295 V
    - 6V ->     6.19 V
    - 10V ->    9.71 V
    - -6V ->    -5.99 V
    - 5V

- **for reference**: 1270057 behaves the same
- booting with cape: all OK

    - 340 - 400 mA during boot
    - ~ 330 mA after boot

- devicetest-tool - OK

    - ADCs & DACs work
    - GPIO out is working
    - Changing Power & GPIO routing works

- GPIO Sweep -> safe Bandwidth ~ 3 MHz, 10 MHz might also work
- GPIO Toggling:

    - Port A: works on all Pins
    - Port B: open

- Watchdog: OK
- Cal OK
- Profiling OK

    - but pretty high stddev on ADC-Current for hrv & emu (~80)

PCB Nr. 1270057
~~~~~~~~~~~~~~~

- Visual OK
- GPIO Toggling Port A & B all Pins OK
- Emu as expected



- TODO: Cal with & without additional Caps, GPIO-Direction-Change,



Errors & Improvements (for 2.4c)
--------------------------------

- BB does not survive turning on the cape

    - Reason: Voltage drop due to increased Caps on Rails
    - FIX: Order for 5V-Input:
    - 3.3 mF Cap: https://www.mouser.de/ProductDetail/Rubycon/6.3ZLJ3300M10X25?qs=T3oQrply3y/OcsI9e27BJQ%3D%3D
    - 6.8 mF Cap: https://www.mouser.de/ProductDetail/Panasonic/ECA-0JHG682?qs=R8vM2Es5yU5OqYwkFTor4Q%3D%3D

- Opa189 does not work for emulator for full range -> replace with Opa388
- ref-voltage can use more buffering -> add >= 100 nF from U3-Pin6 to -6V (Pin5)

    - same for U7

- EMU: Voltage-dependency for Current Measurement after switching to Opa388

    - 0V: ~ 550 n, 5V: ~ 980 n
    - -> +430 increments for + 5 V change (= +80 uA error, or +8.39 mV @ ADC-Input)
    - there is no current flow! Trace cut after Shunt
    - AD8429 - Ref to Output has only 50 kOhm (older PCB show the same)
    - **tldr**: ref-pin does not work as expected when != GND
    - TODO:

        - hrv looked fine, why?
        - remove 2R of Reference (can cause 500 uV offset)
        - only 1 InAmp for the Reference
        - try load-R + Cap between Ref & Output of InAmp



Ref = GND

  DAC @ 0.400 V;        SMU: 0.100 mA @ 0.3998 V;       I_raw: mean=466.85, stddev=99.89
  DAC @ 0.400 V;        SMU: 1.000 mA @ 0.3998 V;       I_raw: mean=4903.37, stddev=85.11
  DAC @ 0.400 V;        SMU: 10.000 mA @ 0.3995 V;      I_raw: mean=49276.55, stddev=88.43
  DAC @ 0.400 V;        SMU: 20.000 mA @ 0.3993 V;      I_raw: mean=98601.06, stddev=101.11

  DAC @ 2.000 V;        SMU: 0.100 mA @ 1.9999 V;       I_raw: mean=465.69, stddev=82.45
  DAC @ 2.000 V;        SMU: 1.000 mA @ 1.9999 V;       I_raw: mean=4902.77, stddev=70.92
  DAC @ 2.000 V;        SMU: 10.000 mA @ 1.9996 V;      I_raw: mean=49274.69, stddev=75.39
  DAC @ 2.000 V;        SMU: 20.000 mA @ 1.9993 V;      I_raw: mean=98596.15, stddev=86.44

  DAC @ 5.000 V;        SMU: 0.100 mA @ 4.9828 V;       I_raw: mean=463.06, stddev=5.78
  DAC @ 5.000 V;        SMU: 1.000 mA @ 4.9732 V;       I_raw: mean=4900.14, stddev=5.81
  DAC @ 5.000 V;        SMU: 10.000 mA @ 4.8746 V;      I_raw: mean=49275.76, stddev=7.61
  DAC @ 5.000 V;        SMU: 20.000 mA @ 4.7552 V;      I_raw: mean=98601.86, stddev=12.64

Ref = 10 mV

  DAC @ 0.400 V;        SMU: 0.100 mA @ 0.3998 V;       I_raw: mean=1023.15, stddev=99.29
  DAC @ 0.400 V;        SMU: 1.000 mA @ 0.3998 V;       I_raw: mean=5464.52, stddev=85.00
  DAC @ 0.400 V;        SMU: 10.000 mA @ 0.3996 V;      I_raw: mean=49884.01, stddev=88.74
  DAC @ 0.400 V;        SMU: 20.000 mA @ 0.3993 V;      I_raw: mean=99258.19, stddev=101.85

  DAC @ 2.000 V;        SMU: 0.100 mA @ 1.9999 V;       I_raw: mean=1182.66, stddev=83.35
  DAC @ 2.000 V;        SMU: 1.000 mA @ 1.9999 V;       I_raw: mean=5623.73, stddev=73.04
  DAC @ 2.000 V;        SMU: 10.000 mA @ 1.9997 V;      I_raw: mean=50041.69, stddev=76.88
  DAC @ 2.000 V;        SMU: 20.000 mA @ 1.9995 V;      I_raw: mean=99412.23, stddev=87.57

  DAC @ 5.000 V;        SMU: 0.100 mA @ 4.9827 V;       I_raw: mean=1458.09, stddev=6.08
  DAC @ 5.000 V;        SMU: 1.000 mA @ 4.9732 V;       I_raw: mean=5899.41, stddev=6.18
  DAC @ 5.000 V;        SMU: 10.000 mA @ 4.8756 V;      I_raw: mean=50311.76, stddev=7.57
  DAC @ 5.000 V;        SMU: 20.000 mA @ 4.7576 V;      I_raw: mean=99679.24, stddev=12.69

Ref = 10 mV, double 0R

  DAC @ 0.400 V;        SMU: 0.100 mA @ 0.3998 V;       I_raw: mean=1335.36, stddev=99.78
  DAC @ 0.400 V;        SMU: 1.000 mA @ 0.3998 V;       I_raw: mean=5776.61, stddev=85.28
  DAC @ 0.400 V;        SMU: 10.000 mA @ 0.3996 V;      I_raw: mean=50194.40, stddev=88.54
  DAC @ 0.400 V;        SMU: 20.000 mA @ 0.3993 V;      I_raw: mean=99565.63, stddev=101.33

  DAC @ 2.000 V;        SMU: 0.100 mA @ 1.9999 V;       I_raw: mean=1494.28, stddev=82.19
  DAC @ 2.000 V;        SMU: 1.000 mA @ 1.9999 V;       I_raw: mean=5935.56, stddev=71.70
  DAC @ 2.000 V;        SMU: 10.000 mA @ 1.9997 V;      I_raw: mean=50351.44, stddev=75.40
  DAC @ 2.000 V;        SMU: 20.000 mA @ 1.9994 V;      I_raw: mean=99723.23, stddev=86.35

  DAC @ 5.000 V;        SMU: 0.100 mA @ 4.9827 V;       I_raw: mean=1771.01, stddev=6.09
  DAC @ 5.000 V;        SMU: 1.000 mA @ 4.9732 V;       I_raw: mean=6212.20, stddev=6.03
  DAC @ 5.000 V;        SMU: 10.000 mA @ 4.8753 V;      I_raw: mean=50624.02, stddev=7.78
  DAC @ 5.000 V;        SMU: 20.000 mA @ 4.7568 V;      I_raw: mean=99989.86, stddev=12.78

adc_voltage = value_raw * 1.25 * 4.096 / (2**18)
            = 8.39 mV



TODO-List
---------

- change ADC to higher resolution?
- change OP-Ampdriver to higher output?
- make system modular?
- direction pin GPO:3 for leveltranslators is named strangely
