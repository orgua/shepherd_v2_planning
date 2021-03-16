Shepherd - Concept
==================

Overview
---------
- (mobile) testbed for batteryless IoT
- observer-nodes for an IoT-Target
- works autonomous or time-sychronized with a network backplane
- software defined power source, emulation of
    - harvesting source (pre-recorded, simulated)
    - regulator / converter - circuit
    - intermediate storage-capacitor
- allows to experiment with emulated spatio-temporal energy availability
- recording of energy-traces -> key-parameters like current-drain and (virtual) capacitor-voltage
- additional functionality: recording of harvesting sources (not part of testbed)

Nodes
-----
- embedded linux board with shepherd-cape
- time critical code runs on two real-time processors
- two targets-ports are available
    - both can be supplied with individual voltages, only one is current-tracked
    - general purpose IO, target selection independent from power-supply-selection
    - separate 3V3 line
- bidirectional GPIO on 10 channels, 2x2 lanes are currently reserved for SWD / Spy-by-Wire, UART
- Targets (currently planned)
    - nRF52840
    - MSP430

Testbed
-------
- 30 Nodes on one floor in a university office-building
- nodes powered via POE
- (optional) one PTP-Masterclock, Node with GPS
- 1 Ubuntu Control-vServer, 10 TB of additional Storage
- 1 experiment at a time, no concurrency
- Web-Framework
    - user-management (roles for admins and users)
    - experiment-management, configure and control, add data (see below)
    - experiment-scheduling, calender (set active, start-time, duration)
    - data management / quota (retrieve / delete recordings)
    - authentication via external services
    - E-Mail notifications
    - testbed status, topology
    - (optional) grafana visualisation of recorded data
    - (admins) server status, quota, testbed control
    - documentation and instructions
- user-provided data (experiment management)
    - (optional) energy-traces, IV-Curves
    - regulator / converter-config
    - target-firmware
    - (optional) python userspace script that interacts with gpio / serial

Technical details
-----------------
- target-voltage 0 to 4.5 V, max 50 mA per Target
    - 100 kHz sampling rate, jitter max +- 90 ns, 95% Quantile is 60 ns
    - 18 bit ADC, LSB results in 19.1 uV or 191 nA
- low noise & high precision design for analog frontend
- 10 shared GPIOs with system
    - bidirectional
    - level translation works from ~ 1.3 to 5 V
    - recording: sampling rate asynchronous between ~ 1 to 5 MHz
    - data throughput untested, but edges look OK for > 1 MBaud
    - leakage during operation < 2 uA from target-side
    - gpio can be turned of, < 10 nA leak from target-side
- data-rates
    - 1 min ~ >= 54 MiB of measurement data (more with heavy GPIO actions)
    - 1 Hour, 30 Nodes -> 100 GiB uncompressed (hdf5)
- time-synchronization
    - in linux via PTP,
    - chip-select edge of two test-nodes have a maximum jitter of about +- 300 ns, 95% quantile is 160 ns
- external watchdog for wakeup / restart on
- network
    - Server has 10 GBit Link to Switch
    - Nodes have 100 MBit Link to Switch
