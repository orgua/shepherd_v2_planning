Beaglebone PRU
==================================

Getting started - handling PRUs (in ansible: dev_rebuild_pru.yml)::

    sudo su

    # stopping PRUs
    echo "stop" > /sys/class/remoteproc/remoteproc1/state
    echo "stop" > /sys/class/remoteproc/remoteproc2/state

    # stop and start kernel module -> warning: some states are not reset this way
    modprobe -r shepherd
    modprobe -a shepherd
    # fw gets flashed and PRUs started by module

    # test code on live system
    sudo shepherd-sheep -vv run --config /etc/shepherd/config.yml

    # helpful when build-system was used with sudo
    sudo chown -R user ./

Code Improvements
-----------------

Toolchain

    - switch to gcc-pru, cmake?
    - add all gpio to lib,
    - ``global`` include should be named ``shared``
    - currently already implemented
        - update pru-software-support-package-5.4.0 to
            - official v5.7, or
            - gcc version https://github.com/dinuxbg/pru-software-support-package (fork of V4), with cherry-picking
            - updating fork: http://www.bartread.com/2014/02/12/git-basics-how-to-merge-changes-from-a-different-fork-into-your-own-branch/
        - fix make files
        - switch from -O2 to -O4, drop debug-symbols, nail char to unsigned, forbid float
        - add more const-correctness, less mixing of signed with unsigned (expensive typecast)
        - avoid signed int < 32bit, also expensive typecast
        - avoid a lot of far/slow register reads, but there can be done more
        - defines are better and more safe to use, explicit typing, proper usage of brackets
        - add lib-fn to access gpio-registers of sys
        - remove a lot of bottlenecks in PRUs
        - initialize vars were possible
        - printf became more userfriendly and selfexplaining
        - avoid global vars, or restrict them by "static" if possible
        - improve constness of fn-parameters throughout the code
        - expensive modulo was used at least 4 times, but never really needed
        - raise warning/hinting-level -> fix warnings and errors
        - code compiles with gcc, but linker has problems with cmake
    - statistics
        - PRU0-Codesize shrank from 161 KB to 99 KB
        - PRU1-Codesize shrank from 131 KB to 91 KB
        - GPIO-Sampling is now at around 5.5 MHz, the routine only needs 100 ns, 720 ns when writing (was 360, 1500), tasks around it are faster too
        - mutex part in buffer-exchange was reduced from 2700 ns to 460 ns)


pru1

    - timer-defines in config and main are codependent, it would be easier to base them on the CLK
    - clean up timecalc, it seems complicated, at least the naming of vars
    - fast loop could be more consistent if there would be a "continue" at the end of the events
    - is "/2" an obvious bitshift?
    - TIMER_BASE_PERIOD / 10 seems to be a constant
    - currently already implemented
        - pin writes could be optimized, bit-shift right away (combinable)
        - mix of types, unsigned int VS. fixed uint32_t
        - typecasting for defines, or just literals
        - event 3 should be on position 1 (if possible), highest prio

pru0 - superficial code-analyse

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
    - so many magic numbers! config seems not like a config, because it needs to know what is in ``resource_table_def``
    - currently already implemented
        - ringbuffer can be optimized
        - ``init_ring`` should be ``ringbuffer_init``, consistency
        - int_source is global, it shouldn't -> it can be reduced to a local bool ``got_sig_block_end``
        - free_buffers is global, but then passed by pointer
        - shared_mem is global,

pru0 vCap

    - it would be perfect to use constexpr-fn to pre-calculate LUTs and literals for proper human readable unit conversion
    - modularize code, because vCap also contains MPPT-Converter, they could be swappable
    - unit-test critical parts (add from teensy project)
    - demystify magic numbers
    - control loop should be faster than 100 kHz, to handle sudden TX-Spikes, depending on local-input-capacitance and pwr-consumption of target-board
    - find a better name
    - allow freezing energy in capacitor

Code Questions

    - is timer 0 reset by pru0?
    - build system by choice? c++, cmake ok?
    - who is maintaining the sample-index in pru0? is it same as sample_counter in pru1 (no it seems to be gpio_sample_counter, but event2 is confusing)
    - there is no real ISR?
    - 1 SampleBuffer contains space for 10'000 ADC-Samples and 16'384 GPIO-Edges -> where is it stored, not in SharedMem
    - what does the ringbuffer store? char
    - compile with debug symbols for decompiler
