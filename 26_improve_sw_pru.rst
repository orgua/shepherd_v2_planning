Beaglebone PRU - Code Improvements
==================================

handling PRUs (in ansible: dev_rebuild_pru.yml)::

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
