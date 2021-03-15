
Problem
-------
- harvest source is weak, so connected with low leakage
- current drain is a Mosfet, that can pull the source to the desired voltage
- mosfet is controlled by an inverted opAmp-voltage-buffer, resulting in a PWM-Controller that is smoothed out by a slow RC-Filter
- RC-Lowpass is delaying big voltage-changes by 1 to 1.7 ms
- second problem: opAmp is oscillating, there must be a better way

Other Ideas
-----------
- JFET
    - pro: larger resistive range than mosfet
    - con: negative voltage required, very little variety
- PID controlled Mosfet
    - controller can hopefully reduced to just one OpAmp
    - con: very complex, tuning required
    - TODO: maybe there is just some integration and a small proportional part needed
- Bipolar Transistor
    - TODO: can a BJT go into very high impedance?
- drain directly into output of OpAmp (voltage buffer)
    - pro: fast, clean,
    - con: no high impedance, could feed into a harvest source

- Switched OpAmp
    - Mosfet above OpAmp -> would need
