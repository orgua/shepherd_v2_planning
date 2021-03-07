Noise Performance
=================

Problem
-------
- Beaglebone offers noisy SYS_5V0 - TODO: add Vpp num
- POE is also noisy - TODO: add Vpp num
- shepherd shows residues of voltage spikes in target voltage
    - Solved: confirmed to be due to a "transmitting" usb-hub 50 cm away from test-setup (not powering anything)

Setup
-----
- BBGreen with Shepherd-PCB, Output VTarget set to 3V
- scope: rigol ds1104z, 100 MHz, calibrated, compensated probes, up-to-date firmware

- 50 cm radius free of additional metal
- Power-Supplies
    - setup1: 5V to BB via benchsupply with 1mF on input
    - setup2: as setup 1, but shepherd 5V and 3v3 powered by keithley sourcemeter, 1m 4-Port Cables, not buffered by Cap
    - setup3: BB powered by NoName POE-Splitter (EC-PD0520USB)
    - setup4: BB powered by TP-Link POE-Splitter (TL-POE10R), buffered by 1 mF on Input
- Measurement
    - scope input set to AC to analyse ripple, internal 20 MHz low pass active
    - probe set to 1x for low noise
    - probe connected with short ground-loop to closest GND
    - timebases /div (mostly): 50 ms, 10 ms, 1 ms, 100 us, 10 us, 1 us, 100 ns
    - voltage range: lowest setting without clipping, mostly 1 mV/div
    - scope-math: Voltage-peak-peak, frequency
