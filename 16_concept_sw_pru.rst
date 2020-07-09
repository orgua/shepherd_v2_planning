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
   - maybe more useful than disassembling via goldbolt
- emulation of DC-converter and capacitor:
   - if compiler allows newer c++-features it would be perfect to use constexpr-fn to pre-calculate LUTs
- Side-Note:
   - PRU has two 200 MHz cores, 1 op per tick, no division, 8 kB RAM per Core, 12 kB shared RAM, and access to host memory (expensive wait)
- one PRU shouldein PRU Core sollte Zeitkritische Dinge erledigen, bsp. samplen in den Ringpuffer und in den gemeinsamen speicher schreiben → die andere Core sollte für den Transfer in den Hauptspeicher sorgen
