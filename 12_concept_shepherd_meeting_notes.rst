Learnings, with Pitfalls and (possible) Solutions
=================================================
- some

Server
------
- have an upgrade path
    - currently TUD/ZIH offers vServers and plenty of Storage from its datacenters, can be changed, expanded
    - current server: 2 Cores, 4 GB RAM, 50 GB local Storage, 10 TB network storage
    - vmware-tools have option to set cores and ram to 64 (for privileged users)
- avoid windows
- splitting servers can be an option (storage with message broker, web-interface, computing)

Data-Management
--------------
- database influx allows nanosec-timestamps as a series
    - allows easy analysis of data
    - needs lots of RAM
    - easiest interface is a socket with json-interface -> inefficient for embedded systems, can often be avoided
- hdf5 / raw-data
    - needs more custom code
    - analysis not available right away

Nodes
-----
- lockups -> powercycle
    - we (shepherd) may not have the chance to control POE
    - there is an external watchdog on the shepherd-capelet
    - there should also be a watchdog integrated in cpu (untested)
    - until now i (ingmar) had no trouble with the nodes, software base seems solid
- heat through sun, radiators, enclosure
    - degrades cpu, storage
    - BBone stays below 40 deg, case will support convectional cooling
- avoid storage without wear-leveling
    - sd-cards are not up for constant data-storage (and industrial SLC-Versions are expensive)
    - large usb-sticks tend to have wear leveling -> ours probably hasn't
    - BBone has eMMC for the linux image, support for wear leveling is unclear
    - filesystems like F2FS have a software-based wear-leveling
    - possible solution
        - keep results in ram (avoid local storage bottleneck) and stream to server
        - use usb-stick for local storage of energy-traces (more static data)
        - keep system read-only (only deactivate for updates)
        - have replacement BBones at hand (automate installation)
- collect logs
    - gives debugging-hints in events of unwanted behaviour
    - temperature, ram-usage, cpu-usage, ...
- target repurposing
    - keep functionality general so it can be used for dev, testing, ...
    - shepherds nRF-Target already has more gpio on edges and optional usb-port
- alternative platforms (copy from 11_concept_hw)
    - zynq (arm-cores + FPGA + shared mem)
        - pro: similar price as BBAI, 1 GBE, FPGA in same Package, hw-timestamping
        - con: xilinx-toolchain, documentation is overwhelming, community small, long dev-cycle
    - embedded amd platform (v2000)
        - pro: compute-power, relatively cheap (>= 200€), fast ethernet, x86-64
        - con: real-time not out of the box, low gpio-count

Web
---
- flask-framework is sufficient (same with bigger brother django)
- user-management should also include groups (to share data-pools)
- experiment-scheduler could be done with rabbitMQ (message broker)

Testbed
-------
- secure against miss-use
    - nodes can vanish, wander
        - fixate the boxes :)
        - make them unobtrusive (glue below desk, non-transparent-case)
        - BUT be transparent about the function
    - user-scripts can get system-access (heavy cpu-load, buffer-overflow, damage linux-partition)
        - put in sandbox
        - limit py-code to shepherd-framework / no other libs
        - run as special user - only essential permissions
        - set to lowest cpu-priority (nice-level)
    - voltage source could destroy hardware
        - gpio- and supply-voltage for shepherd-target are always linked
        - target-pcb has over-voltage-protection
        - experiment-management will check voltage of emulated regulator to match target-constraints
    - sanity-check everything!
    - real world testing required
- maintenance / development can easily occupy 1P full time
- documentation for the next devs

TODO
----
- compare elastic against influx, no support for nanosec?
- benchmark server (disks / ram)
- design-choices for later
    - does shepherd need databases for immediate (deep)analysis of result
        - alternative: provide post-scripts that filter data for key-parameters (benchmark-management)
    - data hording or economical use of space?
    - what else ?????
- try to design low maintenance, multi-purpose, high functionality / speed / quality
- Filesystem:
    - f2fs for usb-sticks
    - find read-only-switch for system partition
- is there an easy way to integrate a fresh BBone into the system?
