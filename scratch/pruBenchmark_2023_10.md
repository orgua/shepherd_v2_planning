## PRU0 

- has access to analog Frontend (DAC, ADC)
- fixed 10 us schedule

### time-budget - virtual converter

 100 ns Trigger ADC Reading
 350 ns Misc (Timestamping for util-monitor)
6600 ns Sampling (VSrc)
        1600 ns get IV-Values from Pru0, (harvester), calc_inp_pwr
         860 ns ADC-Reading
        3200 ns calc_out_pwr, update_cap_storage
         750 ns DAC-Writing
         170 ns write IV to ring

 160 ns check conditions
 780 ns Buffer-swap (every 10us)
OR
  90 ns check conditions
 120 ns kernel-COM 

-> 7990 ns 

## PRU1

- gpio rw-control (includes batOK remote trigger for pru0)
- loose tasks, ranked by prio
  - gpio-sampling
  - timestamping for kernel
  - trigger remote bufferswap (pru0)
  - trigger remote sampling (pru0)
  - read IV-Values from RAM-Buffer (for pru0)
  - process pru0-util-monitor

### time budgets

 165 ns gpio-sampling READ (!!! max blind time is )
     160 ns min duration blind
     195 ns mean duration blind
    5970 ns max duration blind - OLD (write, events & ram-read)
    3718 ns max duration blind - with ram-read-split
     660 ns write

 180 ns Event1 - timestamping for kernel (every 100 ms, 1 ms bevor E2)
 304 ns Event2 - trigger remote bufferswap on pru0 (every 100 ms)
 210 ns Event3 - trigger remote sampling on pru0 (every 10 us)
 620 ns read IV-Values from RAM-Buffer for pru0 (every 10 us)
        525 min, 620 mean, 5350 max (both at once)
        270 min, 310 mean, 3500 max (split reads)

 xxx ns process pru0-util-monitor

## optimizations

- split ram-reads until new ring-buffer is implemented (DONE)
  - 115k uart from waveform looks much better, but still has some symbol-errors
- implement new Ring-buffer
  - allows reading both values simultaneously
  - still violates RT-constraint when on pru0
- let pru0 handle its own timers (E2, E3)
- find a way to save gpio faster ?? 660 ns for write seems too much, but timestamping takes time
- gpio-actuation - just very low tech - 1 pin - max 1 set per 0.1s

## new firmwares

### static voltage, only current-tracing 

pru0 
- ~ 1000 ns ADC & Store
- could actuate gpio now (cpu-registers)

pru1
- does not have to read from RAM


## setup

- pru0: monitor debug-pins & CS of ADC & DAC
  - pru00 toggles on every buffer-activation
  - pru01 is high in sampling() and during kernel-com() & buffer-swap()
- pru0: has a debug-system, just activate the sub-system
  - gpio, events, ram-reads

```Shell
make clean
make
sudo make install
sudo shepherd-sheep -v fix
sudo shepherd-sheep -v run /etc/shepherd/target_device_test3.yaml
```
