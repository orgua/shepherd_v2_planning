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

General short-term Okt
-------------------------
- searched for bottleneck when writing on flash drive
- optimized python code, more pythonic, less overhead
- try to find memory leak
- Lifted limit of click < v8
- updated h5lib

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

- PyCode-Performance
    - h5-NoCompression -    77 % CPU, 47 mb/ 30s
    - h5-lzf                89 % CPU, 24 mb/ 30s
    - loggerOpt1 - ifVerb   84 % CPU, same
    - loggerOpt2 - traceOff 83 % CPU
    - profiler1             83 % CPU
    - with monitors         91 % CPU -> tevent.wait() instead of time.sleep()
    - same w/o profiling    81 % CPU

sudo python3 -m cProfile -o profile.pstats  /opt/shepherd/software/python-package/shepherd/cli.py -vv run --config /etc/shepherd/example_config_emulation.yml
runsnake profile.pstats
results for h5py-3.4:
- 624 s total runtime
-  26 s h5.shape
-  96 s sleep
-  34 s h5.datalog.read_buffers.__getitem__
- 447 s           .write_buffers
- 184 s                         .__getitem__(h5.group.py)
- 103 s                         .__setitem__(h5.dataset.py)
- RAM-Increase 5% (24mb) in 10 min

-> asyncio.sleep or threading.Event().wait() in normal code? -> no, .wait() has small overhead
- adding Flash drive
    - power-increase from 322 mA to 387 mA (), ~590 mA (active)
    - detected as philips USB Flash Drive, high speed, usb mass storage,
    - 512-byte logical blocks 231 GiB, Mode Sense 45 00 00 00, write cache disabled, read cache enabled, doesn't support DPO or FUA
    - DPO: Disable Page out -
    - FUA: Force unit access - FUA write command will not return until data is written to media, thus data written by a completed FUA write command is on permanent media
    - run playbook "setup-ext-storage" with mod for sda1 -> fails because of "p1"-addition

sudo umount -f -v /dev/sda1
sudo mkfs.ext4 -F /dev/sda1
add to /etc/fstab:
/dev/sda1  /var/shepherd/recordings  ext4  defaults,noiversion,auto_da_alloc,noatime,errors=continue,commit=20,inode_readahead_blks=64,delalloc,barrier=0,data=writeback,noexec,nosuid,lazytime,noacl,nouser_xattr,users,noauto  0  0
sudo chmod 777 /var/shepherd/recordings
sudo mount -a
sudo mount /dev/sda1
sudo chmod 777 /var/shepherd/recordings
sudo chown hans /var/shepherd/recordings
https://www.thegeekdiary.com/what-are-the-mount-options-to-improve-ext4-filesystem-performance-in-linux/
https://www.linuxliteos.com/forums/tutorials/fast-disk-io-with-ext4-howto/
mount -t ext4 -o defaults,noiversion,auto_da_alloc,noatime,errors=continue,commit=20,\
inode_readahead_blks=64,delalloc,barrier=0,data=writeback,noexec,nosuid,lazytime,\
noacl,nouser_xattr,users /dev/sda1 /var/shepherd/recordings
- noiversion                -> no tracking of inode-modifications
- auto_da_alloc             -> avoids the "zero-length" problem
- noatime                   -> no tracking of access-time
- errors=remount-ro         -> Seems not optimal (TODO: changed to continue for now)
- commit=20                 -> number of seconds for each data and meta data sync (default=5)
- inode_readahead_blks=64   -> pre-read into buffer cache (default=32)
- delalloc                  -> Deferring block allocation until write-out time
- barrier=0                 -> Write barriers are used to enforce proper on-disk ordering of journal commits, but they will degrade the performance of the file system (default = 1)
- discard                   -> enable trim for ssd (TODO: not for our usb drive)

- data=writeback            -> data ordering will not be preserved, data may be written to the file system after its metadata has been committed to the journal (default data=ordered)
- noexec                    -> Do not allow execution of any binaries
- nosuid                    -> Do not allow set-user-identifier or set-group-identifier bits to take effect.
- extent                    -> more efficient mapping of logical blocks (TODO: seems to be no real option)
- lazytime                  -> reduces writes to inode table for random writes to preallocated files

- noacl                     -> disable access control lists (todo: is marked deprecated)
- nouser_xattr              -> disable Extended User Attributes (todo: is marked deprecated)
- users                     -> FSTAB, allows mount and umount without sudo
- noauto                    -> FSTAB, disable auto-mount
- async                     -> should already be default


