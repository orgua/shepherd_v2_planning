# Improve Security

The goal is to secure the beaglebone, but it is also partly suitable for the vServer.

**Note:** all of these are included in ansible playbooks now, BUT might be checked manually from time to time.

## Find open Ports 

⇾ delete not needed services (included in ansible)::

```Shell
sudo netstat -apn | grep LISTEN
# nginx (webserver)
# dnsmasq (dns and dhcp server)
```

## Delete default Users

```Shell
/etc/passwd shows users: root, ubuntu, ansible-user
sudo su
userdel ubuntu
exit
```

## SSHD-Security-Improvements 

```Shell
sudo nano /etc/ssh/sshd_config

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
    AllowUsers user1 user2   # ⇾ for later

    # the following ones with "-" in front of list are not recommended (weak, broken) and will be excluded (ssh-audit)
    KexAlgorithms -ecdh-sha2*,diffie-hellman-group-exchange*,diffie-hellman-group14-sha1
    HostKeyAlgorithms -ecda-sha2*,ecdsa-sha2*
    Ciphers chacha20-poly1305@openssh.com,aes128-ctr,aes192-ctr,aes256-ctr
    MACs -umac-64*,hmac-sha1*,hmac-sha2-256,hmac-sha2-512,umac-128@open*
```

## Add SSH-Banner for Login

```Shell
sudo nano /etc/issue.net

    This Node is part of project Shepherd of the NES LAB, https://nes-lab.org/

    This service is restricted to authorized users only. All activities on this system are logged.
    Unauthorized access will be fully investigated
```

## Disable Terminal over Serial - Part 1 - Services

```Shell
systemctl                                        # ⇾ shows current services
systemctl list-unit-files                        # ⇾ shows current services
sudo systemctl mask serial-getty@ttyGS0.service  # ⇾ usb gadget serial shell
sudo systemctl mask serial-getty@ttyS0.service   # ⇾ uart0 shell
sudo systemctl mask getty@tty1.service           # ⇾ semi-shell

# also handle the issuing source of the console in /boot/grub/grub.cfg, as kernel command line parameter "console="

# additional things to disable (resource saving)
systemctl set-default multi-user                 # ⇾ prereq to turn of graphical.target
sudo systemctl disable ofono.service             # ⇾ most of these better be handled by apt
sudo systemctl disable motd-news.service         # ⇾ TODO: could be helpful later to show stats on logon
sudo systemctl disable motd-news.timer
sudo systemctl disable graphical.target
sudo systemctl disable dbus-org.bluez.service
sudo systemctl disable bluetooth.service
```

## Disable Terminal over Serial - Part 2 - Grub

```Shell
sudo nano /etc/default/grub
#  ⇾ remove "console=ttyO0,115200n8 " part
sudo update-grub
```

## Disable Terminal over Serial - Part 3 - U-Boot

```Shell
# DEPRECATED - to access config download u-boot-tools and adapt config
sudo nano /etc/fw_env.config
    /dev/mmcblk1boot1 0x0000 0x20000 0x20000
    # ⇾ hint: there is nothing there, check with ``sudo hexdump /dev/mmcblk1boot1`` or ``hexedit``
    # seems to be on mmcblk1 0x20000 0x20000
    CONFIG_BOOT_ENV =
sudo fw_printenv
sudo fw_setenv
# if that fails ``echo 0 > /sys/block/mmcblkXbootY/force_ro``

# now you have to interrupt u-boot to get to it's console (use serial on J1)
saveenv       #  ⇾ will create /boot/uboot.env
# this is no handy way for remote management ⇾ maybe the first image could be modified for that

# uEnv.txt can run cmds! (TODO: figure out the right command, these are wrong)
uenvcmd=run saveenv;
bootcmd=saveenv; run saveenv;
cmdline= ...
```

## Disable Terminal over Serial - Part 4 - Failures

```Shell
dmesg | grep tty                             # ⇾ still shouts "Kernel command line: console=ttyO0,115200n8" ...
sudo grep -rinI  'console=tty' /etc /boot    # ⇾ finds entry in console-setup
# ⇾ /etc/default/grub.ucf-dist
# ⇾ /etc/default/grub
sudo grep -rinI  'ttyO0' /etc /boot
# ⇾ /boot/SOC.sh:31:serial_tty=ttyO0
# ⇾ /etc/securetty:348

sudo rm /etc/default/grub.ucf-dist            # ⇾ copy of "grub" because of manual edit
sudo nano /boot/SOC.sh                        # ⇾ contains uboot start?

# there is a /bbb-uEnv.txt and /nfs-uEnv.txt
remove >>console=tty0 console=${console} <<
```

## Find and disable world writable files

```Shell
# source: https://www.oreilly.com/library/view/linux-security-cookbook/0596003919/ch09s11.html
# find & disable
sudo find / -xdev -perm +o=w ! \( -type d -perm +o=t \) ! -type l -ok chmod -v o-w {} \;
# prevent newly created files from beeing world writable, for current user
umask 002
```

## Further actions

- clean cron jobs
- clean world-writable / readable
- try linPEAS
- collect important log-files periodically, disable the rest
- drop root privilege for testbed-user, allow to handle hw-io with groups
- sysctl contains several sockets
- add concept for security
- allow shepherd without need for sudo
