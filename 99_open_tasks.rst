Current Tasks
=============

Software Short-Term Done
------------------------

-

   user/basics
   user/getting_started
   user/hardware

   user/cli
   user/calibration
   user/data_format
   user/api
   user/performance
   user/virtcap

   dev/contributing
   dev/data_handling
   dev/sysfs
   dev/gps_sync
   dev/virtcap

    tipps
    - low noise
    - low sync offset
    - security
    -

Software Short-Term TODO
------------------------

Next Steps

- test harvester & emulator
- test IO-PCB
- order shepherd 2.3d
- Shortage-Trouble
    - OPA189IDBVR -> only 6 ICs left (1 per Cape) -> date is set to march / april
    - for 6 ICs only stock for 10-15 Capes & also out of order -> should arrive in feb - july
    - AD8421BRMZ has same problem, but date is currently 2023/03
- Software-Trouble
    - last BB-ubuntu is almost 2 years old (2020-03), kernel 4.19, python 3.6
    - there are daily test-builds of debian 11.2 (bullseye) minimal, kernel 5.10, python 3.9
    - https://rcn-ee.com/rootfs/bb.org/testing/
    - probably troublesome: kernel 5.10, maybe debian itself
- naming trouble -> currently: harvesting, emulation
    - verb A: to harvest, to emulate
    - verb B: harvesting, emulating -> does not sound right to use widely
    - noun: harvest, emulation -> harvest can be noun or verb
    - object: harvester, emulator -> **try to always use this**
    - short: hrv, emu
