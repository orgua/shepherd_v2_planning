ansible-playbooks
-----------------

bootstrap, TODO
    - "Set authorized key from local file" -> script stops, no ssh pub key generated before trying to access it, on host!
        - give better error message
        - fix: ssh-keygen
    - why "ansible_become_password", what is the meaning? script sets no pw when creating new user
    - user should add (maybe)
        ``generate_ssh_key: yes``
        ``state: present``

General	
    - playbook workflow - why "changed", and not all "ok"
    - when is deploy needed? -> better document all scripts
    - accelerate ansible: allow pipelining in ``ansible.cfg`` with ``pipelining = True`` in SSH-Section
    - can bash-out be saved to file?
    - how do we see if install is fine? -> ``journalctl -u shepherd``
    - image could be run virtually

playbook args::

    -v              -> stdout
    --check         -> dry run

Improve Speed of SSH and Ansible by tuning local ``~/.ssh/config``::

    Host *
        AddressFamily inet
        Protocol 2
        Compression no
        ServerAliveInterval 60
        ControlMaster auto
        ControlPath ~/.ssh/sockets/%r@%h-%p
        ControlPersist 6000


System Status Feedback
----------------------

BBB Leds
    - USER0 is the heartbeat indicator from the Linux kernel.
    - USER1 turns on when the SD card is being accessed
    - USER2 is an activity indicator. It turns on when the kernel is not in the idle loop.
    - USER3 turns on when the onboard eMMC is being accessed.

BBB Readme
    - up to date system information https://elinux.org/Beagleboard:BeagleBoneBlack_Debian
        - updating kernel
        - new device tree interface
    - improve system and boot performance: https://embexus.com/2017/05/16/embedded-linux-fast-boot-techniques/
    - official boot optimization: https://processors.wiki.ti.com/index.php/Sitara_Linux_Training:_Boot_Time_Reduction

System improvements
---------------------------------------------------

System-Info
    - Ubuntu 18.04, bionic
    - official image from 2020-03-12
    - Beaglebone Green

Downgrade kernel (deprecated and not correct way, see below)::

    sudo apt install linux-image-4.14.108-ti-r136, linux-headers-...
        currently installed 4.19.94-ti-r36
        -> rt-kernel is possible, but A: not needed, B: bad for performance
        last updated bb-cape-overlays
    sudo apt list --installed | grep linux-  -> remove other

Upgrade Kernel (Included in ansible)::

    cd /opt/scripts/tools/
    sudo git pull
    sudo ./update_kernel.sh --lts-5_4       -> warning: does not work for BBB yet, just update to latest 4.19 release by ommiting --lts..
    sudo reboot

    sudo apt-get install linux-headers-`uname -r`

Update Bootloader (Included in ansible)::

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

SSHd improvement (Included in ansible)::

    sudo nano /etc/ssh/sshd_config
        UseDNS no           -> disable dns lookup on server side
        Compression no      -> default is "delayed" (yes) after login

    # Client side: use ipv4, one single tcp-connection (controlMaster auto) on Client-side

