Beaglebone PRU - Code Improvements
==================================


dmesg output::

    [   60.635451] remoteproc remoteproc0: Booting fw image am335x-pm-firmware.elf, size 217168
    [   60.635726] remoteproc remoteproc0: remote processor wkup_m3 is now up
    [   60.635753] wkup_m3_ipc 44e11324.wkup_m3_ipc: CM3 Firmware Version = 0x193
    [   64.826893] PM: bootloader does not support rtc-only!
    [   65.452427] remoteproc remoteproc1: 4a334000.pru is available
    [   65.452596] pru-rproc 4a334000.pru: PRU rproc node pru@4a334000 probed successfully
    [   65.467028] remoteproc remoteproc2: 4a338000.pru is available
    [   65.467191] pru-rproc 4a338000.pru: PRU rproc node pru@4a338000 probed successfully

handling prus

    - stopping ``echo "stop" > /sys/class/remoterproc/remoteproc1/state``
    - start ...
    - reload kernel-module


