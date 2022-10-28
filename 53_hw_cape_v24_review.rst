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

Nr. 1270053

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
- Watchdog: OK
- Cal OK
- Profiling OK

    - but pretty high stddev on ADC-Current for hrv & emu (~80)


- TODO: Cal with & without additional Caps, GPIO-Direction-Change,

- Order for 5V-Input:

    - 3.3 mF Cap: https://www.mouser.de/ProductDetail/Rubycon/6.3ZLJ3300M10X25?qs=T3oQrply3y/OcsI9e27BJQ%3D%3D
    - 6.8 mF Cap: https://www.mouser.de/ProductDetail/Panasonic/ECA-0JHG682?qs=R8vM2Es5yU5OqYwkFTor4Q%3D%3D

TODO-List
---------

- change ADC to higher resolution?
- change OP-Ampdriver to higher output?
- make system modular?
- direction pin GPO:3 for leveltranslators is named strangely
