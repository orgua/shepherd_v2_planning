Current Tasks
=============

Questions for the Team
----------------------

- which Targets should be included
-

General short-term July
-----------------------

- converter py-impl
- test converter virtual source
- kai feedback
    - powergood hyterese, 3 / 2.4
    - init < storage enable threshold, TEST
- optimize converter, speed up
- observe hangs during test-suite-run (probably glitching due to voltage dip)
- OpenOCD, Verdopplung des speedcoeff (230k auf 500k) in /usr/share/openocd/scripts/interface/beaglebone.cfg bringt Erfolg mit etwa 370 kHz clock!

General short-term August
-------------------------

- update ubuntu-repo
- allow old file-behaviour (rec.h5, rec1.h5, ..)
- start-power (some target charge-up-period)
- extend converter
    - has_boost -> allow direct control
    - LUT_input_mins
    - LUT_output_min
    - log_capacitor
    - V_input_limits
    - remove C_output_nF
- py-converter-defaults (based on, complete with ..)
- define BQs from kai and boris
- optimize converter
    - arbeitsbereich von eta definieren
    - converter mode implementieren
- make traces optional
    - for voltage (alternative cap-voltage)
    - for current (alternative cap-current -> trouble with unsigned container -> only outflowing cap-current?)
    - no gpio or maybe custom mask
- VSource standard-values should be neutral, as if that unit is not present
- allow fast sampling in debug mode
- redo calibration with fast sampling
- DAC-Voltage in trace is 2V, but gets written as 1.5V, is calibration-value wrong? -> downsampling-bug
- definition of experiment / converter could all be done in one YML
- harvest file should be named harv, not rec -> already done? emu for emulation is already set

General short-term Sept
-------------------------

- lots of testing
- output v_intermediate on channel2 for debug -> make permanent
- merge latest patches from legacy / kai, up to 12.09.21
- connman sets time every 15min, as long as connected to internet. is that happening all the time?
    - DBus config -> only manual timeUpdate -> playbooks -> made by kai
        - changes /var/lib/connman/settings -> adds TimeUpdates=manual -> stays after boot, lets time freeze when powered off
    - source: https://www.toradex.com/community/questions/926/disable-automatic-manipulation-of-clock-linux-coli.html
    - sync.d is already in playbook
- updated pipenv
    - merged dependabot, but it removed greenlet, h5py, gevent, future, dbus-python, click, click-config-file, msgpack, python-periphery, pyzmq, zerorpc,
    - did it by hand, added
- custom openOCD, config, ... is not installed by playbooks -> separate for now "setup_openocd.yml"
    - SWD Pins are I2C1, are colliding with default dt-driver in uEnv.txt -> /lib/firmware/ holds a i2c2-00A0.dtbo
    - i2c1 can be disabled, i2c-0/2 are still there
    - reduced programming speed in config
