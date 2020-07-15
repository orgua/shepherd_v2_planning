Concept - Software - RT Units
=============================

- SPI, use dedicated hardware and not bit-banging
   - uart could also be a candidate for dedicated hardware
- superficial code-analyse
   - ringbuffer can be optimized
      - modulo is expensive and not needed
      - write more than 1 char if possible (both adc-values would be better)
      - int-return is mostly const and not needed
      - context switch by function calls are expensive (inline, variables via const ref)
- try to benchmark the loop, maybe use timer, counter with min, max, mean
   - maybe more useful than disassembling via godbolt
- vCap, emulation of DC-converter and capacitor:
   - it would be perfect to use constexpr-fn to pre-calculate LUTs (ti compiler not capable, see below)
- one PRU should do time critical things, i.e. sampling into ringbuffer in shared PRU-Memory → other PRU-Core should handle transfer to cpu-memory

BeagleBone PRU Features, Comparison
-----------------------------------

PRU ICSS `(High level Overview <https://elinux.org/Ti_AM33XX_PRUSSv2>`_
    - 200 MHz cores
    - one 32bit-op per cycle
    - no division
    - 8 kB RAM per Core
    - 12 kB shared RAM
    - 3 banks of Scratch-Pad (=3x30x 32-bit registers) directly between the cores, 1Cycle Access
    - access to host memory, L3 interconnect (expensive wait, see benchmark below)
    - INTC, 64 events, 10 channels
    - access to host periphery (QSPI, GPIO, even USB), ~ 40 cycles read latency

`TI Wiki <https://processors.wiki.ti.com/index.php/PRU-ICSS>`_ contains datasheets for various sub-topics
    - PRU C/C++ optimization guide, presentations,
    - Subprocessor documentation
    - `projects <https://processors.wiki.ti.com/index.php/PRU_Projects>`_, notably
        - PyPRUSS (programming PRUs on beaglebone black),
        - libpruio (high speed data handling),
        - BeagleLogic (100 MHz, 14CH Logic Analyzer),
        - High Speed data aquisition

latency benchmarks (source: "sprace8a.pdf")
    - writes take normally 1 cycle, reads 2 to 14 (UART) cycles local, reads 30 - 40 cycles global (periphery)
    - transfer shared RAM to DDR 5 cycles / 4 byte, to 65 cycles / 128 byte
    - transfer DDR to shared RAM 47 cycles / 4 byte, 107 cycles / 128 byte -> prefer large chunks

PRUs (ICSS, ICSSG) Supported techniques (`feature comparison source <http://www.ti.com/lit/sprac90>`_)
    - mostly called (enhanced) EGPIO:
    - 16 bit parallel capture input for GPIO
    - 28 bit shift input
    - 3 Ch peripheral interface (should be enough for SPI) (on ICSS device dependent)
    - Shift output
    - dedicated UART (with 16bit FIFO, 192 Mbps)
    - eCAP (enhanced Capture)
    - IEP (industrial Ethernet)
    - 2x MII_RT (media independant interface), MDIO (management Data IO)


Beagle Black -> AM3358
    - 1 PRU = 2 Cores, 200 MHz, 8 KB IRAM (instructions) per Core, 8 KB DRAM per core, 12 KB shared DRAM, 17/17 GP-Inp, 16/16 GP-Out, 3 Banks Scratch Pad
    - eGPIO on register x30000 / pins pr1_pru0_pru_r31[16:0] (INP) and pr1_pru0_pru_r30[15:0] (OUT) for PRU0, same for PRU1 with changed register name
    - UART on register x28000 / pins pr1_uart0_rxd/txd/cts_n/rts_n
    - eCap on pr1_ecap0_ecap_capin_apwm_o -> capture input or aux PWM out
    - MDIO has an IO pin pr1_mdio_data

Beagle AI -> AM5729
    - 2 PRU, 200 MHz, 12 KB IRAM per Core, 8 KB DRAM per Core, 32 KB shared DRAM, 21/21 GP-Inp, 21 GP-Out, 3 Banks Scratch Pad
    - same peripherals as AM3358

Possible Compilers
    - ti c compiler, supports c99, asm and c++2003 (https://www.ti.com/tool/TI-CGT#PRU)
    - gcc pru port, in mainline now, (https://github.com/dinuxbg/gnupru/wiki)

Program - Optimizations
-----------------------

PRU Good Practice
    - passing of arguments: 16 registers to pass 32-bit each
    - auto-incrementing loops are without overhead [for (i = 0; i < X; ++i)]
    - O2 tries to rewrite div-const-int into reciprocal mult
    - mixing of asm, c, c++ can bring trouble when activating optimizations
    - a more efficient (single instruction) access to local memory in the lower 16-bits (__near), can be used
    - variables in shared memory always "volatile"
    - const helps, at least to save RAM (if defined at compile-time)

CCS Compiler Switches
    - opt_level=[1-4]
    - opt_for_speed=[0-5]
    - fp_mode=[strict] -> disable fp-usage
