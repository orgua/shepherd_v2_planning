# BQ25570 Characteristics

## Setup

Components discribed from front to back

- constant current (CC) supply
	- 400 mA, 700 mA, 900 mA, 1100 mA 
- LED in wooden light box
	- Cree XM-L
- Solar cells in same box, exposed to the LEDs
	- two KXOB121K04F in series
- BQ25570 with said solar cells as input
	- BQ25570 Eval Kit
- resistive load on output of buck-converter
	- Open Circuit (OC), 1k, 100 ohm
	
## Measurements

- ivcurves of solar cells, recorded with shepherd harvester
- Saleae Logic Pro 16 (2MOhm Impedance) was used to record analog pins of BQ-IC
	- V_IN - output of solar cell, input of BQ
	- V_BAT - voltage over storage capacity on Eval Kit
	- V_Out - output of buck-converter, input of load
- BAT_OK signal was recorded digitally by the logic pro
	- signal is analog according to datasheet. (=V_BAT when ON) 

NOTE: the .sal-files can be opened by the freely available Logic 2 software.
	-> traces can be exported to csv via file -> export raw data

## Analog Parts

R100 = 99.79 Ohm
R1k = 983.263 Ohm
C_Stor = 79uF

## Experiments

- 400 mA LED, open circuit
	- input is disconnected and rises to VOC @ 3.35 V
	- capacitor is limited to ~ 4.1 V max
	- output is stable at 1.8 V
- 400 mA LED, 1k Ohm
	- open circuit voltage seems to be 2.9 V
	- output gets enabled when cap rises above 2.35 V
	- output is on for ~ 10 ms, every 120 ms
	- output does not turn off completely right away
	- bat-OK is never high
- 700 mA, 1k Ohm
	- output is on for ~ 80 ms, every 175 ms (45%)
	- bat-ok is high for ~ 58 ms
- 900 mA, 1k Ohm
	- output is on for ~ 150 ms, every 233 ms (64%)
	- bat-OK is high for ~ 58 ms
- 1100 mA, 1k Ohm
	- output always on
	- cap survives VOC-measurement
- 400 mA, 100 Ohm, intermittent
	- 43 s -> disconnect resistor
	- 58 s -> reconnect resistor

NOTE: all measurements are started with a disabled LED to show startup-behavior of the IC.
