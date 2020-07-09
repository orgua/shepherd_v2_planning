Concept - Hardware - Shepherd-Cape
==================================

-> mostly documentation of changes to V1.x

- shepherd Cape
   - fixed & robust power-connector and possibility to switch system on/off, reverse polarity - detection
   - external (SMA) connector for PPS (in addition to Link from GPS), possible switch / level-changer
   - bridge dc-converter and capacitor (to allow emulation)
   - easier (dis)assembly by reducing / removing pin-header-forwarding (only take what is needed)
   - compatibility with and optimization for beagle AI (dedicated concept-file)
   - addressable i2c - flash storage for calibration and distinction
      - all flashes can share same bus, shepherd gets first address, target second, ...
- Capelet - System
   - get rid of pin-headers for b2b / mezzanine - interconnect -> molex, flex cable, hirose ...
   - support for addressable i2c-flash for distinction and configuration
   - maybe rotate capelets, so they stick orthogonal on shepherd (would benefit antenna)
- GPS Capelet
   - look for similar gps-module with external antenna support
   - backup power (LiPo / Supercap)
- target Capelet
   - allow a second target -> switch inputs and power (could also lead to a third if space is available
   - allow different targets (probably limited by software)
   - maximize gpio-count between beagle and target, parallel usage also for programmer-pins and uart if possible / needed (and spi if feasable)
   - fast level-changer for >= 1 MBaud UART
   - bidirectional gpio-connection, tri-state (input, output, disconnected)
   - possible usb-interface (has to be cable based, beagle does not offer usb on pin-header)
   - if there is low cost, make power-connection switchable (for on-off-pattern if power-emulation does not work)
- general-purpose capelet (port)
   - if pins to pru suffice
- beaglebone timekeeping
   - test high precision, temperature compensated crystal oscillator

Concept - Hardware - Beaglebone Pinout
======================================

- TODO
