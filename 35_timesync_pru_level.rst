Timesync
========

Problem
    - ptp4l runs, but two sheeps don't seem to be in sync when comparing ADC-CS-Trigger-Edges
    - spoiler: it was a slow switch and untuned ptp

Setup
    - two beaglebones are connected via ethernet to same switch
        - one beaglebone is default dev-environment, the other is freshly installed
        - both have shepherd-code from https://github.com/orgua/shepherd installed
        - both beaglebones were restarted more than once and had plenty of time to sync
    - switch
        - fritzbox, up to date and even restarted
        - later an additional Cisco Catalyst 2960-S was added to same network

Mechanism
    - two services (ptp4l, phc2sys) are keeping time between Beaglebones, with hardwaretimestamping
    - shepherd-kernel-module and pru-code are syncing the low level hardware-timer that triggers the sampling

Running services::

    /usr/sbin/ptp4l -f /etc/linuxptp/ptp4l.conf -i eth0
    /usr/sbin/phc2sys -q -m -a -rr

Configs are copied from shepherd/deploy/[...] to::

    /etc/systemd/system/phc2sys.service.d/phc2sys_mands.conf
    /etc/systemd/system/ptp4l.service.d/ptp_restart.conf


Get log-data from sync::

    sudo find / -name ptp*
    -> shows no log-files

    sudo pmc -u -b 0  'GET CURRENT_DATA_SET'
    -> offsetFromMaster is jumping like crazy
    sudo pmc -u -b 0  'GET TIME_STATUS_NP'

    sudo pmc -u -b 0  'GET PORT_DATA_SET'
    -> one sheep should show "master", the others "client"

    sudo journalctl -u ptp4l
    -> most helpful feedback

Sync-Log from the Fritzbox::

    sudo journalctl -u ptp4l

    Feb 15 20:04:04 sheep1 ptp4l[383]: [24.634] master offset     -10931 s2 freq  +16451 path delay    154478
    Feb 15 20:04:05 sheep1 ptp4l[383]: [25.634] master offset      47850 s2 freq  +71953 path delay    126215
    Feb 15 20:04:06 sheep1 ptp4l[383]: [26.634] master offset      36291 s2 freq  +74749 path delay    123934
    Feb 15 20:04:07 sheep1 ptp4l[383]: [27.635] master offset      30227 s2 freq  +79572 path delay    123306
    Feb 15 20:04:08 sheep1 ptp4l[383]: [28.635] master offset      11076 s2 freq  +69489 path delay    123306
    Feb 15 20:04:09 sheep1 ptp4l[383]: [29.635] master offset       5765 s2 freq  +67501 path delay    121767
    Feb 15 20:04:10 sheep1 ptp4l[383]: [30.635] master offset      71556 s2 freq +135021 path delay    121470
    Feb 15 20:04:11 sheep1 ptp4l[383]: [31.635] master offset     -73210 s2 freq  +11722 path delay    121470
    Feb 15 20:04:12 sheep1 ptp4l[383]: [32.635] master offset     -31401 s2 freq  +31568 path delay    121470
    Feb 15 20:04:13 sheep1 ptp4l[383]: [33.636] master offset        729 s2 freq  +54278 path delay    121058
    Feb 15 20:04:14 sheep1 ptp4l[383]: [34.636] master offset       8046 s2 freq  +61813 path delay    121058
    Feb 15 20:04:15 sheep1 ptp4l[383]: [35.636] master offset       5453 s2 freq  +61634 path delay    121058
    Feb 15 20:04:16 sheep1 ptp4l[383]: [36.636] master offset       4931 s2 freq  +62748 path delay    121497
    Feb 15 20:04:17 sheep1 ptp4l[383]: [37.637] master offset      -4661 s2 freq  +54635 path delay    121058
    Feb 15 20:04:18 sheep1 ptp4l[383]: [38.637] master offset      21602 s2 freq  +79500 path delay    120077
    Feb 15 20:04:19 sheep1 ptp4l[383]: [39.637] master offset     -11891 s2 freq  +52488 path delay    120516
    Feb 15 20:04:20 sheep1 ptp4l[383]: [40.637] master offset      -5135 s2 freq  +55676 path delay    120240
    Feb 15 20:04:21 sheep1 ptp4l[383]: [41.637] master offset        698 s2 freq  +59969 path delay    120240
    Feb 15 20:04:22 sheep1 ptp4l[383]: [42.637] master offset      -2303 s2 freq  +57177 path delay    120240
    Feb 15 20:04:23 sheep1 ptp4l[383]: [43.638] master offset      -2912 s2 freq  +55877 path delay    120240
    Feb 15 20:04:24 sheep1 ptp4l[383]: [44.638] master offset       1933 s2 freq  +59849 path delay    120240
    Feb 15 20:04:25 sheep1 ptp4l[383]: [45.638] master offset      -1803 s2 freq  +56693 path delay    119055
    Feb 15 20:04:26 sheep1 ptp4l[383]: [46.638] master offset       2346 s2 freq  +60301 path delay    118326
    Feb 15 20:04:27 sheep1 ptp4l[383]: [47.638] master offset       -554 s2 freq  +58105 path delay    119086
    Feb 15 20:04:28 sheep1 ptp4l[383]: [48.638] master offset       -269 s2 freq  +58223 path delay    118872