sudo shepherd-sheep -vv run --config /etc/shepherd/example_config_harvest.yml
sudo shepherd-sheep -vv run --config /etc/shepherd/example_config_emulation.yml
used 600 s db_traces.h5 as input, 521 mb, 870 kb/s
-> flash drive contains source and destination, 180 s worked, 600 s failed after 293 s (run out of buffers), 224 mb
- failing because of full msg-fifo, with cpu-usage of ~ 86 %, no significant ram or nw usage
- despite of mount-option "commit=2" the data is written every ~ 20 to 30 s with peek rates of 12-21 mb/s
    - h5py-trouble? -> changed h5.driver to stdio and _nslots from 521 to 100, without success
    - smaller write cache -> worse performance (~ 230 s), but sysutil shows
        - source: https://unix.stackexchange.com/questions/292024/how-to-reduce-linux-write-buffer-for-removable-devices
        - sudo echo 5000000 > /proc/sys/vm/dirty_bytes      -> 5 mb instead of 200 ? or 20% ram-ratio -> 93 mb
        - echo 300 > /proc/sys/vm/dirty_expire_centisecs    -> 3 s instead of 30
    - bigger write cache -> no difference (~ 280 s)
        - echo 300000000 > /proc/sys/vm/dirty_bytes
        - echo 6000 > /proc/sys/vm/dirty_expire_centisecs
- just heat-throtteling? 150 mA * 5V = 0.75 W in a plastic case -> opened and cooled a stick
- usb-errors? the flash drive seems to be the troublemaker -> even on other systems it shows a wavy write-trend
- lower cpu-usage does not work (mean ~ 80 %, instead of ~86% with monitors)
- reading from mmc, writing to flash drive -> failed also

- some cleanups and optimizations for the python code
    - range(len(x)) -> enumerate(x)
    - list([]) -> [], dict() -> {}
    - allow resizing the fifo-buffer, largest value seems to be 107 (< 10k pages)
    - https://wiki.python.org/moin/PythonSpeed/PerformanceTips
    - compile h5py for beagle -> fails, see below
    - cython, numba, nuitka, pypy: https://doc.pypy.org/en/latest/faq.html
    - -> profiling
    - not needed str() casting for paths before open(), and other str() castings

- look for h5py improvements -> main load according to profiler
sudo /usr/bin/python3 -m pip show h5py -> v2.1?
sudo /usr/bin/python3 -m pip list --outdated
sudo /usr/bin/python3 -m pip install --upgrade wheel h5py -> v3.4
-> also updated numpy is giving libblas-trouble
sudo /usr/bin/python3 -m pip uninstall numpy scipy
sudo apt --reinstall install python3-numpy python3-scipy

# further update all packets
sudo /usr/bin/python3 -m pip install --upgrade click cryptography decorator distlib
# failing because of distutil greenlet: gevent platformdirs pybind11  msgpack-numpy
sudo /usr/bin/python3 -m pip install --upgrade pyyml six virtualenv zope.event zope.interface
# another distutils: xdg


sudo /usr/bin/python3 -m pip install --upgrade --force-reinstall h5py --no-binary :all:
-> still fails libhdf5.so after over 1h

h5py-compilation-cookbook from kai (slightly modded):
sudo apt-get install libhdf5-dev
sudo pip3 install --upgrade cython
ln -s /usr/include/locale.h /usr/include/xlocale.h
#sudo /usr/bin/python3 -m pip uninstall numpy h5py
#sudo /usr/bin/python3 -m pip install --only-binary=numpy numpy==1.17.5
sudo /usr/bin/python3 -m pip install --no-binary=h5py h5py
-> v3.4, created wheel filename=h5py-3.4.0-cp39-cp39-linux_armv7l.whl size=5487437
-> relativly quick, but no benefit to precompiled version

sudo /usr/bin/python3 -m pip install --upgrade --force-reinstall h5py numpy scipy
sudo apt install python3-dev gfortran libopenblas-base liblapack3 libopenblas-dev liblapack-dev libatlas-base-dev
libopenblas* liblapack*
sudo apt remove libopenblas-base  # could be the culprit that overwrites the one working and needed lib
# https://stackoverflow.com/a/34956540

Possible Memory Leak in Python
- sheep starts with 13.2 % of system memory -> after 5000 s it uses 28 % already
    - setup: 10 h input file, no output-writing for V & C & GPIO
    - mem-profiler shows asymptotic behaviour -> maybe normal lazy garbage collection depending on free ram?
