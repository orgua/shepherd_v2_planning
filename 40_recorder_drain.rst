
Problem
-------
- harvest source is weak, so connect it with low leakage
- current drain is a Mosfet, that can pull the source to the desired voltage
- mosfet is controlled by an inverted opAmp-voltage-buffer, resulting in a PWM-Controller that is smoothed out by a slow RC-Filter
- RC-Lowpass is delaying (big) voltage-changes by 1 to 1.7 ms
- second problem: opAmp is oscillating, there must be a better way

Ideas / Approaches
------------------
- JFET
    - pro: larger resistive range than mosfet
    - con: negative voltage required, very little variety
- PID controlled Mosfet
    - controller can hopefully be reduced to just one OpAmp
    - con: very complex, tuning required
    - TODO: maybe there is just some integrator and a small proportional part needed
- Bipolar Transistor
    - TODO: can a BJT go into very high impedance? Seems not (small sample check)
- drain directly into output of OpAmp (voltage buffer)
    - pro: fast, clean, simple
    - con: no high impedance, could feed into a harvest source
- Switched OpAmp-Sink
    - Mosfet above OpAmp -> would need voltage offset to control mosfet
    - analog switch would be a nicer solution than mosfet
    - con: could still feed into harvest source
- oneway OpAmp-Sink
    - Diode above OpAmp to stop reverse flow
    - could be included in opAmp-return-path
    - con: still no high impedance
- conclusion: combined switched oneway OpAmp-Sink could be a proper solution
