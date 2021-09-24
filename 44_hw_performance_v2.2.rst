HW Performance v2.2
=====================

Hardware
--------

- 8 Capes without Recorder, produced by Egas
- Serialnumbers
    - unknown num -> kai
    - 1191022, -23, -25, -27 -> kai
    - 1191029 -> debug-setup
- lend out to kai
    - 1 Cape with pinheader (unknown number)
    - 4 Capes with Long PinSocket (1022, 1023, 1025, 1027)
    - 2 + 1 + 3 Targets


Initial Test for Functionality
------------------------------

- visual inspection OK
- External powered single cape (current limited)
    - disabled cape -> draws 0 mA @ 5 V
    - 35 mA @ 5 V when EN-Pin is Pulled Up with 3 V
    - -> no unsual behaviour
- BB powered by benchsupply 5.1 V, ~ 350 - 400 mA
- Shepherd powered by BB, VIn 5.08V
- Main Voltages on enabled Cape
    - A5V/L5V 	-> 5.000 V    	Should be Spot On
    - A3V/L3V3 	-> 3.300 V    	Should be Spot On
    - 6V 	-> 5.38 V		    [5.29; 5.47] V with 1% Res
    - 10V 	-> 9.73 V		    [9.56; 9.90] V with 1% Res
    - -6V 	-> -6 V		        [5.94; 6.06] V with 1% Res
- calibration with 10 uF (1206, 25 VMax, 16 nA Leak) on both Ports
- Generated Voltages on Target Ports -> deviation is ~ 0.1 mV
- ADC Current-Readout is noisy, despite 10 uF Buffer
- GPIO pass-through:
    - gpio 0-8 and BATOK to TA & TB
    - unconnected pru-pins (p8-41to44) are not reporting activity -> fixed
- GPIO-Speed-Test by programming a target

Capes - fixed and tested
------------------------------

- 1191022: with boot-fix, faster essential gpio, stabile current-meas, stabile V_IO, gpio0 has also speed-fix
    - was used for debugging, some resistors are replaced instead of stacked during modding
- 1191023: with boot-fix, faster essential gpio, stabile current-meas, stabile V_IO
    - 3v3 is a bit off with 3.275 V
- 1191025: with boot-fix, faster essential gpio, stabile current-meas, stabile V_IO
- 1191027: with boot-fix, faster essential gpio, stabile current-meas, stabile V_IO
    - 3v3 is a bit off with 3.286 V
- 1191029: boot-fix, stabile V_IO

Debug-Investigation on 1191022
------------------------------

- BB still fails to boot when P8-41to44 are connected to cape -> lines are separated by a analog switch?!?
    - switch is powered by L3V3 ?!?
    - drilling out the via above the switch and routing enamel-wire from capacitor of switch to 3V3-Source
    - BB is booting!
- current-readout is very noisy
    - add 470 nF over shunt, to get 570 nF -> much better, Lowpass changes from 796 kHz to 140 kHz
        - this cap is bad idea!
    - 2 V rising stable in 6 us, falling in 10 - 16 us
    - add 1 nF over feedback-cap, to get 2 nF -> no Large Effect
    - TODO: switch back to small feedback loop without switch?
- GPIO-Edges -> BB - 1 k - 10 k PU, [33 R PRU] - LSF - 1 k - 10 k PU, Switch - TA
    - baseline test
        - BB-Source Low takes 50 ns from 3.3 to 0 V
        - TB-Receiv Low takes 2-3 us from 2 to 0.8 V
        - PRU-Recv  Low take 300 ns from 3.3 to 0 V
        - BB-Source Hi takes 100 ns to 3.3 V (100%)
        - TB-Receiv Hi takes 20 us from 0.8 to 2 V
        - PRU-Recv  Hi takes 800 ns from 0 to 3.3 V
    - -> try 2x 300 R Series Resistance, @5V only slightly above (8.3mA) current-limit of BB-Pins
        - 330 R || 1k = 248 R, 430 || 1k = 301 R
        - BB-Source Low 60 ns, High 80 ns
        - TB-Recv   low 1 us, Hi ~ 20 us
        - PRU_Rec   low 100 ns + 700 ns, Hi 400 ns
        - signal on target side between seriesRes and Switch is similar to target-output
        - signal on sys side between seriesRes and LSF is slower (400 ns rise instead of 50)
        - RefA = 0.961 V, RefB = 1.526 V -> fet-diode = 565 mV
    - lower RefB Resistor from 240k to 200k
        - TB-Recv   low 1-1.5 us, high 15-20 us
        - RefA = 1.053 V, RefB = 1.611 V -> fet-diode 558 mV
    - PU on both sides lowered from 10k to 2.1k, (= 2.7k || 10k)
        - TB-Recv   low ~< 1 us, Hi 3-5 us
    - other ideas?
        - lower PU on both sides at least for uart & programming -> 2.1 k seem to do the trick
        - capacity of line?
        - remove sys-series-resistor
        - disconnect pru-side
TODO: look for voltage-spikes on coils when turning off power


Mods for HWv2.2
-----------------

- analog switch to pru
    - drill out via with <1mm drill, first layer is enough, trace from IC to Cap should stay intact
    - route wire from cap, through mounting hole to P9-2/3 (3V3 of BB)
- fast gpio-lines for swd and uart with stronger PUs, and lower series resistance
    - target side: on lower LSF (U12),
        - 10 k PU-Array, add 2.7k in parallel to lower 4 resistors, results in ~2.1 k
        - 1 k SeriesResistor-Array, add 100 R in parallel to lower 4 resistors, results in 91 Ohm
    - sys side:
        - same treatment for PUs, above P9-16, above / between P9-18/20, above left side P9-24, above right side P9-26
        - 1 k Series-Array, add 430 R in parallel
    - LSF - 1M parallel to existing 240 k on RefB -> resulting 200 k
- stabilize current measurement
    - 22 pF to GND on amplified path, right before ADC -> 22+5 pF + 100 k -> 60 kHz
    - additional 1 nF Cap on Feedback LP, both paths
    - Terminate unused Ports with 1 uF
    - remove 100 nF parallel to shunt
- stabilize IO-Buf-Voltage
    - cut left trace between 10 R and 1 nF, add 1k

- summary: 22 additional 0402-parts, 1 removed 0402, 2 cuts, 1 enamel trace -> ~ 1 h manual work


TODO Boardchanges
-----------------

- Power Analog-Switch U30 from BB 3V3
- PUs on sys-side should also be powered by BB 3V3
- GPIO-PUs lower to 2k
- GPIO-Series lower to ~ 600 R
- emu-shunt should be stabilized with > 500 nF (and probably the others too)
- TODO: sync with mod-list
