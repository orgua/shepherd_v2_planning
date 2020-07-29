Shepherd-Sheep
--------------

- options and their paramters
    - eeprom
    - emulate
    - record
        - no_calib: bool            -> TODO: why negation, use default
        - force: bool               -> overwrite exiting file
        - init_voltage: float
        - load: artificial, node
        - mode: harvesting, load    -> TODO: make more clear, this one is recorded
        - output: string-folder /var/sheph
    - targetpower
        - on/off
        - --voltage: float
    - run
    - rpc, launcher
- parameters
    -v verbose: int[0:2]
- mode: emulation, virtcap, debug

TODO
----

- help-output could also mention additional parameters for each option
- crash more gracefully, and earlier (ie. missing su)
- test for sudo upfront
- print current config / parameters before starting to do anything
- add timestamp to measurement data, instead of rec[.#.].h5
- notify user that ctrl+c ends the program
