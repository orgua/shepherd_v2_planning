Requirements Refresh / Refinement 2022-06
=========================================

- more focus on a general testbed for the Internet of Things, especially:
- GPIO Monitoring -> higher min sampling frequency / guarantees, >= 5 MHz ??
- UART Monitoring (RX from Target-Side), min 461 kBaud, better 922 kBaud -> on Linux-Side or is PRU-Monitor also fine?
- lower sampling bounds should be guaranteed and known -> avoid spurious phantom signals
- Sync-Error should be lower than Clock of GPIO-Register of target

     - Example: 1 / 16 MHz -> 62 ns

- GPIO Actuation, set predefined pins, precise between nodes, resolution can be rather low (100 kHz OK), parameters:

    - t_offset (since start of measurement)
    - node(s)
    - GPIO(s)
    - State

- GPIO Actuation for Live View would be beneficial

Thoughts on Feasibility
=======================

GPIO Monitoring

- with constant voltage (only current-monitoring, no virtual source model) one PRU-Core would be idle -> custom firmware
- PRU0 handles monitoring el. current, actuating GPIOs, Sync timebase, exchange data-buffers
- PRU1 handles only GPIO-Monitoring -> busy waiting

UART Monitoring

- current design routes UART to ARM controlled Pins (Linux) and PRU (GPIO Monitoring, discrete timestamped Events)
- Linux UART RX will be tested -> we are currently stuck at kernel 4.19 but have to switch to 5.10+ eventually
- for PRU monitoring the dedicated section applies

Sync-Error

- there is still a low frequency with unknown origin (~ 0.2 Hz)
- current limits are hard to improve
    - error between nodes: +- 400 ns abs, q95% ~ +- 200 ns
    - error between local triggers: ~ +- 120 ns abs, q95% ~ +- 50 ns
- tbd: deployed cisco-switch in TUD has layer 3 routing and >doubled spec -> could improve sync

TODO
====

- implement enablers / general improvements

    - decouple GPIO-Ringbuffer from IV-Stream-Buffer -> size constraint of 16k Events per 100 ms
    - current buffer-swap implementation is not optimal, takes too much time and should be replaced by a big ring-buffer -> makes mutex between PRUs redundant

- test UART RX with kernel 4.19 / 5.10 with 461 and 922 kBaud
- fork PRU-Firmware with focus on GPIO-Speed

    - test capabilities

