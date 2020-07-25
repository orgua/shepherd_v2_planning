ansible-playbooks
-----------------

bootstrap
    - "Set authorized key from local file" -> script stops, no ssh pub key generated before trying to access it, on host!
        - give better error message
        - fix: ssh-keygen
    - remove ubuntu-default-user
    - why "ansible_become_password", what is the meaning? script sets no pw when creating new user
    - user should add (maybe)
        generate_ssh_key: yes
        state: present

General	
    - playbook workflow - why "changed", and not all "ok"
    - when is deploy needed? -> better document all scripts
    - is there a way to accelerate ansible?
    - can bash-out be saved to file?
    - how do we see if install is fine? -> journalctl -u shepherd
    - image could be run virtually

System Feedback
---------------

BBB Leds
    - USER0 is the heartbeat indicator from the Linux kernel.
    - USER1 turns on when the SD card is being accessed
    - USER2 is an activity indicator. It turns on when the kernel is not in the idle loop.
    - USER3 turns on when the onboard eMMC is being accessed.

BBB Readme
    - up to date system information https://elinux.org/Beagleboard:BeagleBoneBlack_Debian
        - updating kernel
        - new device tree interface
        -


System improvements
-------------------

Downgrade kernel (for now)::

    sudo apt install linux-image-4.14.108-ti-r136, linux-headers-...
        currently installed 4.19.94-ti-r36
        -> rt-kernel is possible, but A: not needed, B: bad for performance
        last updated bb-cape-overlays
    sudo apt list --installed | grep linux-  -> remove other

Upgrade Kernel::

    cd /opt/scripts/tools/
    sudo git pull
    sudo ./update_kernel.sh --lts-5_4       -> warning: does not work for BBB yet, just update to latest 4.19 release by ommiting --lts..
    sudo reboot

    sudo apt-get install linux-headers-`uname -r`

Update Bootloader::

    sudo /opt/scripts/tools/developers/update_bootloader.sh
    reboot

Storage Information::

    # reference: https://learn.sparkfun.com/tutorials/single-board-computer-benchmarks
        BBB-revC, write 10 MB/s, read 27 MB/s
    
    sudo blockdev --getbsz /dev/mmcblk1p1
        blocksize on eMMC and uSD is 4096 byte

    sudo cat /sys/kernel/debug/mmc1/ios | grep "bus width"
        -> should be 8 bits for mmc1/eMMC and 4 bits for mmc0/uSD
        # https://groups.google.com/forum/m/#!topic/beagleboard/fOGeXCub9OY

Storage benchmark::

    dd if=/dev/zero of=./testfile bs=4096 count=40000 oflag=direct
        eMMC-w  5.6 MB/s, sda-w  5.6 MB/s, uSD-w  2.3 MB/s
    dd if=/dev/zero of=./testfile bs=100M count=1 oflag=direct
        eMMC-w 21.1 MB/s, sda-w 26.0 MB/s, uSD-w 17.7 MB/s
    dd if=/dev/zero of=./testfile bs=100M count=1
        eMMC-w 55.4 MB/s, sda-w 26.2 MB/s, uSD-w 39.3 MB/s

- explanation: uSD is a samsung evo plus 128 GB, sda is same uSD with a fast card reader via usb
- note: sd is only in 4bit-bus-mode
- learning: external USB seems to be the better choice for data storage,

SSHd improvement::

    sudo nano /etc/ssh/sshd_config
        UseDNS no           -> disable dns lookup on server side
        Compression no      -> default is "delayed" after login

    # Client side: use ipv4, one single tcp-connection (controlMaster auto) on Client-side

OpenSSL Benchmark::

    time openssl speed -evp aes-128-cbc

    -> Benchmark of disabled module is ~3s
        Doing aes-128-cbc for 3s on 16 size blocks: 5618835 aes-128-cbc's in 2.94s
        Doing aes-128-cbc for 3s on 64 size blocks: 1886183 aes-128-cbc's in 2.98s
        Doing aes-128-cbc for 3s on 256 size blocks: 517655 aes-128-cbc's in 2.98s
        Doing aes-128-cbc for 3s on 1024 size blocks: 132735 aes-128-cbc's in 2.97s
        Doing aes-128-cbc for 3s on 8192 size blocks: 16702 aes-128-cbc's in 2.99s
        Doing aes-128-cbc for 3s on 16384 size blocks: 8359 aes-128-cbc's in 2.98s
    -> Benchmark of enabled is <<1.00s (CPU-Time)
        Doing aes-128-cbc for 3s on 16 size blocks: 410104 aes-128-cbc's in 0.38s
        Doing aes-128-cbc for 3s on 64 size blocks: 348184 aes-128-cbc's in 0.28s
        Doing aes-128-cbc for 3s on 256 size blocks: 37545 aes-128-cbc's in 0.02s
        Doing aes-128-cbc for 3s on 1024 size blocks: 25658 aes-128-cbc's in 0.01s
        Doing aes-128-cbc for 3s on 8192 size blocks: 5663 aes-128-cbc's in 0.01s
        Doing aes-128-cbc for 3s on 16384 size blocks: 4040 aes-128-cbc's in 0.01s

