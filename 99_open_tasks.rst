Current Tasks
=============

Questions for the Team
----------------------

- which Targets should be included
-

General short-term TODO
-----------------------

- converter py-impl
- test converter virtual source
- optimize converter
    - arbeitsbereich von eta definieren
    - converter mode implementieren
    - beschleunigen
    -
- add default regulators (BQ... need to be parametrized)
- fix for kai
    - file-name / auto-transfer fails, retrieve newest?
    - sheep / tasks / main / meta-package overwrites /etc/shepherd
    - add start timestamp to config
    - force_overwrite seems to be wrong? default not applied
    - lowPrio: include GPS / PTP - Sync - status logging in h5-file
- include commits from Kai
- observe hangs during test-suite-run (probably glitching due to voltage dip)
- add recorder-example as default  /etc/shepherd/config.yml (start with button)
- harvesting - voltage-sweep
- add option to test device (change DT and uEnv to allow pinaccess to UART-Pins)
- Test hw, all subelements, eeprom, ...
- hw redesign 2.1r1
- optional
    - click might be slowing down start of programs substantially
    - proper exit-handler for python
    - pru-fw - base msg system on irq, but not really needed, except for timestamping
- ask kai
    - given time of find_consensus_time() is only used for comment? sheep does not start
        - config file gets
        - sudo python3 setup.py install --force
        - shepherd-herd -vvv -i inventory/example.yml record -d 10 --no-calib
    - BQ Parametrize -> YES
    - HW - diode shows ~ 430 nA reverse current
    - HW - what about harvest LED
    - HW - target cap: reducing from 1 us to 100 nF brings edge-response from 30-80 us down to 8-14 us -> target can buffer on its own, 10 Ohm shunt & 1 uF are responsible for 16 kHz Lowpass
    - hw - maybe add V-ADC for emu? resulting V can deviate from dac -> chips select pins could be cross-used when only rec or emu is active
    - wirklich nur 20min timer?

Testbed
-------

- for global server access -> security concept needed
- measure ptp-performance with new cisco-switch
- get ptp-capable cisco-switch
- get proper wall-mounting for nodes


Hardware - mostly shepherd Cape
-------------------------------



Software - RealTime-Code
------------------------




Software - Linux, Python
------------------------

- figure out a system to bulk-initialize scenario, measurement, but also individualize certain nodes if needed
   - build "default" one and deep-copy and individualize -> this could be part of a test-bed-module-handler
      - test-bed instantiates beaglebone-nodes [1..30] and user can hand target and harvest module to selected nodes
   - shepherd herd -> yaml -> per node config
- SSH speedproblem: cpu-encryption is slow, transfer is ~ 50 MBit with 100% CPU Usage
    - Crypto-Module brings ~ 25 MBit with < 30% CPU Usage
    - ssh should allow to switch to lower crypto after handshake, maybe even something that is fast for Crypto-Module

- i2c1 is only for target-pin-header and can be disabled by default (needed for target-programmer later)
- uart1 is disabled for now (to access pins in linux)
- calibration: switching main power to both targets shows, that the routes seem to have different current-readings for the same load! odd

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
