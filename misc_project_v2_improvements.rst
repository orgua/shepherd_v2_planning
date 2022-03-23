General Shepherd-Description
----------------------------

**About Shepherd v1.x (from git)**

shepherd is a testbed for the batteryless Internet of Things, allowing to record harvesting conditions at multiple points in space over time. The recorded data can be replayed to attached wireless sensor nodes, examining their behaviour under the constraints of spatio-temporal energy availability.

**About Shepherd v2.x**

- previous description is still correct, in detail:
    - embedded linux board with analog frontend serves as a shepherd node
    - harvesting-circuit can record an energy trace from a energy-source like solar, thermoelectric, ...
    - emulation-circuit replays the energy-trace for a real target (user programmable uController) and records the drawn energy
- v1 is build around a BQ25504-IC (plus capacitor) as harvester for recording and emulating various environments -> good approach, but limited by design:
    - MPPT-controller is slow to react on changing environmental conditions by design (check every 16s with 64 ms downtime)
    - (VOC-)mppt-controller is fairly simple with pre-set setpoint (e.g. 76 % of open-circuit voltage for solar cells)
    - recorded harvest-environment is specific to harvest-IC + configuration
    - setup / configuration (especially) with storage cap is fairly static (combination of MPPT-Controller, Boost-Converter, Cap)
- v2 improves the project by generalizing the basic idea and therefore virtualizing the harvester, storage capacitors and voltage converters
- by switching to a software defined / virtual harvester-system and power-source the disadvantages from v1 vanish, with further advantages
    - full customization per config-parameters (e.g. boost-voltage, capacitor size, ...) -> currently 10 parameters for the harvester and 29 parameters for the converter-stage
    - harvesting-recorder has already several strategies implemented: constant voltage (CV), MPPT based on open circuit voltage or perturbe & observe
    - harvesting can also be postponed by recording iv-curves from the energy-source
    - emulation handles harvested energy-traces or harvests directly from the iv-curves and simulates a customizable converter-stage (pic: https://github.com/orgua/shepherd_v2_planning/blob/master/32_virtual_source_schemdraw.png)
    - power-stage has already predefined templates for several setups:
        - direct throughput of traces
        - simple diode + capacitor
        - buck-boost-converter (e.g. BQ25570) including the power-good-signal and efficiencies of underlying converters
        - buck-converter (BQ25504)
    - the design enables users to automate testing of harvesting-setups e.g. by sweeping through parameters like storage-cap-size
- the emulator and harvester are consisting of a purpose-fully chosen combination of low-noise and high-speed DACs, ADCs and Instrumentation-Amplifiers
    - both circuits can handle 0 - 4.7 V (hrv even 5.0V) with up to 50 mA current
    - resulting resolution, step size is ~ 200 nA and 80 uV for voltage and current
- the software-implementation updates in real time with 100 kHz

- general improvements for shepherd beside the virtualization
    - synchronization of sampling-trigger for node network optimized from ~ 2.4 us to under 500 ns
    - jitter of sampling trigger improved from about +- 600 ns to under 100 ns
    - 9 GPIO-Channels between target and system monitored with 2.5 - 5.5 MHz sampling-rate (previous ~ 160 - 500 kHz, with 6 GPIO)
    - two target-ports available, emulator can choose
    - watchdog to handle hangups during unsupervised operation
    - one default target with a nrf52-module

- near future
    - advanced target with msp430 (with FRAM) and nrf52 for various configurations: only 1 uC active, msp as processor and nrf as radio, nrf as processor+radio and msp as low-energie storage
    - combined network of shepherd nodes as iot-testbed with web-based control