SCP Improvement::

    # Idea: handshake is secure and fully crypted, after that the encryption could be lowered, maybe even with fast crypto-module-support
    # switching crypto cipher -> man ssh_config shows for local ``~/.ssh/config``, global ``/etc/ssh/ssh_config`` and ``sshd_config``

    Specifies the ciphers allowed and their order of preference.  Multiple ciphers must be comma-separated.  If the specified list begins with a
    ‘+’ character, then the specified ciphers will be appended to the default set instead of replacing them.  If the specified list begins with a
    ‘-’ character, then the specified ciphers (including wildcards) will be removed from the default set instead of replacing them.  If the spec‐
    ified list begins with a ‘^’ character, then the specified ciphers will be placed at the head of the default set.

    The supported ciphers are:
        3des-cbc, aes128-cbc, aes192-cbc, aes256-cbc, aes128-ctr, aes192-ctr, aes256-ctr
        aes128-gcm@openssh.com, aes256-gcm@openssh.com, chacha20-poly1305@openssh.com

    The default is:
        chacha20-poly1305@openssh.com, aes128-ctr, aes192-ctr, aes256-ctr,
        aes128-gcm@openssh.com,aes256-gcm@openssh.com

    The list of available ciphers may also be obtained using "ssh -Q cipher".

    OpenSSH 7.3 are:
        3des-cbc, aes128-cbc, aes192-cbc, aes256-cbc, aes128-ctr, aes192-ctr,
        aes256-ctr, aes128-gcm@openssh.com, aes256-gcm@openssh.com, arcfour,
        arcfour128, arcfour256, blowfish-cbc, cast128-cbc, chacha20-poly1305@openssh.com.

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

    # compact benchmark:
    openssl speed -elapsed -evp aes-128-cbc aes-192-cbc aes-256-cbc
    openssl speed -elapsed -evp aes-128-ctr aes-192-ctr aes-256-ctr
    openssl speed -elapsed -evp aes-128-gcm aes-256-gcm des-ede3-cbc chacha20-poly1305

    The 'numbers' are in 1000s of bytes per second processed.
    type             16 bytes     64 bytes    256 bytes   1024 bytes   8192 bytes  16384 bytes

    aes-128-cbc      30229.13k    40065.07k    43963.48k    45118.46k    45378.22k    45416.45k  --> Insecure
    aes-192-cbc      26305.07k    33554.03k    36051.20k    36890.97k    37188.95k    37191.68k  --> Insecure
    aes-256-cbc      24307.25k    30221.35k    32434.60k    33024.34k    33161.22k    33166.68k  --> Insecure

    aes-128-ctr      24565.01k    36514.28k    41899.95k    47885.31k    49993.05k    50173.27k
    aes-192-ctr      22875.85k    32318.14k    35530.50k    40397.14k    42265.26k    42341.72k
    aes-256-ctr      21166.89k    29006.49k    30876.16k    35073.37k    36560.90k    36580.01k

    aes-128-gcm      21461.14k    28427.01k    31007.74k    34032.30k    34802.35k    34794.15k
    aes-256-gcm      18821.07k    23611.90k    24569.51k    27030.19k    27661.65k    27634.35k

    des-ede3-cbc      5420.43k     5722.56k     5799.77k     5807.45k     5829.97k     5821.78k
    chacha20-poly    22729.05k    52835.75k    96532.65k   107768.83k   112194.90k   112361.47k
                     128-cbc        chacha     chacha      chacha       chacha         chacha

    # real test:
    scp -o Cipher=chacha20-poly1305@openssh.com ./rec.2.h5 10.0.0.52:/home/hans/
    # TI-Website about CryptoModule and performance on this CPU: https://processors.wiki.ti.com/index.php/AM335x_Crypto_Performance
    # TI-Support shows that Module also handles basic compression: https://e2e.ti.com/support/processors/f/791/t/349219?AM335x-Hardware-Crypto-Engine
    # TODO: change packet size for scp, try basic compression and fastest cipher for module

Add Driver for Crypto-Module of CPU::

    # compile and add Cryptodev module / https://github.com/cryptodev-linux/cryptodev-linux
    # Manual1: https://lauri.võsandi.com/2014/07/cryptodev.html
    # Manual2: https://datko.net/2013/10/03/howto_crypto_beaglebone_black/

    cd ~/
    wget https://github.com/cryptodev-linux/cryptodev-linux/archive/cryptodev-linux-1.10.tar.gz
    tar zxf cryptodev-linux-1.10.tar.gz
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
    apt list --installed | grep sll             -> shows 1.0.2n
    cd ~/
    wget https://github.com/openssl/openssl/archive/OpenSSL_1_0_2n.tar.gz
    tar zxf OpenSSL_1_0_2n.tar.gz
    cd OpenSSL
    ./config -DHAVE_CRYPTODEV -DUSE_CRYPTODEV_DIGESTS shared enable-devcryptoeng no-sse2 no-com --openssldir=/usr/local/ssl
    make build_generated && make libcrypto.a
    sudo make install_sw
    sudo cp /usr/local/ssl/lib/libcrypto.so.1.0.0 /usr/lib/arm-linux-gnueabihf/libcrypto.so.1.0.0
    # -> WORKS but is slow (see benchmark)

    TODO: openssl config option: no-comp, no-sslv3, -DOPENSSL_NO_HEARTBEATS

