Concept - Software - Web Interface
==================================

Functions
---------
- user-management, permission / role management
- Quota
- authentication via external service like OAuth (i.e. Github) (if possible)
- Upload: Scripts, Harvesting-Traces, Firmware
- Scratch-Area for user-data
- integrated pre-tests for measurement: test for plausibility, pre-run in software (abstract virtual hardware)
- scheduler for measurement, time to prepare and follow up (data transfer, conversion, compression, ...)
- results downloadable by user, for a certain time (no hording)
- feedback via e-mail - measurement start, data available, error, shortly before deletion
- (optional) grafana-visualisation
- documentation and instructions


Implementation
--------------
- possibly python based / django, flask
- django offers the most, is flexible, modular and easy to extend
    - admin-interface
    - authentication (also oauth client), accounts
    - session-management
    - sub-websites with html-templates
    - -> security seems to be OK, attach surface is big, but >v3.0 seems to be mature
- basic implementation could be similar to https://github.com/fkt/36c3-junior-ctf-pub (web-interface for a ctf, that didn't get compromised)
- database: timescaleDB, influxDB, postgreSQL
- data-exchange: protobuf, rabbitMQ, RPC
- API: rest
- (prio) allow scripted workflow -> yaml -> rest ->
    - this could also be the base for the web-page-interface

TODO
----
- compare with "12_concept_.." (and notes)
- compare elastic against influx, no support for nanosec?
- benchmark server (disks / ram)
- offer predefined energy-patterns (on/off, diode, different converters (boost, buck/boost))
- design-choices for later
    - does shepherd need databases for immediate (deep)analysis of result
        - alternative: provide post-scripts that filter data for key-parameters (benchmark-management)
    - data hording or economical use of space?
    - what else ?????
