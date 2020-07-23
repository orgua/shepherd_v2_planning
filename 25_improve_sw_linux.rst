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

System improvements
-------------------

Downgrade kernel (for now)::

    sudo apt install linux-image-4.14.108-ti-r136, linux-headers-...
        currently installed 4.19.94-ti-r36
        -> rt-kernel is possible, but A: not needed, B: bad for performance
        last updated bb-cape-overlays
    sudo apt list --installed | grep linux-  -> remove other

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
        -> Benchmark of enabled is 0.03s (CPU-Time)



Force OpenSSL to use CryptoModule-Hardware (TODO: hard-coding openSSL-Version is stupidly unsecure)::

    # add Cryptodev module / https://github.com/cryptodev-linux/cryptodev-linux
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

    # recompile openSSL with cryptodev-support
    cd /usr/local/src/                    -> TODO: rethink that, it forces sudo on make, not good practice
    sudo wget https://www.openssl.org/source/openssl-1.1.1g.tar.gz
    sudo tar zxf openssl-1.1.1g.tar.gz
    cd openssl...
    sudo ./config -DHAVE_CRYPTODEV -DUSE_CRYPTODEV_DIGESTS shared
    sudo make                             -> TODO: this takes ~33min
    sudo make install                     -> will be in /usr/local/bin
    # STOP TODO - everything finishes, but bin is not working at all
        -> relocation error: openssl: symbol EVP_mdc2 version OPENSSL_1_1_0 not defined in file libcrypto.so.1.1 with link time reference
    /etc/ssl/openssl.cnf                  -> TODO: maybe add/uncomment crypto in [engine]-section

    # Manual1: https://lauri.võsandi.com/2014/07/cryptodev.html
    # Manual2: https://datko.net/2013/10/03/howto_crypto_beaglebone_black/

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
    - look at dmesg
        - console on ttyO0, 115200n8, ttyS0
        - spectre v2 -> not needed mitigation, cost performance
        - redundant drivers enabled: CAN driver, ALSA, Bluetooth,
        - unusual timer-jump, mounting mmc takes 20-25s each
            [    1.122421] Freeing unused kernel memory: 1024K
            [   18.463305] EXT4-fs (mmcblk1p1): mounted filesystem with ordered data mode. Opts: (null)
    - systemd-analyze blame shows: 39.936s dev-mmcblk1p1.device -> kernel 4.14 seems to cut it more than in half
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

    dmesg still shouts "Kernel command line: console=ttyO0,115200n8" ...

Further actions:
- clean cron jobs
- clean world-writable / readable
- try linPEAS
- collect important log-files periodically, disable the rest
- drop root privilege for testbed-user, allow to handle hw-io with groups
- sysctl contains several sockets
- add concept for security

