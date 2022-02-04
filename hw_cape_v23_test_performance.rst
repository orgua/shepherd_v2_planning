Shepherd Cape v2.3 - Performance
================================

Tested
------

- WD is fine now -> gets turned on
- BB boots with Shepard Cape on
- BB-powered boot works, but turning Cape on crashes the 5V Rail (P9-7/8)


Profiling Frontends
-------------------

00

- lab / bench supply powered -> for all the following, if not stated otherwise

01

- raised 10V rail from 9V7 to 10V41 (R 240k to 270k) -> without benefit

02

- C101 100 uF destroyed (parallel to 1 mF) on cape-input
- L3 shorted
- voltages measurement seems to have worsended by 1 % BUT current measurement improved by 3 % (max-error)

03

- reverted to 9V7 and overhauled the profiling-system offering a short and full profile (not completely comparable)
- measure full and short profile as new baseline

04

- Shunt-Buffer-Cap C6 increased from 100 nF to 470 nF -> lowpass 170 kHz
- voltage measur




TODO
-----

- fix BB-Powered Mode
- determine final fixed for EMU
- determine final fixes for HRV
- test WD restarting BB
- determine stencil-thickness -> shrink some paste-mask-pads
- remove inductors from A5V, 10/-6V


Troubleshooting
---------------

Harvester

- below 1-2 uA drain the voltage seems to invert, not caring about the set-voltage of the DAC
- around -0.3 V reported by SMU
- adc-current values start at 11k for sinking currents, but in this mode the value "jumps" down ~3k, nothing in between
- adc increment is 223 nA, resulting in theoretical 58.4 mA range
- something seems to reverse leak current
    - OPA189 input can leak max +-1 nA (input bias current) and differential input impedance is 100 MOhm (100nA to 10V)
    - AD8421 inputs can leak max 2x +-500 pA
    - OPA2388 input can leak max +-400 pA
    - and the op-amp output
    - diode is rated for 40 nA
- that may never occur with a real harvesting source
- TODO:
    - reverse position of diode and shunt
    - lower R20 (Feedback-Lowpass) to 100R
    - opa189 input offset voltage is in that range (0.4 to 3 uV)
    - separate fixed test with scope, even without voltage adc measurement
    - possible scenario: dac demands ie. 3V, diode locks the rising output-voltage from harvester input because something is draining there: 2 OpAmp-Inputs

Diode Comparison

- PMEG10010ELRX
    - rated for (extremely low leakage current) **4 nA @ 10 V & 25 °C** and 40 nA (typical, 150 nA max) at 100V & 25°C
    - measurement: old smu data suggests 400 nA
- SMMSD701T1G
    - rated for ~ 8-9 nA @ 6-12 V & 25 °C (curves in datasheet)
    - measurement:
- RB168MM-40TR
    - rated for 50 (typical) to 550 uA reverse current @ 40 V
    - curves in datasheet show IR @ 5 V, 25°C at around 10 nA, up to 1000 nA at 75°C
    - measurement:

emulator

- can't produce 5 V with 50 mA
- even at 0 mA the limit of 5 V is not completely on point,
- at 50 mA around 4 V are usable without large error
- -> seems to be fine for modern electronics
- 2 R Shunt resistor is responsible of 100 mV drop (50 mA)


BB-Powered Mode

- turning cape on when on BB-USB-Power crashes the system
- 5V_BB (P9-7/8) gets connected to 5V Line with inductor and large 1mF Cap
- TODO
    - test without inductor and big cap, monitor voltage-rails
    - buffer 5V_SEL with big cap to counter rush-current



Changes in Layout
-----------------

- 74LVC2T45GS has too small pads -> prone to errors (very hard to see, but shorts under IC in all cases)
- Force proper Fanout with Neck-Down -> EC seems to extend solder mask expansion on its own
- feducials can go, are on outer frame
- more pads for Caps on backside
- rotate harvest port in schematic to reflect board layout
- emulator FB-Resistor-Switch can be removed
- testpoints don't need gnd - its all around
- big 0402 caps near device -> dont bother with 100nF or smaller
- bring sense / FB-line directly to target-port, maybe
- reverse order of diode & shunt in harvester