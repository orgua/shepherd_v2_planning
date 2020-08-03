Beaglebone PRU
==================================

Getting started - handling PRUs (in ansible: dev_rebuild_pru.yml)::

    sudo su

    # stopping PRUs
    echo "stop" > /sys/class/remoterproc/remoteproc1/state
    echo "stop" > /sys/class/remoterproc/remoteproc2/state

    # stop and start kernel module -> warning: some states are not reset this way
    modprobe -r shepherd
    modprobe -a shepherd
    # fw gets flashed and PRUs started by module

    # test code on live system
    shepherd-sheep -vv run --config /etc/shepherd/config.yml


Code Improvements
-----------------

Toolchain

    - switch to gcc-pru, cmake?
    - update pru-software-support-package-5.4.0 to
        - official v5.7, or
        - gcc version https://github.com/dinuxbg/pru-software-support-package (fork of V4), with cherry-picking
            - updating fork: http://www.bartread.com/2014/02/12/git-basics-how-to-merge-changes-from-a-different-fork-into-your-own-branch/
    - add all gpio to lib,
    - ``global`` include should be named ``shared``

pru1

    - timer-defines in config and main are codependent, it would be easier to base them on the CLK
    - typecasting for defines, or just literals
    - clean up timecalc, it seems complicated, at least the naming of vars
    - mix of types, unsigned int VS. fixed uint32_t
    - initialize vars
    - pin writes could be optimized (combinable)
    - goto must go
    - fast loop could be more consistent if there would be a "continue" at the end of the events
    - event 3 should be on position 1 (if possible), highest prio
    - is "/2" an obvious bitshift?
    - TIMER_BASE_PERIOD / 10 seems to be a constant

pru0 - superficial code-analyse

    - ringbuffer can be optimized
    - modulo is expensive and not needed
    - write more than 1 char if possible (both adc-values would be better)
    - int-return is mostly const and not needed
    - context switch by function calls are expensive (inline, variables via const ref)
    - firmware should do self-tests for its key components
        - both cores running
        - ram-interface to cpu responsive
        - dac and adc available (chk product-id register)
        - setting voltage is measurable
        - bring it down to kernel module or (if not possible, or additionally) as blink-codes
        - show printf as kernelmsg, but don't spam too much
    - ``init_ring`` should be ``ringbuffer_init``, consistency
    - int_source is global, it shouldn't -> it can be reduced to a local bool ``got_sig_block_end``
    - free_buffers is global, but then passed by pointer
    - shared_mem is global,
    - so many magic numbers! config seems not like a config, because it needs to know what is in ``resource_table_def``


pru0 vCap

    - it would be perfect to use constexpr-fn to pre-calculate LUTs and literals for proper human readable unit conversion
    - modularize code, because vCap also contains MPPT-Converter, they could be swappable
    - unit-test critical parts (add from teensy project)
    - demystify magic numbers
    - control loop should be faster than 100 kHz, to handle sudden TX-Spikes, depending on local-input-capacitance and pwr-consumption of target-board
    - find a better name
    - allow freezing energy in capacitor

Code Questions

    - where does printf() go? down to kernel i assume
    - is there a reason for goto in pru1?
    - why lib and not normal include, monolith should be better optimized, who wrote lib? seems like a wrapper of support package
    - is timer 0 reset by pru0?
    - build system by choice? c++, cmake ok?
    - in pru0-event-loop-while: can the interrupt be cleared later? is it for all interrupts?
    - who is maintaining the sample-index in pru0? is it same as sample_counter in pru1 (no it seems to be gpio_sample_counter, but event2 is confusing)
    - there is no real ISR?
    - 1 SampleBuffer contains space for 10'000 ADC-Samples and 16'384 GPIO-Edges -> where is it stored, not in SharedMem
    - what does the ringbuffer store? char
    - compile with debug symbols for decompiler