''' sudo /usr/bin/python3 -m pip install pympler
https://pythonhosted.org/Pympler/muppy.html
- try tracker / muppy
- look for circular references and custom __del__()-methods
- try to avoid exception-handling as a default-strategy in mainloop -> only in shepherdio._get_msg()
    - no difference
- filedescriptors or other things without calling close() can leak -> not the case here
- tracemalloc is in stdlib -> brings no clue as mem usage and peak settle at a value
    - constant timejumps and higher cpu-usage after 30000 s or 464 of 484 mb RAM
    -
- disable some modules (logging, memread, h5pywrite, compression)
    - loglevel = 0
    - disable h5-writer & compression
    - not use click and logging (logging.getLogger(__name__).addHandler(NullHandler()))
        - rec: mem-usage is growing 11.3? to 12.9 % in 10min, 50% CPU
        - emu1: 13.0 to 13.6.. %, 22 % CPU
        - emu2: 14.1 to 15.3, 55 % CPU ?? -> why not ~80 % ?
    - also replace shared_mem.read_buffer() by random-data
        - emu1: 11.7 to 13.7 % -> ram-usage stays between
        - emu2: to 16.3 %
    - also replace .get_msg/buffer and emu.return_buffer() by dummy, also gc.collect() in between
        - untrottled run on 100% cpu
        - emu1: 11.7 to 13.7
        - emu2: 13.7 to 16.4
    - also skip hdf5-writing
        - emu1: 11.6 - 13.5
        - emu2: 13.6 - 14.6 -> improved memory - for real?
    - also skip databuffer-Class
        - e12: up to 14.8
    - reading or writing is problem? one h5py-issue mentions vlen-type
        - rec. 10.x - 12.5
    - removing lzf again
        - rec. 10.7 - 11.3
    - isolated datalogger, 25 min sim,
        - rec 5.6 - 7.9 % (seems to be maxed there), emu
        - emu 6.0 % - 16 % (after 2330 s) -> thats the bug! reading from h5py, (lzf?)


- valgrind -> too slow to work
- chap https://stackoverflow.com/questions/61288749/finding-memory-leak-in-python-by-tracemalloc-module
- fil, python memory profiler, https://pythonspeed.com/fil/docs/fil/what-it-tracks.html
    - trouble as arm is not natively supported, but github-issue for arm-macos gives a fix

sudo valgrind --tool=memcheck shepherd-sheep -vv run --config /etc/shepherd/example_config_emulation.yml
sudo valgrind --tool=memcheck --leak-check=yes shepherd-sheep -vv run --config /etc/shepherd/example_config_emulation.yml

#sudo /usr/bin/python3 -m pip install filprofiler
sudo apt install rustc
pip install git+https://github.com/pythonspeed/filprofiler.git#egg=filprofiler
fil-profile run --no-browser shepherd-sheep -vv run --config /etc/shepherd/example_config_emulation.yml
-> fails to compile for armV7 -> missing SYS_mmap2

Mods to allow testing
pru0/main.c, line99, //send_status(...NOFREEBUF
pypkg/init.py, line 626, start_time = + 25


- deploy roles (ptp-client & gps-client) have connman-disabler -> problem: time not synced at all
    - connmanctl seems to enable service instead of oneshot
    - solution: install ntpdate, use "sudo ntpdate -b -s -u pool.ntp.org" at boot -> systemd-oneshot-service
        - https://linuxconfig.org/how-to-automatically-execute-shell-script-at-startup-boot-on-systemd-linux
        - https://askubuntu.com/questions/814/how-to-run-scripts-on-start-up
- switch to one logger? all seem to are different instances
- there seem to run two (!) py shepherd launcher?
-

- do not crash when ssh-session is terminated (logger?)
    -> use "setsid program" or "nohup program" and an "&" at the end to remove dependency
    - nohup can even redirect the outputs to a file
- known issue: after several testbench-runs the emulate-tests hang in main-loop, there are more buffers returned than allowed
- prepare kernel and pru code for programming-interface
- system-profiler - https://www.linuxlinks.com/SystemProfilers/
- make compression and monitors optional
- logging -> second handler to stream into hdf5-file
- newest h5py-Version seems to hang sometimes on .close() -> profiler shouts "infinite loop"
- timesync-logging -> parse chrony for gps
- benchmark - long duration -> test memory leaks, uart-exceptions, usb-read/write-trouble
- recorder, also software-defined:
    - constant voltage
    - mppt:
        - measure open circuit voltage, jump to XX % of that, interval for how often and how long measurement takes
        - perturb and observe -> change small increments, steps-size, interval
    - IV - curves -> window-size
- google-doc
- emulation seems to run longer than wanted: duration=180 produces file with 186.2 s traces
- timing of dmesg-log is wrong. there are start-trigger-msgs and errors 0.1s apart (both timestamps), when dmesg shows 250 s
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
    - speed up python (quick and easy):  remove compression from individual h5-datasets
    - speed up python (cython): datasteam from memory-carveout to hdf5-file should be ported to cython (seems to be possible)
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