Compile SSHd with support for new openSSL-Version::

    # compile openSSH with openssl usage
    # sources and readme: https://github.com/openssh/openssh-portable
    # info: installed is v7.6p1-4
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
        1.5 - 2.8 MB/s  with 50% usage

Switch to proper timezone - 2h behind (included in ansible)::

    sudo dpkg-reconfigure tzdata
    /etc/timezone       -> one line "Europe/Berlin", alternative to "reconfigure"

Software cleanup (included in ansible)::

    sudo apt list --installed
    sudo apt -y remove ...
    sudo apt autoremove

        alsa-utils
        dnsmasq
        dnsmasq-base
        nginx &-common &-core
        can-utils
        rfkill

        linux-headers-4.15.0*
        linux-image-5.4.24

        wireless-regdb -tools
        wpasupplicant
        ofono

    Ansible-Hard.To.Get.packets:
        sudo apt remove linux-image-4.19.94-ti-r36
        # dpkg shows a kernel, that isn't in apt...
        # dpkg-query -Wf '${Installed-Size}\t${Package}\n' | sort -n
        sudo dpkg -P linux-image-5.4.24-armv7-x20

    -> down to          1.4 GB MMC &   <41 MB RAM usage      (with shepherd)

Software Cleanup Part2::

    gcc-pru
    gdb-dbg
    gdb
    cmake
    btrfs-progs
    bluez
    alsa


Find biggest space waster::

    sudo du -s * | sort -n
        450 MB /lib -> /firmware -> intel 22 MB, netronome 24 MB, liquidio 24 MB, amdgpu 31 MB
        912 MB /usr
        190 MB /var

    dpkg-query -Wf '${Installed-Size}\t${Package}\n' | sort -n
    # better (part of debian-goodies):
    dpigs -n20

Switch dynamically between cpu-governors::

    sudo apt install cpufrequtils
    cpufreq-info
    sudo cpufreq-set --governor powersave
        -> when idling
    sudo cpufreq-set --governor performance
        -> when preparing or during measurement
        hardcoded in /etc/init.d/cpufrequtils
        GOVERNOR, MAX_SPEED, MIN_SPEED

CPU-Info::

    cat /proc/cpuinfo | grep BogoMIPS
    dmesg | grep Bogo # better

Disable Devices in /boot/uEnv.txt (included in shepherd package)::

    disable_uboot_overlay_video=1
    disable_uboot_overlay_audio=1
    disable_uboot_overlay_wireless=1
    disable_uboot_overlay_adc=1

Switch to Ubuntu 20.04 (bionic to focal)y::

    # pro: brings fresh gcc 10, python 3.8, sshd 8.2,
    sudo apt update && sudo apt upgrade
    sudo reboot
    sudo apt install update-manager-core
    sudo do-release-upgrade -d
    sudo reboot
    # Some third party entries in your sources.list were disabled.
    # new unwanted sw: libasound* alsa* ubuntu-release-upgrader* update-manager* ti-sgx* iw gfortran* eject
    sudo apt-get remove '^namestart.*'
    # general things to look out for gfx, rf, wifi, wlan, sound, alsa

Fix long boot (included in ansible)::

    sudo rm /boot/initrd.img-*
    # file is not needed and is putting a 20s wait on kernel


