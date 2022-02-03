Shepherd Cape v2.3 - Performance
================================

Tested
------

- WD is fine now -> gets turned on
- BB boots with Shepard Cape on
- BB-powered boot works, but turning Cape on crashes the 5V Rail (P9-7/8)


Profiling Frontends
-------------------

00

- lab / bench supply powered -> for all the following, if not stated otherwise

01

- raised 10V rail from 9V7 to 10V41 (R 240k to 270k) -> without benefit

02

- C101 100 uF destroyed (parallel to 1 mF) on cape-input
- L3 shorted
- voltages measurement seems to have worsended by 1 % BUT current measurement improved by 3 % (max-error)

03

- reverted to 9V7 and overhauled the profiling-system offering a short and full profile (not completely comparable)
- measure full and short profile as new baseline

04

- Shunt-Buffer-Cap C6 increased from 100 nF to 470 nF -> lowpass 170 kHz
- voltage measur




TODO
-----

- fix BB-Powered Mode
- determine final fixed for EMU
- determine final fixes for HRV
- test WD restarting BB
- determine stencil-thickness -> shrink some paste-mask-pads


Changes in Layout
-----------------

- 74LVC2T45GS has too small pads -> prone to errors (very hard to see, but shorts under IC in all cases)
- Force proper Fanout with Neck-Down -> EC seems to extend solder mask expansion on its own
- feducials can go, are on outer frame
- more pads for Caps on backside
