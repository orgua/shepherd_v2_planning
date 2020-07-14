Current Tasks
=============

Unsolved, not mentioned Details in Requirements
-----------------------------------------------

- Testbed
    - are targeted rooms limited to BAR II55 - II75 (`cfaed floor-plan <https://navigator.tu-dresden.de/etplan/bar/02>`_)
- Hardware
    - nodes powered and controllable via POE
        - already available: 20 external PoE-Splitter and 24 Port Zyxel Ethernet-Switch (with PoE)
        - -> Kai preferes this solution
    - how to control distant long-Range-Nodes
        - idea 1: mobile network for control back-channel
        - idea 2: scheduled via pre-configuration (and access to time-base)
    - variable TX-Power for multi-hop → is it enough to change firmware or do we need (programmable) attenuation?
        - -> input from kai: firmware should suffice
    - should the gpios to target be individually switchable (connected, disconnected) for less energy-interference
        - input from kai: no requirement, but current IC supports it (TI TXB03)
    - 2x2x25 Pin-Header between beaglebone and Shepherd-cape is hard to (dis)assemble -> is there a need to forward all pins (additional cape)?
        - improvement 1: used pins don't have to be forwarded
        - improvement 2: do not forward at all -> capelets and targets get connected by better mezzanine-connector
        - -> input from kai: gold plated pins should be easier to handle
    - are there any future-extensions (sensors, actors) that would require a general purpose capelet-Port (SDR-Extension is not feasible for shepherd nodes)
        - there are still unused GPIO available, even a uart, but no SPI or I2C
    - preferred casing choices: off-the-shelf case with custom front-plates or laser-cut-acrylic box?
- questions regarding design-choices on shepherd v1.x
    - does target-cape benefit from routed v_in_SHT+/-? seems like a noise-source for the ADC
    - what is the reason for the subtractor-bias / V_EMU_I
    - wouldn't it be better to have the uni-dir level switcher on vdd-target -> gpios could go into undefined state, when level is low enough
- Software
    - how dynamic do Nodes have to react on current environment (network access, gps attached)
        - i.e. system start → look for GPS and network → decide which role is used
        - -> input from kai: nodes don't have to be dynamic, can be reconfigured manually. currently done by ansible, roles per node, infrastructure service
    - do all targets get the same firmware, is it precompiled? is it already individualized, is it done by hardware / MAC, or do we have to change IDs in binary?

Testbed
-------

- when ZIH has vLAN ready: test if infrastructure of university is sufficient, mostly regarding ptp
- for node-distribution
    - talk with the leaders of groups that occupy offices
    - examine offices with IT-Admin


Hardware - mostly shepherd Cape
-------------------------------

- target-relays/switches : multi-pin, low leakage, high data-rate
  - current uni-direction (gpio) -> SN74LV4T125PWR -> diodes needed?
  - current bi-direction (uart, swd) -> TXB0304RUTR
- power-switches: low leakage
- level-changer: high speed, low-power, possible combination with switch / programmable
- is there a better power-path?
  - find reason for substractor (EMU-I)
  - why is uni-dir level switcher not on vdd-target -> it could get into undefined state
- draw digital version of float chart for power-stage
   - where is V_CREF coming from, or is it flowing backwards from VOC_SAMP?
   - is there a possibility that (CV)-LDO drives against MPPT-Converter in a unwanted state?


Software - RealTime-Code
------------------------

- PRU
    - does beaglebone AI with TI AM5729 offer more pins for PRU?
       - https://www.ti.com/product/AM5729
    - is it possible to use SPI-silicon?
    - would openOCD be able to access memory-mapped pins (tunneled through PRU)
    - fix device tree for current beagle-kernel
- FPGA, CPLD would be overkill, but what is with a teensy 4? lots of iO, SPI with DMA, FPU, 600 MHz

Software - Python
-----------------

- figure out a system to bulk-initialize scenario, measurement, but also individualize certain nodes if needed
   - build "default" one and deep-copy and individualize -> this could be part of a test-bed-module-handler
      - test-bed instantiates beaglebone-nodes [1..30] and user can hand target and harvest module to selected nodes
   - shepherd herd -> yaml -> per node config

Software - OpenOCD
------------------

- check for compatibility jtag, swd, spy-by-wire to new target ICs (tunneled through PRU)
   - nRF52 (DFU / USB, SWD)
   - STM32L4 (SWD)
   - MSP430, MSP432, CC430 (JTAG, Serial, USB, Spy-By-Wire)
- currently not routed through PRU, just normal beagle-GPIO


Software - Web-Interface
------------------------
