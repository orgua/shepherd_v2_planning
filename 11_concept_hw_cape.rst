Concept - Hardware - Shepherd-Cape
==================================

-> mostly documentation of changes to V1.x

- shepherd Cape
   - fixed & robust power-connector and possibility to switch system on/off, reverse polarity - detection
   - external (SMA) connector for PPS (in addition to Link from GPS), possible switch / level-changer -> record via PRU
   - bridge dc-converter and capacitor (to allow emulation)
   - easier (dis)assembly by reducing / removing pin-header-forwarding (only take what is needed)
      - reduce or bundle pins to shepherd (or another way to make disassembly easier)
   - compatibility with and optimization for beagle AI (dedicated concept-file)
   - addressable i2c - flash storage for calibration and distinction
      - all flashes can share same bus, shepherd gets first address, target second, ...
   - current load solution seem a bit overkill and brings non-linearity with the LEDs
- Energy-Recorder/Emulator:
      - easiest case: replay / emulation could "just" rely on voltage-DAC and target-current-draw measurement?
      - current implementation: recording with U/I before DC-Conv, emulation with U/I meas. after DC-Conv
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
   - if usb to target (via cable), then make it off-switchable
- general-purpose capelet (port)
   - if pins to pru suffice
- beaglebone timekeeping
   - test high precision, temperature compensated crystal oscillator

Concept - Hardware - PinOuts
============================

- PRUs seems to have 28 Pins accessable (PRU0 15, PRU1 13), with the current occupation
   - 2Pin: target UART (on dedicated uart-pins)
   - 1Pin: target SWDCLK (seems to use normal gpio-fn, SWDIO on regular gpio/clkout2)
   - 4Pin: target GPIO
   - 5Pin: SPI to DAC, ADC (on dedicated SPI-pins)
   - 1Pin: Led1 PRU
   - 1Pin: LED2 User Space
   - 1Pin: select LOAD Pru
   - 1Pin: ADC RST/PDN
   - [3Pin: Debug-Pins (will be reserved by dts, but not in layout)]
   -> leaves 9 (+3) PRU controllable pins on beagle Black
- PRU Tasks
   - PRU0 seems to handle SPI, Leds, load select
   - PRU1 seems to handle target gpios, uart, adc-reset

Concept - Hardware - Shepherd V1 Functionality
======================================

- see beagle-pinout in excel-sheet (12_concept_..)
- Interfaces
   - Beaglebone 2x46 Pins
   - button + led
   - harvesting-source (VIn, 80%)
   - Energy-Storage
   - Target (4 GPIo, SWD, UART, VCC, BatOK)
   - Jumper to tap into current path
- fixed supply voltage for target
   - DAC6571IDBVR -> i2c-DAC,
   - TPS73101DBVR -> LDO
   - TMUX1101DCK -> Switch 1Port 1Endpoint
- LM27762DSSR -> low_noise pos&neg analog voltage (VDD, VSS) for some OP-Amps
- CAT24C256WI-GT3 -> i2c-EPROM
- Target IO
   - TXB0304RUTR -> BiDir level converter for target uart & swd (switchable)
   - LMP7701MF -> OP-Amp, voltage buffer
   - SN74LV4T125PWR -> UniDir level converter, high imp (Sep. Switchable, not used)
- BQ25504_RGT_16 -> Voltage Reg with MPPT
   - ADG736LBRMZRM_10-L -> Analog Switch 2Port 2Endpoints
- ref Voltage emulation
   - DAC8562_DGS_10 -> 2CH SPI-DAC
   - OPA2388DGK8_L -> dual OP-Amp, Voltage2Current Converter
   - LMP7701MF -> OP-Amp, bias subtractor
- current & voltage measurement (harvesting & load)
   - ADS8694TSSOP38 -> 4CH SPI-ADC
   - OPA2388DGK8 -> OP-Amp, 3x voltage buffers
   - AD8422BRMZ -> precision OP-Amp, 2? Ohm Shunt Amperemeter
- dummy load
   - OPA2388DGK8_L -> dual OP-Amp, voltage buffer & Schmitt Trigger to switch on two LEDs
   - ADG849YKSZ-REELKS_6-L -> Switch 1Port 2Endpoints
- harvesting
   - G3VM-31HR22SOP -> low on-res switch to disconnect harvester
   - AD8422BRMZ -> precision OP-Amp, 2? Ohm Shunt Amperemeter

Concept - Hardware - eagle project
==================================

- improvements to project
- allow proper DRC and ERC by redefining pins in symbol-lib
    - NC - not connected
    - In - input
    - Out - output
    - IO - in/out
    - OC - open collector or open drain
    - Hiz - high impedance output
    - Pas - passive (resistor, etc)
    - Pwr - power pin (supply input)
    - Sup - supply output (also for ground)
- swap-level (>0) allow easy pin-changes in later design stages (pins with same swap level)
- function -> inverted (dot), clock, invClk
- add parameters for partnumber, order-number (mouser, digikey), some key specs (forward current, max power, max voltage, ..), price -> eagle does not seem to support that at all?!?
   - reason to switch to kicad?
- minimize BOM
