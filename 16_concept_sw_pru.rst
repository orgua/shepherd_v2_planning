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
- try to benchmark the loop, maybe use timer
   - maybe more useful than disassembling via godbolt
- emulation of DC-converter and capacitor:
   - if CCS-compiler allows newer c++-features it would be perfect to use constexpr-fn to pre-calculate LUTs (seems to be limited to c99, c++2003)
- Side-Note:
   - PRU has two 200 MHz cores, 1 32bit-op per tick, no division, 8 kB RAM per Core, 12 kB shared RAM, and access to host memory (expensive wait)
- one PRU should do time critical things, i.e. sampling into ringbuffer in shared PRU-Memory → other PRU-Core should handle transfer to cpu-memory

Program - Optimizations
-----------------------

- Beagle Black -> AM3358
    - 2 Cores, 200 MHz, 8 KB IRAM per Core, 8 KB DRAM per core, 12 KB shared DRAM, 17/17 GP-Inp, 16/16 GP-Out, 3 Banks Scratch Pad
    - UART, eCAP, IEP, 2x MII_RT, MDIO
- Beagle AI -> AM5729
    - 2 Cores, 200 MHz, 12 KB IRAM per Core, 8 KB DRAM per Core, 32 KB shared DRAM, 21/21 GP-Inp, 21 GP-Out, 3 Banks Scratch Pad
    - same peripherals as AM3358
- `TI Wiki <https://processors.wiki.ti.com/index.php/PRU-ICSS>`_ contains datasheets for various sub-topics
    - PRU C/C++ optimization guide, presentations,
    - Subprocessor documentation
    - `projects <https://processors.wiki.ti.com/index.php/PRU_Projects>`_, notably
        - PyPRUSS (programming PRUs on beaglebone black),
        - libpruio (high speed data handling),
        - BeagleLogic (100 MHz, 14CH Logic Analyzer),
        - High Speed data aquisition
- PRUs (ICSS, ICSSG) Support techniques listed below (`feature comparison source <http://www.ti.com/lit/sprac90>`_
    - 16 bit parallel capture input for GPIO
    - 28 bit shift input
    - 3 Ch peripheral interface (should be enough for SPI) (on ICSS device dependent)
    - Shift output
    - dedicated UART, eCAP, IEP, 2x MII_RT, MDIO
- PRUs have
    - passing of arguments: 16 registers to pass 32-bit each
- CCS Compiler Switches
    - opt_level=[1-4]
    - opt_for_speed=[0-5]
    - fp_mode=[strict] -> disable fp-usage
