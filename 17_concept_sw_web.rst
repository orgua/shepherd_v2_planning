Concept - Software - Web Interface
==================================

Functions
    - user-management, permission / role management
    - Quota
    - authentication via external service like OAuth (i.e. Github) (if possible)
    - Upload: Scripts, Harvesting-Traces, Firmware
    - Scratch-Area for user-data
    - integrated pre-tests for measurement: test for plausibility, pre-run in software (abstract virtual hardware)
    - scheduler for measurement, time to prepare and follow up (data transfer, conversion, compression, ...)
    - results downloadable by user, for a certain time
    - feedback via e-mail - measurement start, data available, error, shortly before deletion
    - grafana-visualisation
    - documentation and instructions

Implementation
    - possibly python based / django
    - django offers the most, is flexible, modular and easy to extend
        - admin-inferaces
        - authentication (also oauth client), accounts
        - session-management
        - sub-websites with html-templates
        - -> security seems to be OK, attach surface is big, but >v3.0 seems to be mature
    - basic implementation could be similar to https://github.com/fkt/36c3-junior-ctf-pub (web-interface for a ctf, that didn't get compromized)
