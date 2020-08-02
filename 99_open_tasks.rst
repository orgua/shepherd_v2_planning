Current Tasks
=============

Questions for the Team
----------------------

- which Targets should be included
-

Testbed
-------

- wait for ZIH-Answer regarding rules, (hw) requirements
- when ZIH has vLAN ready: test if infrastructure of university is sufficient, mostly regarding ptp
- for node-distribution
    - talk with the leaders of groups that occupy offices
    - examine offices with IT-Admin
- measure link quality around cfaed-floors
- for global server access -> security concept needed
- distribution - git for debian package seems possible -> https://wiki.debian.org/GitPackaging

Hardware - mostly shepherd Cape
-------------------------------

- target-relays/switches : multi-pin, low leakage, high data-rate
    - current uni-direction (gpio) -> SN74LV4T125PWR -> are diodes needed?
    - current bi-direction (uart, swd) -> TXB0304RUTR
    - optimal specs: v_in & v_ref_a & v_ref_b (3 separate levels), IO-Ports
- power-switches: low leakage
- level-changer: high speed, low-power, possible combination with switch / programmable
- find large pin-count gpio-switch (target-selector)
- is there a better power-path?
  - find reason for substractor (EMU-I)
  - why is uni-dir level switcher not on vdd-target -> it could get into undefined state
- draw digital version of float chart for power-stage
   - where is V_CREF coming from, or is it flowing backwards from VOC_SAMP?
   - is there a possibility that (CV)-LDO drives against MPPT-Converter in a unwanted state?
- test accessing GPIO Periphery via PRU, register address
- look at https://github.com/cdsteinkuehler/beaglebone-universal-io
- some routine is driving gpio on boot -> input kai: not uboot

Software - RealTime-Code
------------------------

- does beaglebone AI with TI AM5729 offer more pins for PRU? https://www.ti.com/product/AM5729
- find a better name for vCap, like vEH, vPwr
- try to access host gpio peripheral via pru -> would make pin-doubling redundant
- try to benchmark the loop (debug-pin-high when processing)
- check out other testbeds
    - tracelab 200 ns accuracy - https://pub.tik.ee.ethz.ch/people/rlim/LMDBT2015.pdf
- GIT, for Kai
    - make PR for shepherd1 with fixes
    - is dev-branch in shepherd1 important? two pins are swapped, and some scripts refined
    - where is python-periphery v2 reacting wrong? can we work around it? character device VS sysfs
        - device tree allows to define standard behaviour of pins

Software - Linux, Python
------------------------

- figure out a system to bulk-initialize scenario, measurement, but also individualize certain nodes if needed
   - build "default" one and deep-copy and individualize -> this could be part of a test-bed-module-handler
      - test-bed instantiates beaglebone-nodes [1..30] and user can hand target and harvest module to selected nodes
   - shepherd herd -> yaml -> per node config
- SSH speedproblem: cpu-encryption is slow, transfer is ~ 50 MBit with 100% CPU Usage
    - Crypto-Module brings ~ 25 MBit with < 30% CPU Usage
    - ssh should allow to switch to lower crypto after handshake, maybe even something that is fast for Crypto-Module

Software - OpenOCD
------------------

- check for compatibility jtag, swd, spy-by-wire to new target ICs (eventually tunneled through PRU)
   - nRF52 (DFU / USB, SWD)
   - STM32L4 (SWD)
   - MSP430, MSP432, CC430 (JTAG, Serial, USB, Spy-By-Wire)
- currently not routed through PRU, just normal beagle-GPIO
- bring https://github.com/geissdoerfer/openocd/commits/am3358gpio mainline
    - git https://sourceforge.net/p/openocd/code/merge-requests/?status=open
    - gerrit http://openocd.zylin.com/#/q/status:open


Software - Web-Interface
------------------------

- security concept needed if interface should be globally accessible
