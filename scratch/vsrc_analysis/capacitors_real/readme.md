# Measuring capacitor behavior

Capacitor1: 100 uF, 20%, 6.3 V, MLCC, Taiyo Yuden, JMK316ABJ107ML-T
Capacitor2: 100 uF, 20%, 6.3 V, MLCC, Taiyo Yuden, JMK316ABJ107ML-T
Capacitor3: 100 uF, 20%, 6.3 V, Tantal, AVX TAJB107M006RNJ
Resistor: 1 kOhm (cherrypick, measured 1000 Ohm)

Measured with 

- SMU - Voltage Source with programmed switch
- Logic Analyzer with analog input, 
- roomtemp is 22°C

Charge / Discharge

- let start-voltage settle for 20s
- switch & measure

SelfDischarge

- run for 100s
- LogicPro has 2 MOhm Impedance
- SMU was connected & charged via 1k and switched to 100pA Current-Supply for the measurement (turning it off discharged the cap quickly)
