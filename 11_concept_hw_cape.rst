Concept - Hardware - Shepherd-Cape
==================================

-> mostly documentation of changes to V1.x

- shepherd Cape
   - fixed & robust power-connector and possiblity to switch system on/off, reverse polarity - detection
   - external (SMA) connector for PPS (in addition to Link from GPS)
   - bridge dc-converter and capacitor (to allow emulation)
   - easier (dis)assembly by reducing / removing pin-header-forwarding (only take what is needed)
   - compatibility with and optimization for beagle AI
- Capelet - System
   - get rid of pin-headers for b2b / mezzanine - interconnect -> molex, flex cable, hirose ...
   -
- GPS Capelet
   - look for similar gps-module with external antenna support
   - backup power (LiPo / Supercap)
- target Capelet
   - allow a second target -> switch inputs and power