Unnecessary kernel modules, ``lsmod`` shows

    - wkup_m3_ipc               -> Cortex M3 Co-Processor, misbehaving in dmesg, loaded to early
    - virtio, virtio-ring       -> IO-Virtualization in KVM
    - uio, uio_pdrv_genirq      -> should be user-space IO
    - u_serial, usb_f_acm       -> serial emulation on USB
    - sch_fq_codel              -> Fair Queue controlled delay
    - libcomposite              -> usb HID and massstorage

Further actions:
    - nix, https://nixos.org/ seems to be the better ansible (only future reference)
    - is active cooling improving the performance? IC is only warm to the touch, so no
    - look at ``dmesg`` for oddities
        - console on ttyO0, 115200n8, ttyS0 -> see security concept
        - spectre v2 -> not needed mitigation, cost performance
        - redundant drivers enabled: CAN driver, ALSA, Bluetooth -> uninstalled
        - unusual timer-jump, mounting mmc takes 20-25s each -> ext4-mount takes forever
            [    1.122421] Freeing unused kernel memory: 1024K
            [   18.463305] EXT4-fs (mmcblk1p1): mounted filesystem with ordered data mode. Opts: (null)
    - ``systemd-analyze blame`` shows:
        - v4.14: 39.936s dev-mmcblk1p1.device
        - v4.19: 53.286s dev-mmcblk1p1.device, 29.013s generic-board-startup.service
    - look at power consumption
    - BBB has a crypto engine, but is it used by openSSL! This site has a benchmark: https://datko.net/2013/10/03/howto_crypto_beaglebone_black/
    - switch to more SD friendly filesystem, F2FS, YAFFS2
    - benchmark cpu BOINC
    - switch from ``-ti-kernel`` to ``-bone``?
        - see https://groups.google.com/forum/#!topic/beagleboard/sAefubfDqco
        - ``-bone`` is from Robert Nelson, mainly for BB and BBB, PRU with UIO
        - ``-ti-kernel`` is for all TI CPUs, PRU with remoteproc
        - ``-xenomai`` is dual kernel, realtime, 40 us
        - ``-rt`` uses preemt features to reduce latency to about 100 us

Security Concept
----------------

Goal: mostly secure beaglebone, but it is also partly for the vServer

find open ports -> delete not needed services (included in ansible)::

    sudo netstat -apn | grep LISTEN
        nginx (webserver)
        dnsmasq (dns and dhcp server)

delete default users (included in ansible)::

    /etc/passwd shows users: root, ubuntu, ansible-user
    sudo su
    userdel ubuntu
    exit

sshd-security-improvements [/etc/ssh/sshd_config] (included in ansible)::

    Protocol 2                    # default: 2, 1
    StrictModes yes               # regarding choice of libs and world writables

    LoginGraceTime 1m
    MaxAuthTries 2

    PermitRootLogin no
    PasswordAuthentication no       # for the Server we should at least allow secure PWs
    PermitEmptyPasswords no

    UsePAM yes
    PubkeyAuthentication yes
    AuthorizedKeysFile .ssh/authorized_keys
    RhostsRSAAuthentication no
    ChallengeResponseAuthentication no

    X11Forwarding no
    AllowUsers user1 user2    -> for later

    # the following ones with "-" in front of list are not recommended (weak, broken) and will be excluded (ssh-audit)
    KexAlgorithms -ecdh-sha2*,diffie-hellman-group-exchange*,diffie-hellman-group14-sha1
    HostKeyAlgorithms -ecda-sha2*,ecdsa-sha2*
    Ciphers chacha20-poly1305@openssh.com,aes128-ctr,aes192-ctr,aes256-ctr
    MACs -umac-64*,hmac-sha1*,hmac-sha2-256,hmac-sha2-512,umac-128@open*


