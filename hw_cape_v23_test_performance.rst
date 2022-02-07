Shepherd Cape v2.3 - Performance
================================

Tested
------

- WD is fine now -> gets turned on
- BB boots with Shepard Cape on
- BB-powered boot works, but turning Cape on crashes the 5V Rail (P9-7/8)


TODO
-----

- fix BB-Powered Mode
- determine final fixes for EMU
- determine final fixes for HRV
- test WD restarting BB
- determine stencil-thickness (=100um) -> shrink some paste-mask-pads
- remove inductors from A5V, 10/-6V

Troubleshooting
---------------

Profiling Ranges

- full range: 0 to 5V, 0 to 50 mA
- limited range: 1 to 3.9 V, 3uA to 40mA

Harvester - low current measurement-limit

- draining below 1-2 uA -> voltage seems to invert (SMU reports -0.3V), not caring about the set-voltage of the DAC
- adc-current values are equal to "zero"
- diode blocks (later tests show 2nA reverse current), because voltage at cathode (opAmp-Out) is similar high to DAC-Voltage
- something seems to reverse leak current -> tldr: it is the OPA189 Negative Input Pin
    - **OPA189 input** can leak max +-1 nA (input bias current) and differential input impedance is 100 MOhm (100nA to 10V)
    - AD8421 inputs can leak max 2x +-500 pA, tests show < 1 nA
    - OPA2388 input can leak max +-400 pA (spec), tests show < 1 nA
    - diode is rated for 40 nA but shows in tests 2 nA @ 5V (see picture below)
    - capacitor C34 (Opa-Feedback) could leak -> tests show < 1 nA @ +-5V-Range (see picture below)
    - and the op189 output -> not relevant due to safe diode and capacitor
    - removing R20 stops the leak -> hint at OPA189 or cap C34
    - removing C34 changes nothing -> final clue for OPA189
- that may never occur with a real harvesting source (or work as a hard-to-detect offset)
- baking pcb off (80 °C, 30min) had no effect (mentioned in datasheet)
- this leakage is often not existent when SMU is freshly started for the day -> firmware-update to 3.4.0 (2021-04, from 3.2.2 2016-04) did not help
    - see profile 25, whole voltage range, down to 0 uA
- changing R20 (Feedback-Lowpass) to 100R or 10k does not change behaviour
- tests with solar-cell (SM101K09L) shows that 2uA is near to dark environment
- TODO:
    - reverse position of diode and shunt
    - OPA189 speaks of (8.3.3) input bias current clock feedthrough (switching input to correct intrinsic offset)
    - -> it seems to be the "zero-drift" feature of OPA189 that gets triggered wrongly
    - worst outcome: 1-2 uA offset in measurement

.. image:: ./media_v23/harvester_schematic_v230.png


.. image:: ./media_v23/current_leakage_capacitor_feedback_1nF.png


.. image:: ./media_v23/current_leakage_at_harvest_port.png

.. image:: ./media_v23/solar_power_SM101KO9L.png

Diode Comparison

- PMEG10010ELRX
    - rated for (extremely low leakage current) **4 nA @ 10 V & 25 °C** and 40 nA (typical, 150 nA max) at 100V & 25°C
    - measurement: -5 V result in **2.1 nA at room temperature**
    - seems the safest bet, because datasheet promises the spec
- SMMSD701T1G
    - rated for ~ 8-9 nA @ 6-12 V & 25 °C (curves in datasheet)
    - measurement: -5 V result in **1.4 nA at room temperature**
    - lowest leak-value but not distinguishable from PMEG-Version in Frontend
- RB168MM-40TR
    - rated for 50 (typical) to 550 uA reverse current @ 40 V
    - curves in datasheet show IR @ 5 V, 25°C at around 10 nA, up to 1000 nA at 75°C
    - measurement: -5 V result in **6.9 nA at room temperature**
- the first two diodes are fine!
- --> see media_v23/profiler_smu_diodes.csv

.. image:: ./media_v23/diode_reverse_currents_smu-measured.png

Harvester - Current Measurement

- 2R-Shunt, Gain x48 -> 10R Shunt, Gain x10
    - no significant effect from profiler
    - **keep synced to emulator to save parts**
- Lowpass between InAmp and ADC
    - 100k results in high offset of > 11k increments for 0 nA (ADC input seems to be raised by ADC itself)
    - 1k results in offset = ~ 182 (Good) and lower Noise, mostly on full range (3-14x better)
    - 100R seems to worsen limited area (slightly), but improve full range (almost x2)
    - Cap was varied to match 80 - 160 kHz lowpass, but influence is minimal
    - 33R / 10nF is also fine, limited range gets minimal worse, but full range improves
- buffered shunt (parallel cap C35)
    - 470 nF instead of nothing: 10 - 20% improvement on limited and full range
    - nothing instead of 100 nF: 5-10 % worse on full range, minimal better on limited range (but with 100 nF seems the better bet)
    - 100nF instead of nothing: ~10% improvement on both ranges
- buffered inputs (Caps on V_HRV and V_Sense)
    - adding 2x 100nF is ~ 10 % worse
- different diode (try alternatives)
    - no significant effect between new (and better) SMMSD701T1G-Diode and (current) PMEG10010ELRX
- slower OpAmp-Feedback
    - R20, 10k instead of 1k or 100R: 10-12% improvement for both ranges, but only static case (lowpass 16 kHz)
- DAC to OpAmp Connection
    - slower response helps measurement

Harvester - Voltage Measurement

- bigger shunt Resistor is 5-10% worse
- C35 parallel to shunt is better than no Cap, 100 nF is fine
- R16 before ADC-V is better 1k
- Cap before ADC-V is better, 10nF compared to nothing brings 10 % improvement
- R18 before OpAmp was 1k, removal brings 10 % improvement
- Caps 100nF on Pinheader-Inputs is 5-10 % worsening
- R20 low -> Voltage-Matcher should be rather fast (better for V_meas, worse for C_meas)
- DAC-Lowpass is fine, lower Freq helps measurement

- TODO:
    - R16 add back 1k
    - R20 add back 1k
    - C26 to 10nF
    - R27 to 100R

emulator

- can't produce 5 V with 50 mA
- even at 0 mA the limit of 5 V is not completely on point,
- at 50 mA around 4 V are usable without large error
- -> seems to be fine for modern electronics
- 2 R Shunt resistor is responsible of 100 mV drop (50 mA)


.. image:: ./media_v23/profile_quiver_offset_sheep0_cape_v230c1_profile_07_short_C6_increased_1uF_emu_a.png

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
- reverse order of diode & shunt in harvester ?? No, seems fine currently
- harvester
    - R22 to 33R
    - C140, TP6 to 10nF
    - R18, can be removed (or lowered to 33R)
