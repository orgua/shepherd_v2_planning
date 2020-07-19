Current Tasks
=============

Unsolved, not mentioned Details in Requirements
-----------------------------------------------

Testbed
    - are targeted rooms limited to BAR II55 - II75 (`cfaed floor-plan <https://navigator.tu-dresden.de/etplan/bar/02>`_)

Hardware
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

Software
    - how dynamic do Nodes have to react on current environment (network access, gps attached)
        - i.e. system start → look for GPS and network → decide which role is used
        - -> input from kai: nodes don't have to be dynamic, can be reconfigured manually. currently done by ansible, roles per node, infrastructure service
    - do all targets get the same firmware, is it precompiled? is it already individualized, is it done by hardware / MAC, or do we have to change IDs in binary?
    - python framework: how do you like to control a measurement?
        - Var1: Set Start with absolute timestamp and from then on relative?
        - Var2: no absolute timestamp at all, just synched start, then relative timestamps for timing

questions regarding design-choices and limitations on shepherd v1.x, mostly for @kai
    - does target-cape benefit from routed v_in_SHT+/-? seems like a noise-source for the ADC
    - what is the reason for the subtractor-bias / V_EMU_I
    - wouldn't it be better to have the uni-dir level switcher on vdd-target -> gpios could go into undefined state, when level is low enough
    - do you see a chance to dynamically change pin-direction for PRU-Pins? seems to be hammered in mud in device-tree config (remuxing by cortex) but there seems to be no possibility to access the Pad Control Registers from PRU
    - uart to target is handled in target, not pru, correct?
    - spi dac ~ 25 MHz or 8 ticks / bit, adc ~17 MHz or 12 ticks / bit
    - should the current controller be replaceable? current jumpers almost allow it
    - there is no switch for who drives the output-shunt (mppt or I2C-LDO), is it safe?

most controversial (possible) changes to current platform
- Power stage
    - Var A: remove recording (and mppt-conv) and simplify power-stage with virtual Converter (recorder can be a separate pcb, device)
    - Var B: make converter modular (capelet)
    - Var C: keep everything like before + make MPPT-Conv bridgeable (EMU-V-DAC will be connected to second shunt)
- host-cpu offers SWD, JTAG, GPIO, SPI, UART to target (unified pins), PRU is recorder and power-supply-emulator
- switch to beaglebone AI "just" because it has GBE and a more capable power-in (usb type c)
- with vCap in mind, PRU would be best replaced by a teensy 4.1 (lots of iO, SPI with DMA & FIFO, FPU, 600 MHz, 1 MB RAM)
- switch to more more complex CAD-Software (see sub-chapter in concept_hw)


Testbed
-------

- when ZIH has vLAN ready: test if infrastructure of university is sufficient, mostly regarding ptp
- for node-distribution
    - talk with the leaders of groups that occupy offices
    - examine offices with IT-Admin
- measure link quality around cfaed-floors


Hardware - mostly shepherd Cape
-------------------------------

- target-relays/switches : multi-pin, low leakage, high data-rate
  - current uni-direction (gpio) -> SN74LV4T125PWR -> are diodes needed?
  - current bi-direction (uart, swd) -> TXB0304RUTR
- power-switches: low leakage
- level-changer: high speed, low-power, possible combination with switch / programmable
- find large pin-count gpio-switch (target-selector)
- is there a better power-path?
  - find reason for substractor (EMU-I)
  - why is uni-dir level switcher not on vdd-target -> it could get into undefined state
- draw digital version of float chart for power-stage
   - where is V_CREF coming from, or is it flowing backwards from VOC_SAMP?
   - is there a possibility that (CV)-LDO drives against MPPT-Converter in a unwanted state?


Software - RealTime-Code
------------------------

- does beaglebone AI with TI AM5729 offer more pins for PRU? https://www.ti.com/product/AM5729
- PRU replacement? FPGA, CPLD would be overkill, but what is with a teensy 4? lots of iO, SPI with DMA, FPU, 600 MHz
    - https://www.pjrc.com/store/teensy40.html
- fix device tree for current beagle-kernel
- find a better name for vCap, like vEH, vPwr

Software - Python
-----------------

- figure out a system to bulk-initialize scenario, measurement, but also individualize certain nodes if needed
   - build "default" one and deep-copy and individualize -> this could be part of a test-bed-module-handler
      - test-bed instantiates beaglebone-nodes [1..30] and user can hand target and harvest module to selected nodes
   - shepherd herd -> yaml -> per node config

Software - OpenOCD
------------------

- check for compatibility jtag, swd, spy-by-wire to new target ICs (eventually tunneled through PRU)
   - nRF52 (DFU / USB, SWD)
   - STM32L4 (SWD)
   - MSP430, MSP432, CC430 (JTAG, Serial, USB, Spy-By-Wire)
- currently not routed through PRU, just normal beagle-GPIO
- bring https://github.com/geissdoerfer/openocd/commits/am3358gpio mainline
    - git https://sourceforge.net/p/openocd/code/merge-requests/?status=open
    - gerrit http://openocd.zylin.com/#/q/status:open


Software - Web-Interface
------------------------

- security concept needed if interface should be globally accessible