- Scope-Screenshots (DS1Z_Quickprint#.png) are not linked or included here, only referenced for each measurement (./media_noise/)

Scope Noise with grounded signal-input

.. image:: media_noise/DS1Z_QuickPrint28.png


Measurements
------------

- Probe Signal shorted to ground (noise floor)
    - Vpp = 1.20 mV
    - no abnormalities or standing waves
    - QuickPrint 26-31
- **SETUP 2**
- A5V (setup2) - on biggest cap after regulator
    - Vpp = 2.10 mV
    - 1.3 MHz Ripple (1.72mVpp)
    - QuickPrint 32-36
- 10V (setup2) - on biggest cap after regulator
    - Vpp = 3.40 mV
    - 7 kHz Ripple,
    - QuickPrint 37-41
- VTargetA = 3.3 V (setup2), 1k Load
    - Vpp = 1.90 mV
    - no abnormalities or standing waves
    - QuickPrint 42-46
- VTargetA = 3.3 V (setup2), no load
    - Vpp = 1.72 mV
    - no abnormalities or standing waves
    - QuickPrint 47
- VTargetB = 3.0 V (setup2), no load
    - Vpp = 1.65 mV
    - no abnormalities or standing waves
    - QuickPrint 48-52
- SourceMeter 3V3 (setup2), ~ 4.06 mA Shepherd-Load, 4-Port-Meas
    - Vpp = 16.6 mV (unfiltered input)
    - no abnormalities, some switching noise
    - QuickPrint 53-57
- SourceMeter 5V0 (setup2), ~ 73.9 mA Shepherd-Load, 4-Port-Meas
    - Vpp = 20.4 mV (unfiltered input)
    - no abnormalities, some switching noise
    - QuickPrint 63-67
- BBone 3v3 (setup2) - on pinheader, shepherd not connected
    - Vpp = 46 mV
    - no abnormalities, some switching noise 20 kHz & 333 kHz
    - QuickPrint 58-62
- BBone SYS_5V / P9-7/8 (setup2) - on pinheader, shepherd not connected
    - Vpp = 145 mV
    - all kind of fragments from msec to nsec (50 ms & 1us view shows best)
    - QuickPrint 68-72
- BBone VDD_5V / P9-5/6 (setup2) - on pinheader, shepherd not connected
    - Vpp = 5.6 mV
    - minor abnormalities, 5Hz wave, 333 kHz switching fragments
    - QuickPrint 73-79
- **SETUP 1**
- VTargetA = 3.3 V (setup1), no load
    - Vpp = 1.8 mV
    - no abnormalities or standing waves
    - QuickPrint 80-87
- A5V (setup1) - on biggest cap after regulator
    - Vpp = 1.9 mV
    - no abnormalities, some ripple ~1.3 MHz, 1.6 mVpp
    - QuickPrint 101-106
- BBone 3v3 (setup1) - on pinheader
    - Vpp = 51 mV
    - switching noise 20 kHz, 250 kHz
    - QuickPrint 107-113
- BBone SYS_5V / P9-7/8 (setup1) - on pinheader
    - Vpp = 111 mV
    - switching noise 10 Hz, 50 Hz, 20 kHz, 333 kHz, 2.5 MHz
    - QuickPrint 114-120
- Bench Supply 5V (setup1) - 360 mA Load
    - Vpp = 37 mV
    - switching noise 10 Hz, 50 Hz, 2.5 kHz
    - QuickPrint 121-130
- Bench Supply 5V (setup1) - no Load
    - Vpp = 20 mV
    - switching noise 4 kHz
    - QuickPrint 131-137
- **SETUP 3**
- BBone 5V Input (setup3), TP-Link Poe
    - Vpp = 22 mV
    - switching noise 10 Hz, 50 Hz, 16 kHz, 256 kHz
    - QuickPrint 201-207
- VTargetA = 3.3 V (setup3), no load
    - Vpp = 2.7 mV
    - no abnormalities, but some oscillation around ~ 1 MHz
    - QuickPrint 208-215
- A5V (setup1) - on biggest cap after regulator
    - Vpp = 3.3 mV
    - no abnormalities, but some oscillation around 1.3 MHz
    - QuickPrint 216-224
- **SETUP 4**
- BBone 5V VCC P9-5/6 (setup4), NoName Poe
    - Vpp = 7.6 mV
    - heavy switching noise ~ 75 kHz
    - QuickPrint 225-232
- VTargetA = 3.3 V (setup4), no load
    - Vpp = 12.2 mV
    - heavy switching noise ~75 kHz
    - QuickPrint 233-239
- A5V (setup4) - on biggest cap after regulator
    - Vpp = 11 mV
    - ramps with 50 kHz and the additional switching noise
    - QuickPrint 240-246


Analysis
--------
- disclaimer
    - some noise is very close to the scopes lower threshold (~ 1.2 mVpp)
    - A5V-LDO should have ~ 18 uV Noise with 60 dB Ripple Rejection
    - -> measurements can't be trusted when looking at individual values, but comparisons should be valid
    - amplifying active probe should be prefered
- A5V and VTargetA are very similar -> further analysis will take maximum of these two
- setup comparison (worst to best)
    - setup4 (NoName POE) shows heavy artifacts, Noise VTarget = 12 mVpp
    - setup3 (TPLink POE) shows some oscillations, Noise A5V = 3.3 mVpp
    - setup2 (Shepherd pwrd by sourcemeter) shows minor ripple, noise A5V = 2.1 mVpp
    - setup1 (benchPowered BB) shows minor ripple, Noise A5V = 1.9 mVpp
- Sys_5V-Line is surprisingly noisy, but has limited influence on VTarget


Conclusion
----------
- BB-Power should be avoided
    - Sys-5V was already used in previous shepherd pcb
    - switch to VDD_5V (less noisy)
    - avoid 3v3, generate on shepherd
- use very low noise ldo for InAmp
- POE-Input
    - should be allowed to be > 5V, and filtered by ldo
    - **TP-Link TL-POE10R V5.0** is rated for 1A @ 9/12V, 2A @ 5V -> ~ 10 W
- Side Note
    - TP-Link POE-Splitter has heat-issues at least when powering ~300@5V, ICs are Ok, but the input Cap (47uF 100V) gets also very warm -> may shorten life-expectancy
    - there is no cheap alternative for this unit
