Virtual Source
==============


Current Features
----------------

- capacitor, with
    - max voltage
    - leakage current
    - power-good-signal with hysteresis
    - status check interval
- Boostconverter, with
    - enable threshold voltage
    - efficiency factor
- buck converter, optional, with
    - fixed output voltage
    - efficiency factor
- switchable output
    - simulated external Capacitor - should be set to buffer size of target: fast transients can't be monitored by shepherd
    - enable threshold voltage hysteresis

Implementation
--------------

- fixed point math with u32 & u64 with voltages in uV, currents in nA, power in fW, capacity in nF
- a python port is available
- modules
    - InputPower - calculated from recorded C-V-traces
    - OutputPower - voltage is set by DAC, current is measured by ADC
    - CapacitorUpdate - Voltage delta is calculated by resulting sum of Power
    - regulatorUpdate - handles internal States and Output
- limits
    - input power can be 56 bit in size (fW = uV * nA) -> ~ 72 W
        - lowest is 1 fW, but due to hardware limitations 195 nA * 19 uV = 3.7 pW
    - output power can be 50 bit in size (fW = uV * nA) -> ~ 1 W
        - difference to input due to inverted efficiency taking 14 instead of 8 bit
    - capacitor voltage can be 4.2 kV
        - due to custom faster division-function the range with low error is 0 to 5 V
    - storage capacitor can not be larger than 2.68 F (= 10*(2^28) nF)
    -
- Speed in PRU (max timings)
    -   280 ns calc input power
    -  3200 ns calc output power
    - 10500 ns update capacitor -> TODO: a custom uDiv() brings that down to 3000 ns
    -   470 ns update boost-buck
    - ~7300 ns for all (with space in between)

.. image:: media/vSource_in100uW_out2mW.png