- GPIO-Sampling should include Bat-OK (doesn't it?`), and stop sampling when voltage is off or below a certain threshold
- h5-writing updated
- extend Logging
    - Proper Uart Logging, either pyserial in 0.01s window or external grabserial started by herd
    - log sync-state
    - log sys-values: cpu, ram, dmesg, temp, io, network
- characterize noise, 10 voltages, 10 currents, 1s each

Software Short-Term TODO
-----------------------

- logging-module of python has serious performance impact -> 4*10 msg/s in debug are >20 % overhead on BB
    -> follow https://docs.python.org/3/howto/logging.html#optimization
    - avoid assembling these 4 most critical fast-Strings
        - __init__.py/emulator.return_buffer(), external verbose
        - datalog.py/LogReader.read_buffers(), generator with internal verbose -> good enough
        - shepherd_io.py/ShepherdIO.get_buffer(), external verbose
            - SharedMem.read_buffer(), external verbose & GPIO-Msg disabled
    - try to avoid collection of useless data (thread,process,_srcfile)
    - warn in yamls about impact of verbose>2
- logging -> second handler to stream into hdf5-file

- timesync-logging -> parse chrony for gps
- benchmark - long duration -> test memory leaks, uart-exceptions, usb-read/write-trouble
- recorder, also software-defined:
    - constant voltage
    - mppt:
        - measure open circuit voltage, jump to XX % of that, interval for how often and how long measurement takes
        - perturb and observe -> change small increments, steps-size, interval
    - IV - curves -> window-size
- google-doc

- remove h5-file from commit 6f45b70a5cca0ce489c21c92ff891b2e54e7bed6
    - https://stackoverflow.com/questions/307828/how-do-you-fix-a-bad-merge-and-replay-your-good-commits-onto-a-fixed-merge
- update OpenOCD-Instance with latest patch from kai
    - OpenOCD seems to poll when still active after programming -> higher IO-Traffic
    - bring OpenOCD-Patches to mainline
    - SpyBiWire - solution to bring it to BBone, https://forum.43oh.com/topic/10035-4-wire-jtag-with-mspdebug-and-raspberry-pi-gpio/
- usb-writing seems to fail, maybe due to latency? even reading of h5-file seems to fail (problem with h5lib?)
- benchmark h5-variations, 10mins for various versions (compression, full write and read,

- exception handling
- nicer exit
- update py-packets, improve speed, solve USB-Issue (see 29_improve_sw_performance.rst).
- kai-report: buffer or sysdisk overflow after ~1h even when writing on separate disk
- reduce pru-opt-level? most likely cause for u64-trouble. or switch to gcc
- kai feedback: powertrace + harvesting-firmware on nRF (LED + bLE-packet)
- unit-test
    - vsource - low and high power inputs 72W, 1W, 195 nA * 19 uV = 3.7 pW, what is with 1fW?
    - vsource - log intermediate
    - log skip V/C/GPIO
- send stop when ending measurement (now, legacy)
- fix for kai
    - file-name / auto-transfer fails, retrieve newest?
    - (fixed in v2) sheep / tasks / main / meta-package overwrites /etc/shepherd
    - (fixed in v2) add start timestamp to config in herd
    - (fixed ?) force_overwrite seems to be wrong? default not applied
    - lowPrio: include GPS / PTP - Sync - status logging in h5-file
- Test hw, all subelements, eeprom, ...
- hw redesign 2.1r1
    - update doc with new pinconfig: en_rec p9-14, en_emu p9-16
- update nrf-democode
- add option to test device (change DT and uEnv to allow pinaccess to UART-Pins)
- optional
    - "click" might be slowing down start of programs substantially
    - proper exit-handler for python
    - pru-fw - base msg system on irq, but not really needed, except for timestamping
- ask kai
    - given time of find_consensus_time() is only used for comment? sheep does not start
        - config file gets
        - sudo python3 setup.py install --force
        - shepherd-herd -vvv -i inventory/example.yml record -d 10 --no-calib
    - HW - diode shows ~ 430 nA reverse current
    - HW - what about harvest LED
    - HW - target cap: reducing from 1 us to 100 nF brings edge-response from 30-80 us down to 8-14 us -> target can buffer on its own, 10 Ohm shunt & 1 uF are responsible for 16 kHz Lowpass
    - hw - maybe add V-ADC for emu? resulting V can deviate from dac -> chips select pins could be cross-used when only rec or emu is active


Hardware Short-Term TODO
------------------------

- target-mod: msp430 + msp, spi + 2+ handshake-lines, same gpio access,

- Pwr-by-BB does not work with current cape-revision -> just add a switch?
- optimize filters with noise-metrics
    - possible tradeoffs: speed of voltage-transitions, compensation of analog switch resistance
- GPIO-Speed
    - BugFlap uses different schematic and has faster transitions
    - alternative: switchable direction for group of level translators, 2x2 configurable, 5 static input

- decide if rec & emu should be combined
    - more complex design
    - always complete package
    - reduced cost (~ 3*9 €)
    - emu gets voltage-measurement for free
- finalize hardware (WD, filters, GPIO-Speed, current bugs)
- possible extension of target port
    - programming pins are exclusive and don't have to be recorded/monitored -> free pins should be used for additional gpio
    - a second target (with option of programming) would help for some usecases (MSP430 + nRF-Radio)
        - var1: analog switch on target-pcb for programming lines controlled by one of the gpio (exclusive or could still be used as gpio)
        - var2: analog switch on cape, 2x2 programming lines on target-port
        - var3: intermediate uC on target-pcb for programming targets talking with BBone over programming lines (very custom solution but cape is left untouched similar to var1)
- target -> add target powered LED to burn away energy (or use second LED for that purpose)
- Essential changes to discuss
    - combination of rec & emu -> see HW
    - extension to target-port
- test harvesting-target
- get target A/B/1/2 straight. it is target 1/2 from now on!
- find reason for 2.3mA Offset
- ADC seems to act up sometimes after sheph-EN -> test in PRU, reenable a couple of times -> seems to be fixed with EN
- diodes for coils if needed
- LED of PRU: dedicated pwr_good / harvesting
- Board does not start when powered by BB (with extra Cap) -> extra switch needed? Not even Starting without Jumper? BootPins-Trouble Again?

Long-Term TODO
--------------
- WEB
- Future Work for vSource:
    - smaller error-margin / more resolution (similar to python-port): extend division-LUT
    - overhead from calc_inp_power could be moved to python, also with a cheap way to interpolate efficiency-LUT
    - interpolate LUTs -> cheapest would be to take 4 (or more) following bits of input and multiply them and the negative version with current and following LUT-Value, add, then shift right 5 bit to get mean
- harvesting - voltage-sweep


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
