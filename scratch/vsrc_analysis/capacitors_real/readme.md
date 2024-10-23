# Measuring Charg / Discharge

Capacitor1: 100 uF, 6.3 V, MLCC, Taiyo Yuden, JMK316ABJ107ML-T
Capacitor2: 100 uF, 6.3 V, MLCC, Taiyo Yuden, JMK316ABJ107ML-T
Capacitor3: 100 uF, 20%, 6.3 V, Tantal, AVX TAJB107M006RNJ
Resistor: 1 kOhm (Measured 1000 Ohm)

Measured with 
- SMU - Voltage Source with programmed switch (10s pre-charge)
- Logic Analyzer with analog input, 

Oddities
- V_start during discharge is varying because of manual swap

SelfDischarge
- run for 100s
- LogicPro has 2 MOhm Impedance
- SMU was connected & charged via 1k and switched to 100pA Current-Supply for the measurement (turning it off discharged the cap quickly)