sshd-banner for login (/etc/issue.net) (included in ansible)::

    This Node is part of project Shepherd of the NES LAB, https://nes-lab.org/

    This service is restricted to authorized users only. All activities on this system are logged.
    Unauthorized access will be fully investigated



disable terminal over serial (part1: services) (included in ansible)::

    systemctl                                         -> shows current services
    systemctl list-unit-files                         -> shows current services
    sudo systemctl mask serial-getty@ttyGS0.service   -> usb gadget serial shell
    sudo systemctl mask serial-getty@ttyS0.service    -> uart0 shell
    sudo systemctl mask getty@tty1.service            -> semi-shell

    # also handle the issuing source of the console in /boot/grub/grub.cfg, as kernel command line parameter "console="

    # additional things to disable (resource saving)
    systemctl set-default multi-user                      -> prereq to turn of graphical.target
    sudo systemctl disable ofono.service                  -> most of these better be handled by apt
    sudo systemctl disable motd-news.service              -> TODO: could be helpful later to show stats on logon
    sudo systemctl disable motd-news.timer
    sudo systemctl disable graphical.target
    sudo systemctl disable dbus-org.bluez.service
    sudo systemctl disable bluetooth.service

disable terminal over serial (part2: grub) (included in ansible)::

    sudo nano /etc/default/grub
        -> remove "console=ttyO0,115200n8 " part
    sudo update-grub

disable terminal over serial (part3: all failures)::

    dmesg | grep tty                            -> still shouts "Kernel command line: console=ttyO0,115200n8" ...
    sudo grep -rinI  'console=tty' /etc /boot      -> finds entry in console-setup
        -> /etc/default/grub.ucf-dist
        -> /etc/default/grub
    sudo grep -rinI  'ttyO0' /etc /boot
        -> /boot/SOC.sh:31:serial_tty=ttyO0
        -> /etc/securetty:348

    sudo rm /etc/default/grub.ucf-dist              -> copy of "grub" because of manual edit
    sudo nano /boot/SOC.sh                          -> contains uboot start?

    # there is a /bbb-uEnv.txt and /nfs-uEnv.txt
    remove >>console=tty0 console=${console} <<

disable terminal over serial (part4: u-boot)::

    # DEPRECATED - to access config download u-boot-tools and adapt config
    sudo nano /etc/fw_env.config
        /dev/mmcblk1boot1 0x0000 0x20000 0x20000
        # -> hint: there is nothing there, check with ``sudo hexdump /dev/mmcblk1boot1`` or ``hexedit``
        # seems to be on mmcblk1 0x20000 0x20000
        CONFIG_BOOT_ENV =
    sudo fw_printenv
    sudo fw_setenv
    # if that fails ``echo 0 > /sys/block/mmcblkXbootY/force_ro``

    # now you have to interrupt u-boot to get to it's console (use serial on J1)
    saveenv         -> will create /boot/uboot.env
    # this is no handy way for remote management -> maybe the first image could be modified for that

    # uEnv.txt can run cmds! (TODO: figure out the right command, these are wrong)
    uenvcmd=run saveenv;
    bootcmd=saveenv; run saveenv;
    cmdline= ...

Find and disable world writable files (included in ansible)::

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
    - overlays: https://github.com/RobertCNelson/bb.org-overlays/tree/master/src/arm

- changes to reference DT-overlays
    - compatible with v4.14.x: "ti,beaglebone", "ti,beaglebone-black"
    - newer dts files only speak of "ti,am335x-bone-black", "ti,am335x-bone-green", "ti,am335x-bone", "ti,am33xx"
    - pinctrl-single,pins
        - shprd:    0x034 0x06  /* P8.11, pr1_pru0_pru_r30_15 */
        - bbuniv:   AM33XX_IOPAD(0x0834, PIN_OUTPUT | INPUT_EN | MUX_MODE6)
    - exclusive-use seems fine
    - target pruss overlay -> fine
    - overlay is not announcing itself in fragment@0

