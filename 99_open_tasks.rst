Current Tasks
=============

Unsolved, not mentioned Details in Requirements
-----------------------------------------------

- Hardware
   - nodes powered and controllable via POE
   - how to control distant long-Range-Nodes
      - mobile network for control backchannel, or just scheduled via pre-configuration
   - Cape-ID or Node-ID could be coded in hardware (Resistor-bridges would be human readable, flashstorage can also contain calibration-data
   - variable TX-Power for multi-hop → is it enough to change firmware or do we need attenuation
   - should the gpios to target be individual switchable (connected, disconnected)
   - 2x2x25 Pin-Header between beaglebone and Shepherd-cape is hard to (dis)assemble -> is there a need to forward all pins (additional cape)?
      - improvement 1: used pins don't have to be forwarded
      - improvement 2: do not forward at all -> capelets and targets get connected by better mezzanine-connector
- Software
   - how dynamic do Nodes have to react on current environment (network access, gps attached)
      - i.e. system start → look for GPS and network → decide which role is used

Testbed
-------

- Infrastructure of university sufficient and usable? ethernet-ports, power-sockets, ptp over ethernet-switch-cascade
- specs / prices for
   - ethernet-switch: poe, ptp, QoS, GPS
   - POE adapter
- ZIH Server request -> how to get a (virtual) server hosted there
- look for rules, ZIH, active interfering RF-nw in buildings of university (office WIFI)
- rules for using infrastructure of university (ethernet-ports, power-sockets, ptp)
- is it possible to put the nodes in cable canal

Hardware
--------

- Shepherd-Cape
   - pinout on beaglebone Black and AI, what's used and where to go
      - allow to share tasks with additional PRU of beaglebone Black
      - max out pins to target (general purpose for programming and io)
      - allow recording of PPS signal via PRU
      - reduce or bundle pins to shepherd (or another way to make disassembly easier)
   - how does the recorder measure real power if only voltage before converter and current after converter is measured?
      - does replay / emulation "just" rely on voltage-DAC and target-current-draw measurement?
   - target-relays/switches : multi-pin, low leakage, high data-rate
   - power-switches: low leakage
   - level-changer: high speed, low-power, possible combination with switch / programmable
- look for similar gps-module with external antenna support


Software - PRUs
---------------

- does beaglebone AI with TI AM5729 offer more pins?
   - https://www.ti.com/product/AM5729
- fix device tree for current beagle-kernel

Software - Python
-----------------

- figure out a system to bulk-initialize scenario, measurement, but also individualize certain nodes if needed
   - build "default" one and deep-copy and individualize -> this could be part of a test-bed-module-handler
      - test-bed instantiates beaglebone-nodes [1..30] and user can hand target and harvest module to selected nodes

Software - OpenOCD
------------------

- check for compatibility jtag, swd, spy-by-wire to new target ICs (tunneled through PRU)

Software - Web-Interface
------------------------