Good Network Switch (Cisco Catalyst 2960-S in same network)::

    sudo journalctl -u ptp4l

    Feb 15 20:52:42 sheep1 ptp4l[383]: [2942.858] master offset        173 s2 freq  +57987 path delay     12467
    Feb 15 20:52:43 sheep1 ptp4l[383]: [2943.859] master offset        -82 s2 freq  +57784 path delay     12467
    Feb 15 20:52:44 sheep1 ptp4l[383]: [2944.859] master offset        118 s2 freq  +57959 path delay     12454
    Feb 15 20:52:45 sheep1 ptp4l[383]: [2945.859] master offset        -41 s2 freq  +57836 path delay     12454
    Feb 15 20:52:46 sheep1 ptp4l[383]: [2946.860] master offset       -172 s2 freq  +57692 path delay     12463
    Feb 15 20:52:47 sheep1 ptp4l[383]: [2947.860] master offset        -69 s2 freq  +57744 path delay     12434
    Feb 15 20:52:48 sheep1 ptp4l[383]: [2948.860] master offset         64 s2 freq  +57856 path delay     12427
    Feb 15 20:52:49 sheep1 ptp4l[383]: [2949.861] master offset         98 s2 freq  +57909 path delay     12427
    Feb 15 20:52:50 sheep1 ptp4l[383]: [2950.861] master offset       -107 s2 freq  +57734 path delay     12427
    Feb 15 20:52:51 sheep1 ptp4l[383]: [2951.861] master offset        -41 s2 freq  +57767 path delay     12427
    Feb 15 20:52:52 sheep1 ptp4l[383]: [2952.862] master offset         44 s2 freq  +57840 path delay     12436
    Feb 15 20:52:53 sheep1 ptp4l[383]: [2953.862] master offset         36 s2 freq  +57845 path delay     12436
    Feb 15 20:52:54 sheep1 ptp4l[383]: [2954.862] master offset       -129 s2 freq  +57691 path delay     12452
    Feb 15 20:52:55 sheep1 ptp4l[383]: [2955.863] master offset         36 s2 freq  +57817 path delay     12457
    Feb 15 20:52:56 sheep1 ptp4l[383]: [2956.863] master offset        -92 s2 freq  +57700 path delay     12457
    Feb 15 20:52:57 sheep1 ptp4l[383]: [2957.863] master offset        -29 s2 freq  +57736 path delay     12460
    Feb 15 20:52:58 sheep1 ptp4l[383]: [2958.864] master offset         -9 s2 freq  +57747 path delay     12460
    Feb 15 20:52:59 sheep1 ptp4l[383]: [2959.864] master offset         49 s2 freq  +57802 path delay     12461
    Feb 15 20:53:00 sheep1 ptp4l[383]: [2960.864] master offset         44 s2 freq  +57812 path delay     12466


Signs of a bad network switch
    - path delay on fritzbox was 10x as high as the cisco-switch and the values show variance of 126 to 118 us
    - master-offset is jumping, logs even show 70 us offsets
        - the cisco switch is after 30 mins down to <200 ns corrections

On PRU Level
    - sync in kernel-module and pru-code works and keeps correcting
    - oszi shows that client is mostly behind (mean is ~ 500ns, max seems to be 1 us)
        - quickshot 105-108
    - capture from logic analyzer could be visualized

TODO
    - tune ptp-parameters