- shepherd firmware
    - ``make && sudo make install`` in device-tree sub-folder
    - install in ``/lib/firmware/``
    - check status in ``/proc/device-tree/chosen/overlays/``
        - or via: ``sudo /opt/scripts/tools/version.sh | grep UBOOT``

Workflow shepherd firmware::

    cd ~/
    git clone https://github.com/orgua/shepherd
    cd shepherd/software/firmware/device-tree
    make && sudo make install
    # add to /boot/uEnv.txt
    # check after reboot if loaded
    sudo /opt/scripts/tools/version.sh | grep UBOOT

Backup Image::

    sudo mount /dev/sda1 /media
    sudo dd if=/dev/mmcblk1 of=/media/mmc_s0_v4.19.94_bootstrap_apt.img
    sudo umount /media

Install custom Shepherd-Code and check install
----------------------------------------------

-> TODO: refactor this into general documentation / dev

Install::

    # on server
    sudo git clone https://github.com/orgua/shepherd
    cd /shepherd
    ansible-playbook ./deploy/deploy.yml

Check (on sheep)::

    # DT-Overlay: there should be an BB-SHPRD-... -> overlay is active
    ll /proc/device-tree/chosen/overlays/

    # Custom-Services: should show 3x shepherd entries, only shepherd-launcher.service enabled, also: shepherd-rpc, shepherd
    systemctl list-unit-files | grep shep

    # Timesync-Services: both should be active and running
    systemctl | grep ptp
    systemctl | grep phc

    # PRUs: two pru-rproc available and probed successfully
    dmesg | grep pru

    # PRUs: should show remoteproc1 and 2
    ll /sys/class/remoteproc/

    # KernelModule: it should probably be active - but isn't (sudo modprobe shepherd)
    lsmod | grep shep

    # KernelModule: should talk "shprd: found device", "found PRU0/1", "PRUs started"
    dmesg | grep shp

    # KernelModule: ``state`` should exist
    ll /sys/shepherd/

    # Shepherd program: >
    cp /opt/shepherd/software/meta-package/example_config.yml /etc/shepherd/config.yml
    shepherd-sheep -vv run --config /etc/shepherd/config.yml
        -> error, no /sys/shepherd/state
            there is /sys/module/shepherd, without "state"

Tests for preparing software-release

    - use a fresh ubuntu lts host and newest fresh ubuntu image for BB
    - follow install instructions (install ansible, bootstrap, deploy)
    - let pytests run

Useful commands on a fresh system::

    pip install --upgrade ansible

    sudo chown -R user /opt/shepherd
    sudo passwd user
    cp /opt/shepherd/software/meta-package/example_config.yml /etc/shepherd/config.yml
    sudo shepherd-sheep -vv run --config /etc/shepherd/config.yml

    cd /opt/shepherd/software/python-package/
    sudo python3 setup.py test --addopts "-vv"
    # bump2version --tag patch # -> just hand in PR or hash

Open Questions

    - vCap -> what else is there to do to activate it? DT-Overlay, probably switch in pru-firmware, board-modification?
    - how do is see that pru got the right firmware?

Beaglebone AI
-----------------

- Images
    - Best Image: am57xx eMMC flasher ubuntu console, 2 GB, https://elinux.org/BeagleBoardUbuntu#eMMC:_BeagleBoard-X15_and_BeagleBone_AI
    - Better Image: am57xx eMMC flasher debian iot, 4 GB, https://elinux.org/Beagleboard:BeagleBoneBlack_Debian#Debian_Buster_IOT_Snapshot
            - untested alternative: debian console, sub 1 GB
    - Wrong Image: am57xx debian IoT am5729, 8 GB unpacked, http://beagleboard.org/latest-images
- Install
    - "boot" button is gone, but image flashes automatically (LED Larson-Scanner, until finished with copy, then static)
