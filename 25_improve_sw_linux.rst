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

>	sudo apt install linux-image-4.14.108-ti-r136, linux-headers-...
>>	currently installed 4.19.94-ti-r36
>>  -> rt-kernel is possible, but A: not needed, B: bad for performance
>	last updated bb-cape-overlays
>	sudo apt list --installed | grep linux-  -> remove other

SD benchmark::

> fio --rw=write --name=test --size=100M --direct=1 --filename=fioBench
>>  measure ram-speed: omit --direct
>>  parallel OPs: --ioengine=libaio --iodepth=16
>
> eMMC, 4GB
> write: 7145 KiB/s at 98% util,    read:  10.1 MiB/s at 99% util
>
> external uSD is /var/shepherd/recordings, 128 GB Samsung EVO Plus
> write: 2322 KiB/s at 84% util,    read: 4245 KiB/s at 98% util
>
> reference: https://learn.sparkfun.com/tutorials/single-board-computer-benchmarks
>>  BBB-revC, write 10 MB/s, read 27 MB/s
>
> sudo blockdev --getbsz /dev/mmcblk1p1
>>  blocksize on eMMC and uSD is 4096 byte

SSH benchmark::

> rsync -r -v --progress -e ssh ./rec.2.h5 hans@10.0.0.52:/home/hans/
>>  3.7 - 4.7 MB/s at 45% cpu usage out-of-the-box
>>  6.x - 8.x MB/s at 66% cpu usage after optimizations
>>  -> similar results with "external" sd-card
>>  -> cpu has most likely no crypto-engine, or does not use it

SSH improvement::

> disable dns lookup on server side
>>  /etc/ssh/sshd_config -> UNcomment "UseDNS no"
> use ipv4, one single tcp-connection (controlMaster auto) on Client-side

Switch to proper timezone (2h behind)::

> sudo dpkg-reconfigure tzdata
> /etc/timezone -> one line "Europe/Berlin"

Software cleanup::

> sudo apt list --installed
> sudo apt -y remove ...
> sudo apt autoremove
>
> alsa-utils
> dnsmasq
> dnsmasq-base
> libpython2.7 &-dev &-minimal &-stdlib
> libpython-dev &-stdlib
> linux-headers-4.15.0*
> linux-image-5.4.24
> nginx &-common &-core
> python
> python-*
> python2.7
> python2.7-*
> wireless-regdb -tools
> wpasupplicant

Find biggest space waster::

> sudo du -s * | sort -n
>>  450 MB /lib -> /firmware -> intel 22 MB, netronome 24 MB, liquidio 24 MB, amdgpu 31 MB
>>  912 MB /usr
>>  190 MB /var

Further actions:
    - nix, https://nixos.org/ seems to be the better ansible
    - is active cooling improving the performance?
    - look at dmesg
    - look at power consumption
    - BBB has a crypto engine, but is it used by openSSL! This site has a benchmark: https://datko.net/2013/10/03/howto_crypto_beaglebone_black/
    - switch to more SD friendly filesystem

Security Concept
----------------

find open ports -> delete not needed services::

> sudo netstat -apn | grep LISTEN
>>  nginx (webserver)
>>  dnsmasq (dns and dhcp server)

- delete default user
- clean cron jobs
- clean world-writable / readable
- try linPEAS
- disable most log-files
- drop root privilege for testbed-user, allow to handle hw-io with groups
- disable terminals over serial
- add custom ssh welcome-screen (inform about service, and actions to prevent messing with it)
    - https://www.tecmint.com/5-best-practices-to-secure-and-protect-ssh-server/
- add concept for security

