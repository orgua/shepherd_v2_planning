Using a new Ubuntu
===================


Ubuntu 20.04.04
---------------

- release: https://rcn-ee.com/rootfs/ubuntu-armhf/2022-03-29/ -> bone ... console armhf
- kernel 5.10.100-ti-r40
- python 3.8
- minimal image with 2.1 GB of free space


Install Steps
-------------

- mostly: https://elinux.org/Beagleboard:BeagleBoneBlack_Debian#Flashing_eMMC
- flashing to eMMC via user-button was not active by default
- downgrade kernel (4.19.94-ti-r72):

    update-ca-certificates -f -v

    git clone https://github.com/RobertCNelson/boot-scripts /opt/scripts/
    sudo /opt/scripts/tools/update_kernel.sh --lts-4_19
    sudo reboot now

- ansible bootstrap runs
- deploy error1 for sheep/main/"install shepherd python package" -> msgpack not found
    - isolated: python3 setup.py install --force -> only showed warnings -> second time was ok
- deploy error2 for gps-host/"add shepherd rep to aptitude -> certificate is expired
    -

TODO
----

- test newest kernel 5.10.100 -> expected trouble with memory interface to pru