- ubuntu 18.04.4-console-armhf-2020-03-12
    - **Warning**: CPU gets very hot, even whole PCB, 66 °C idle, 77 °C after apt upgrade
    - takes about 1.2 GB of the 15 GB eMMC
    - dmesg reports 24.59 BogoMIPS (BBG shows 995?!?)
    - uname: 4.19.94-ti-r36
    - dd if=/dev/zero of=./testfile bs=100M count=1 oflag=direct -> 73 MB/s (x3.5 of BBG)
    - GBE works with Cat 5e, 5m

    - 2nd AI shows "sudo hexdump -C /dev/mmcblk1boot1" -> .U3.BBONE-AI00A1 | 1933EMAI000015 -> board 15
- ansible: bootstrap, install, setup_linux_configuration, _performance, _security
    - uname: 4.19.94-ti-r51
    - uname: 5.4.24-armv7-x20 -> not booting
- **oddities**
    - some restarts are not coming back & there are random shutdowns
    - cpu stays boiling hot, even with 99.6% idling, governor set to powersave
        - ubuntu 18.4.4 from elinux, with 4.19.94-r36 & r51
        - debian 10.4 iot from elinux, with 4.19.94-r41?
        - debian 10.4 console -> does not even flash
        - debian 10.3 iot from bb.org with 4.19.94-r42
        - debian 9.12 console from elinux with 4.14.108-r134 stays at 50 deg, only one?!?
    - ram only shows 578 MB ?!? it should be 1 Gig
        - DSP reserves 300 MB+
        - get ram back: https://groups.google.com/g/beagleboard/c/-kDcIPsLCkc/m/xHyrFKepAgAJ
    - there is no device-tree overlay yet, just a big monolithic dts
    - forum-post: it is easy to kill a cpu with wrong pin-inputs, https://groups.google.com/forum/embed/?place=forum/beagleboard&showsearch=true&showpopout=true&showtabs=false&hideforumtitle=true&parenturl=http%3A%2F%2Fbeagleboard.org%2Fdiscuss#!category-topic/beagleboard/beaglebone-ai/fzwYWLDrQJw
        - some pins are connected to two balls on the CPU, but io-use must be mutual exclusive
    - PRU-Changes -> ll /sys/class/remoteproc/ -> remoteproc4 to remoteproc7
    - addresses in RAM changed most likely as well
    -
- documentation
    - nice pin-overview https://docs.google.com/spreadsheets/d/1fE-AsDZvJ-bBwzNBj1_sPDrutvEvsmARqFwvbw_HkrE/edit#gid=1518010293
    - nice to distinguish BB-Models: cat /proc/device-tree/model -> BeagleBoard.org BeagleBone AI
    - device tree is raw, see https://www.elinux.org/EBC_Exercise_41_Pin_Muxing_for_the_AI
        - AI.dts https://github.com/beagleboard/BeagleBoard-DeviceTrees/blob/v4.19.x-ti-overlays/src/arm/am5729-beagleboneai.dts
        - overlays, general: https://github.com/beagleboard/bb.org-overlays
    - AI survival guide: https://www.element14.com/community/community/project14/visionthing/blog/2019/11/16/beagleboard-ai-brick-recovery-procedure
    - AI reference manual: https://github.com/beagleboard/beaglebone-ai/wiki/System-Reference-Manual
        - says that out rev A1 is prototype, even A1a is alpha pilot run
    - show temp from internal sensors: watch /opt/scripts/device/x15/test_thermal.sh
    - included Processors
        - 2x cortex a15
        - 2x C66 DSP, FP VLIW with openCL, TMS320C66x
        - 4x Cortex-M4
        - 4x PRU
        - 4x EVE, embedded vision engines
        - dual core powerVR SGX544 3d GPU
        - vivante GC320 2D graphics accelerator

TODO:
- save power
- turn off not needed processors,
- unload (lsmod) wifi, bt, media (videodev, v4l2), videobuf, vpdma, ti_csc
- apt: bb-node-red-installer