Add Driver for Crypto-Module of CPU::

    # compile and add Cryptodev module / https://github.com/cryptodev-linux/cryptodev-linux
    # Manual1: https://lauri.võsandi.com/2014/07/cryptodev.html
    # Manual2: https://datko.net/2013/10/03/howto_crypto_beaglebone_black/

    cd /usr/local/src/                    -> TODO: rethink that, it forces sudo on make, not good practice
    sudo wget https://github.com/cryptodev-linux/cryptodev-linux/archive/cryptodev-linux-1.10.tar.gz
    sudo tar zxf cryptodev-linux-1.10.tar.gz
    cd crypt...
    make
    sudo make install
    sudo depmod -a                        -> register
    sudo modprobe cryptodev               -> insert
    lsmod                                 -> check, /dev/crypto now available
    add cryptodev to /etc/modules         -> permanent
    sudo sh -c 'echo cryptodev /etc/modules'

Force OpenSSL to use Crypto-Module-Hardware (TODO: hard-coding openSSL-Version is stupidly unsecure)::

    # Check active OpenSSL Version
    apt list --installed | grep openssl   -> check current version
    openssl engine -t -c                  -> should contain devcrypto
    openssl version -f                    -> should list -DHAVE_CRYPTODEV -DUSE_CRYPTDEV_DIGESTS

    # Check what ssh & sshd is using
    wheris -u sshd                         -> /usr/sbin/sshd
    ldd /usr/sbin/sshd
        libcrypto is part of openssl
       -> installed is /lib/arm-linux[...]/libcrypto.so.1.0.0 with 2 year old openSSL 1.1.1 (NOT current 1.1.1g)
       -> current is /usr/local/lib/libcrypto.so.1.1

    # compile openSSL with cryptodev-support
    # Manual: https://wiki.openssl.org/index.php/Compilation_and_Installation

    cd ~/
    wget https://www.openssl.org/source/openssl-1.1.1g.tar.gz
    wget -O openssl.tar.gz https://github.com/openssl/openssl/archive/OpenSSL_1_1_1g.tar.gz
    tar zxf openssl.tar.gz  -> TODO: still unpacks to full name with version nr.
    cd openssl...
    ./config -DHAVE_CRYPTODEV -DUSE_CRYPTODEV_DIGESTS shared enable-devcryptoeng no-sse2 no-com --openssldir=/usr/local/ssl
    perl configdata.pm --dump
    make clean
    make                                   -> TODO: this takes ~33min
    sudo make install_sw                   -> will be in /usr/local/bin

    # ubuntu has a strange behaviour: local/bin is used, local/lib gets ignored, so dirty fixing it
    -> add "/usr/local/lib" as first active line in /etc/ld.so.conf.d/arm-gnueabihf.conf

    # /etc/ssl/openssl.cnf                  -> TODO: maybe add/uncomment crypto in [engine]-section, seems not to be needed

    # Problem: new openSSL gives us libcrypto.so.1.1. but sshd demands libcrypto.so.1.0.0
    cd /usr/local/lib
    # sudo ln -s libcrypto.so.1.1 libcrypto.so.1.0.0
    # sudo shutdown -r now
    # sudo cp libcrypto.so.1.1 libcrypto.so.1.0.0
    -> symlinks and copy do not help, sshd relies on old version

    # bypass: compile old version of libcrypto.ssl of openssl, could fail for ssh because of ABI-changes
    # readme: https://github.com/openssl/openssl/issues/4597
    cd ~/
    wget https://github.com/openssl/openssl/archive/OpenSSL_1_1_1.tar.gz
    tar zxf OpenSSL_1_1_1.tar.gz
    cd OpenSSL
    ./config -DHAVE_CRYPTODEV -DUSE_CRYPTODEV_DIGESTS shared enable-devcryptoeng no-sse2 no-com --openssldir=/usr/local/ssl
    make build_generated && make libcrypto.a
    sudo make install_sw

    TODO: openssl config option: no-comp, no-sslv3, -DOPENSSL_NO_HEARTBEATS

