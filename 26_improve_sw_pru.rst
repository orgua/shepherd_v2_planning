Beaglebone PRU
==================================

Getting started - handling PRUs (in ansible: dev_rebuild_pru.yml)::

    sudo su

    # stopping PRUs
    echo "stop" > /sys/class/remoterproc/remoteproc1/state
    echo "stop" > /sys/class/remoterproc/remoteproc2/state

    # stop and start kernel module -> warning: some states are not reset this way
    modprobe -r shepherd
    modprobe -a shepherd
    # fw gets flashed and PRUs started by module

    # test code on live system
    shepherd-sheep -vv run --config /etc/shepherd/config.yml


Code Improvements

    - firmware should do self-tests for its key components
        - both cores running
        - ram-interface to cpu responsive
        - dac and adc available
        - setting voltage is measurable
    - switch to gcc
    - update pru-software-support-package-5.4.0 to
        - official v5.7, or
        - gcc version https://github.com/dinuxbg/pru-software-support-package (fork of V4), with cherry-picking
