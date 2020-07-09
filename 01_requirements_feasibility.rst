Feasibility of Requirements
===========================

Unsolved, not mentioned Details
-------------------------------

- Testbed, TODO
   - Infrastructure of university sufficient and usable? ethernet-ports, power-sockets, ptp over ethernet-switch-cascade
   - how to get server from ZIH
   - what about interference with office WIFI -> rules and constraints of ZIH / university
   - is it possible to put the nodes in cable canal
- Hardware
   - nodes powered and controllable via POE
   - how to control distant long-Range-Nodes
      - mobile network for control backchannel, or just scheduled via pre-configuration
   - Cape-ID or Node-ID could be coded in hardware (Resistor-bridges would be human readable, flashstorage can also contain calibration-data
   - variable TX-Power → is it enough to change firmware or do we need attenuation
- Software
   - how dynamic do Nodes have to react on current environment (network access, gps attached)
      - i.e. system start → look for GPS and network → decide which role is used


Emulation of Capacitor / DC-Converter
-------------------------------------

- Problem: PRU of beaglebone black is currently already quite occupied with measuring and replay of energy-trace, emulation means real time control loop, the PRU has limited capability for that (no division, ...)
- Enabler 1: keep previous hw-design (fall-back), but add switches to bridge converter and cap (one additional pin - does not need to be connected to PRU)
- Improvement 1: optimize PRU-Code, i.e. bitbanging of SPI
- Improvement 2: current beaglebone AI offers two PRU and 2x dual-arm-cortex-M4 cores (price is 122 € instead of 60 €)
- Improvement 3: try to find approach where same cape-pinout can be used with BB black and BB AI
- assessment:
   - mostly critical for software implementation
   - -> hardware enabled approach, not difficult in hardware, low risk and low impact on time expense

Accuracy of time-base
---------------------

- Problem: jitter on gpio-traces from different nodes
- Improvement 1: use ethernet switches with ptp-support, QoS and GPS-Interface
- Improvement 2: GBE of BB AI could bring advantage (faster processing in stack / switch, stricter timing constraints)
- Improvement 3: change crystal oscillators of BB to temperature compensated ones (lower PPMs for drift and aging). Oven controlled crystals would be to big
- Improvement 4: external sync port is already available for the gps-capelet, even if it is not used for time-keeping, it can be recorded for later trace-alignment
- assessment:
   - no definitive solution for sub 1 µs accuracy, but some of the solutions should be considered in concept phase, others are sw / hw mods in a later stage
   - no risk on hw-level, minimal more time expense in design-stage

Mobility of Nodes
-----------------

- Problem: node presumably without network access and gps-reception, not powered all the time
- Improvement 1: allow external gps-antenna (not possible for current ublox SAM M8Q / 22 €)
- Improvement 2: offer backup power to gps module, small LiPo or supercap
- Improvement 3: offer software based scheduling and pre-config of measurements on nodes
- Improvement 4: offer a robust power-connection
- improvement 5: tweak linux for low power usage (turn off unused devices)
- improvement 6: proper casing with interfaces (i.e. eth, power-switch/connector, gps-antenna, pps)
- assessment:
   - low risk on hw-level

Support for other Targets
-------------------------

- Problem: different µC need various programmers
- Info: Flocklab and D-Cube support nRF52 (DFU / USB, SWD), STM32L4 (SWD), MSP430 / 432 & CC430 (JTAG, Serial, USB, Spy-By-Wire)
- Enabler 1: generalize programmer pins and GPIO-Pins to Target (specialize on target-carrier-pcb)
- Enabler 2: bring usb to target device if possible (BB-Pinheader does not have USB, but could be realized via cable)
- assessment:
   - TODO, but seems viable

Support for two selectable Targets
----------------------------------

- Problem: gpios with PRU support are limited
- enabler 1: switching of targets by BB (not PRU-Pins)