Compile SSHd with support for new openSSL-Version::

    # compile openSSH with openssl usage
    # sources and readme: https://github.com/openssh/openssh-portable
    # info: installed is v7.6
    cd ~/
    wget https://github.com/openssh/openssh-portable/archive/V_8_3_P1.tar.gz
    tar zxf V_
    cd
    configure --help
    ./configure --with-pam
    make
    make tests

SSH benchmark::

    rsync -r -v --progress -e ssh ./rec.2.h5 hans@10.0.0.52:/home/hans/
        3.7 - 4.7 MB/s at 45% cpu usage out-of-the-box
        6.x - 7.0 MB/s at 66% cpu usage after optimizations
        -> similar results with "external" sd-card
        -> cpu has most likely no crypto, or does not use it

Switch to proper timezone (2h behind)::

    sudo dpkg-reconfigure tzdata
    /etc/timezone       -> one line "Europe/Berlin", alternative to "reconfigure"

Software cleanup::

    sudo apt list --installed
    sudo apt -y remove ...
    sudo apt autoremove

        alsa-utils
        dnsmasq
        dnsmasq-base
        nginx &-common &-core

        linux-headers-4.15.0*
        linux-image-5.4.24

        wireless-regdb -tools
        wpasupplicant

        libpython2.7 &-dev &-minimal &-stdlib
        libpython-dev &-stdlib
        python
        python-*
        python2.7
        python2.7-*

Find biggest space waster::

    sudo du -s * | sort -n
        450 MB /lib -> /firmware -> intel 22 MB, netronome 24 MB, liquidio 24 MB, amdgpu 31 MB
        912 MB /usr
        190 MB /var

Switch dynamically between cpu-governors::

    cpufreq_info
    sudo cpufreq-set --governor powersave
        -> when idling
    sudo cpufreq-set --governor performance
        -> when preparing or during measurement
        hardcoded in /etc/init.d/cpufrequtils
        GOVERNOR, MAX_SPEED, MIN_SPEED

CPU-Info::

    cat /proc/cpuinfo | grep BogoMIPS

Disable Devices in /boot/uEnv.txt::

    disable_uboot_overlay_video=1
    disable_uboot_overlay_audio=1
    disable_uboot_overlay_wireless=1
    disable_uboot_overlay_adc=1


Further actions:
    - nix, https://nixos.org/ seems to be the better ansible (only future reference)
    - is active cooling improving the performance? IC is only warm to the touch, so no
    - look at dmesg for oddities
        - console on ttyO0, 115200n8, ttyS0
        - spectre v2 -> not needed mitigation, cost performance
        - redundant drivers enabled: CAN driver, ALSA, Bluetooth,
        - unusual timer-jump, mounting mmc takes 20-25s each
            [    1.122421] Freeing unused kernel memory: 1024K
            [   18.463305] EXT4-fs (mmcblk1p1): mounted filesystem with ordered data mode. Opts: (null)
    - "systemd-analyze blame" shows:
        - v4.14: 39.936s dev-mmcblk1p1.device
        - v4.19: 53.286s dev-mmcblk1p1.device, 29.013s generic-board-startup.service
    - look at power consumption
    - BBB has a crypto engine, but is it used by openSSL! This site has a benchmark: https://datko.net/2013/10/03/howto_crypto_beaglebone_black/
    - switch to more SD friendly filesystem, F2FS, YAFFS2
    - benchmark cpu BOINC

Security Concept
----------------

find open ports -> delete not needed services::

    sudo netstat -apn | grep LISTEN
        nginx (webserver)
        dnsmasq (dns and dhcp server)

delete default users::

    /etc/passwd shows users: root, ubuntu, ansible-user
    sudo su
    userdel ubuntu
    exit

sshd-security-improvements (/etc/ssh/sshd_config)::

    Protocol 2                    # default: 2, 1
    StrictModes yes               # regarding choice of libs

    LoginGraceTime 1m
    MaxAuthTries 1

    PermitRootLogin no
    PasswordAuthentication no
    PermitEmptyPasswords no

    UsePAM yes
    PubkeyAuthentication yes
    AuthorizedKeysFil .ssh/authorized_keys
    RhostsRSAAuthentication no
    ChallengeResponseAuthentication no

    X11Forwarding no
    # AllowUsers user1 user2    -> for later