- what are some of the performance-specs? burden voltage, rise-time emulator current
- recorder trouble
    - below 1-2 uA the voltage seems to invert (reported by SMU)
    - something seems to reverse leak current (there are only opamp-inputs with rated leaks (drain) of 2x500pA, 1x50nA, and the op-amp output
    - adc increment is 223 nA
- emulator trouble
    - can't produce 5 V with 50 mA
    - even at 0 mA the limit of 5 V is not completely on point,
    - at 50 mA around 4 V are usable without large error
    - -> seems to be fine for modern electronics
- turning cape on when on BB-USB-Power crashes the system

Ansible

- deploy roles (ptp-client & gps-client) have connman-disabler -> problem: time not synced at all
    - connmanctl seems to enable service instead of oneshot
    - solution: install ntpdate, use "sudo ntpdate -b -s -u pool.ntp.org" at boot -> systemd-oneshot-service
    - https://linuxconfig.org/how-to-automatically-execute-shell-script-at-startup-boot-on-systemd-linux
    - https://askubuntu.com/questions/814/how-to-run-scripts-on-start-up
- dont use apt for python-libs, install and update with pip

Python

- unit-tests for virtual harvester (adc and ivc)
- unit-tests for programmer
- update herd with latest command-changes -> done, todo: test
- write plausible data as cal, if module is missing -> default_cal, wrong cal can trigger a exception
- py should know about pru-state -> error if no contact can be established, same with kernel-module when sysfs is offline
- nicer exit -> improve exception handling and use proper exit
- newest h5py-Version seems to hang sometimes on .close() -> profiler shouts "infinite loop"
- timesync-logging -> parse chrony for gps
- log pru-sync-progress -> report internal vars of kernel-sync-routine to sysfs
- logging -> second handler to stream into hdf5-file
- switch to one logger? all seem to are different instances
- there seem to run two (!) py shepherd launcher?
- unittest should contain option to benchmark system -> harvest / emulate, 10 min, report cpu, ram usage
- unit-test
    - vsource - low and high power inputs 72W, 1W, 195 nA * 19 uV = 3.7 pW, what is with 1fW?
    - vsource - log intermediate
    - log skip V/C/GPIO
- send stop when ending measurement (now, legacy)
- add option to test device (change DT and uEnv to allow pinaccess to UART-Pins)

PRU

- reduce pru-opt-level? most likely cause for u64-trouble. or switch to gcc

Misc

- adapt to newest PinConfig v2.3
    - also v2.1r1 update doc with new pinconfig: en_rec p9-14, en_emu p9-16
- "virtual converter" should be named "recorder"
- "virtual source" should be named "converter"
- update nrf-democode
- recorder, also software-defined:
    - constant voltage
    - mppt:
        - measure open circuit voltage, jump to XX % of that, interval for how often and how long measurement takes
        - perturb and observe -> change small increments, steps-size, interval
    - IV - curves -> window-size
- do not crash when ssh-session is terminated (logger?)
    -> use "setsid program" or "nohup program" and an "&" at the end to remove dependency
    - nohup can even redirect the outputs to a file
- known issue: after several testbench-runs the emulate-tests hang in main-loop, there are more buffers returned than allowed
- emulation seems to run longer than wanted: duration=180 produces file with 186.2 s traces
- google-doc milestones
- timing of dmesg-log in python is wrong. there are start-trigger-msgs and errors 0.1s apart (both timestamps), when bash-dmesg shows 250 s
- remove h5-file from commit 6f45b70a5cca0ce489c21c92ff891b2e54e7bed6
    - https://stackoverflow.com/questions/307828/how-do-you-fix-a-bad-merge-and-replay-your-good-commits-onto-a-fixed-merge

- fix for kai
    - file-name / auto-transfer fails, retrieve newest?
    - (fixed in v2) sheep / tasks / main / meta-package overwrites /etc/shepherd
    - (fixed in v2) add start timestamp to config in herd
    - (fixed ?) force_overwrite seems to be wrong? default not applied
    - lowPrio: include GPS / PTP - Sync - status logging in h5-file
 - ask kai
    - HW - diode shows ~ 430 nA reverse current
    - HW - what about harvest LED
    - HW - target cap: reducing from 1 us to 100 nF brings edge-response from 30-80 us down to 8-14 us -> target can buffer on its own, 10 Ohm shunt & 1 uF are responsible for 16 kHz Lowpass
    - hw - maybe add V-ADC for emu? resulting V can deviate from dac -> chips select pins could be cross-used when only rec or emu is active

DOCs

--length -l is now --duration -d ->
--input --output is now --output_path -> correct docs
--virtsource replaces vcap, is not optional anymore, maybe prepare preconfigured converters (bq-series) to choose from
         possible choices: nothing, regulator-name like BQ25570 / BQ25504, path to yaml-config
- the options get repeated all the time, is it possible to define them upfront and just include them where needed?
- ditch sudo, add user to allow sys_fs-access and other things
- default-cal -> use_cal_default
- start-time -> start_time
- sheep run record -> sheep run harvest, same with sheep record

Hardware Short-Term TODO
-----------------------------

- test cape v2.3r1
- finalize cape v2.3
- finalize target v2.3

Long-Term TODO
--------------

- WEB
- Future Work for vSource:
    - smaller error-margin / more resolution (similar to python-port): extend division-LUT
    - overhead from calc_inp_power could be moved to python, also with a cheap way to interpolate efficiency-LUT
    - interpolate LUTs -> cheapest would be to take 4 (or more) following bits of input and multiply them and the negative version with current and following LUT-Value, add, then shift right 5 bit to get mean
- harvesting - voltage-sweep
- test Link-Quality of targets over time, to specific points in time
    - map each node to each other -> ask carsten for code-sharing


Testbed - Software - Web-Interface
----------------------------------

- for global server access -> security concept needed
- measure ptp-performance with new cisco-switch
- get ptp-capable cisco-switch
- get proper wall-mounting for nodes

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
- update OpenOCD-Instance with latest patch from kai
- OpenOCD seems to poll when still active after programming -> higher IO-Traffic
- bring OpenOCD-Patches to mainline
- SpyBiWire - solution to bring it to BBone, https://forum.43oh.com/topic/10035-4-wire-jtag-with-mspdebug-and-raspberry-pi-gpio/
