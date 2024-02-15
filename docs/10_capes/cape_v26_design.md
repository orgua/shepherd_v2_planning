# Cape v2.6 - PCB Changes (WIP)

## TODO NextGen

- change ADC to higher resolution?
- change OP-Ampdriver to higher current output? Double Opa388?
- make system modular?
- direction pin GPO:3 for leveltranslators is named strangely
- rename Recorder ⇾ Harvester
- maybe switch to rpi Cm4 Platform

### PWR-Board

- 3 inputs (Enable, 5V, <= 17V)
- 4 Output (L3V3, -6V, L5, 10V)
- GND

### EMU / HRV Board

- GND
- 10 inputs (4 voltages, 3 SPI, 3 SPI-CS,
- 4 outputs (2 Rails, 2 Feedback)
- (generalized) - no enable needed

### Advantages

- would allow specialized BeagleBones (could also easily work on a teensy)
- sub-pcbs are reusable
- harvesting with a cheaper network of nrf52 + pwr + hrv (rf-syncronized)