sshd-banner for login (/etc/issue.net)::

    This Node is part of project Shepherd of the NES LAB, https://nes-lab.org/

    This service is restricted to authorized users only. All activities on this system are logged.
    Unauthorized access will be fully investigated



disable terminal over serial (part1: services)::

    systemctl                                         -> shows current services
    systemctl list-unit-files                         -> shows current services
    sudo systemctl mask serial-getty@ttyGS0.service   -> usb gadget serial shell
    sudo systemctl mask serial-getty@ttyS0.service    -> uart0 shell
    sudo systemctl mask getty@tty1.service            -> semi-shell

    # also handle the issuing source of the console in /boot/grub/grub.cfg, as kernel command line parameter "console="

    # additional things to disable
    sudo systemctl disable ofono.service
    sudo systemctl disable motd-news.service              -> TODO: could be helpful later to show stats on logon
    sudo systemctl disable motd-news.timer
    sudo systemctl disable graphical.target
    sudo systemctl disable dbus-org.bluez.service
    sudo systemctl disable bluetooth.service

disable terminal over serial (part2: grub)::

    sudo nano /etc/default/grub
        -> remove "console=..." part
    sudo update-grub

disable terminal over serial (part3: ??)::

    dmesg | grep tty                            -> still shouts "Kernel command line: console=ttyO0,115200n8" ...
    sudo grep -rinI  'console=tty' /etc /boot      -> finds entry in console-setup
        -> /etc/default/grub.ucf-dist
        -> /etc/default/grub
    sudo grep -rinI  'ttyO0' /etc /boot
        -> /boot/SOC.sh:31:serial_tty=ttyO0
        -> /etc/securetty:348

    sudo rm /etc/default/grub.ucf-dist              -> copy of "grub" because of manual edit
    sudo nano /boot/SOC.sh                          -> contains uboot start?

Find and disable world writable files::

    # source: https://www.oreilly.com/library/view/linux-security-cookbook/0596003919/ch09s11.html
    # find & disable
    sudo find / -xdev -perm +o=w ! \( -type d -perm +o=t \) ! -type l -ok chmod -v o-w {} \;
    # prevent newly created files from beeing world writable, for current user
    umask 002

Further actions:
- clean cron jobs
- clean world-writable / readable
- try linPEAS
- collect important log-files periodically, disable the rest
- drop root privilege for testbed-user, allow to handle hw-io with groups
- sysctl contains several sockets
- add concept for security

Fixing Device Tree Drivers for newer Kernels
--------------------------------------------


- device Tree Versions
    - v4.14.x https://github.com/beagleboard/BeagleBoard-DeviceTrees/commit/4a9c0a652f58090491319d27dac4bf76da7d6086
    - v4.19.x https://github.com/beagleboard/BeagleBoard-DeviceTrees/commit/af07ef77cc6f8f94568a4c238cc6d41fb8c81931
    - v5.4.x https://github.com/beagleboard/BeagleBoard-DeviceTrees/commit/26b4c9fea3ff919835ba27393d5781ca4dd0923f
    - overlays: https://github.com/beagleboard/bb.org-overlays/tree/master/src/arm

- found changes
    - compatible was: "ti,beaglebone", "ti,beaglebone-black"
    - newer dts files only speak of "ti,am335x-bone-black", "ti,am335x-bone-green", "ti,am335x-bone", "ti,am33xx"
    - pinctrl-single,pins
        - shprd:    0x034 0x06  /* P8.11, pr1_pru0_pru_r30_15 */
        - bbuniv:   AM33XX_IOPAD(0x0834, PIN_OUTPUT | INPUT_EN | MUX_MODE6)
    - exclusive-use
    - target pruss overlay

- shepherd firmware
    - make && make install in device-tree sub-folder
    - install in /lib/firmware/
    - manual load::  echo BB-SHPRD >/sys/devices/bone_capemgr.7/slots

Workflow shepherd firmware::

    cd ~/
    git clone https://github.com/orgua/shepherd
    cd shepherd/software/firmware/device-tree
    make && make install

    # change uboot_overlay_pru to 4-19 in /boot/uEnv.txt

    # add to /boot/uEnv.txt
    # check after reboot if loaded
    sudo /opt/scripts/tools/version.sh | grep UBOOT

    Helper to show loaded overlays under: /proc/device-tree/chosen/overlays/

Backup Image::

    dd if=/dev/mmcblk1 of=/media/stick/mmc_s0_v4.19.94_bootstrap_apt.img

