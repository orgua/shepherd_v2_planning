Profiling of Frontends
----------------------

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







11 Harvester

- baseline w/o voltage sense
- R22 100k causes the big offset!

12 R22 from 100k to 1k

- 11k ADC-Value down to 182
- start still at 2-5 uA
- 3-40n std-dev for current

13 C140 from 22pf to 1nF (160 kHz)

14 C140 to 2nF

15 C35 removed, 100nF

16 ADC_V, TP6 gets 10nF

17 Bake off

18
