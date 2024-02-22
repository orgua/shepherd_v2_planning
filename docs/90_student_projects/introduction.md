# Introduction

The [issue-section](https://github.com/orgua/shepherd/issues) of the main-repo contains a roadmap of future implementations that are planned for the testbed. A subset is suitable for student projects. Some even qualify to be used as topics for a bachelor or master thesis.

Projects with detailed sub-pages:

- (Web-) [dataviewer for recorded traces](./implement_dataviewer)
- replace [Fifo-system between userspace & pru](./improvement_for_memory_interface)

The sections below are a rough description of possible topics. [Contact us](https://nes-lab.org/) for more details.

## Concept for externalizing IO Sampling

- High-Speed, high temporal resolution (>= 1 MHz, <= 100 ns)
- FPGA or MCU as Interface in front of SBC
- optional: bidirectional (also actuating pins)
- example from Flocklab: <https://github.com/ETHZ-TEC/RocketLogger>

## Optimize Network Topology of Testbed

- find and characterize interesting topologies (multi-hop, ring, mesh, ...)
- layout-optimization to include topos as subnets (while keeping node-count small)
- bootstrapping - how to start (with smaller number of nodes)
- optional: consider different PHY (protocol or target dependent)
- link-measurements or channel characterization could be a baseline for research

## Target-Design (more practical work)

- motivation: one free port on shepherd
- what system to choose, feature-set
- survey: what is popular, missing or growing in science-community
- first orientation could be flocklab or <https://www.iot-lab.info/>
- examples for possibles PHYs: lora, wifi, 15.4, uwb
- design, validation of PCB

## Optional time-sync Strategies

- idea: when ptp and gps are out of reach
- DCF77: reference implementation using arduino and a 5 € DCF-Module: <https://blog.blinkenlight.net/experiments/dcf77/local-clock/>
  - phase-detection enables high-res time sync
  - what min error would be possible?
- alternative: lora heartbeat or similar rf-signal to sync on
- interesting for far away nodes (uwb) ⇾ distant subnets that can't use ptp via LAN
- how to correct for error introduced by physical distance?
- topics could also include: antenna design, module concept, control loop optimization

## Cape Redesign - HowTo - Feasibility-Study

- characterize constraints
- survey of SBC with included feature-set

## Concept for measuring / recording energy environments

- statistically valid data
- how to scale (50 .. 80 .. 100 nodes)
- sounds easy, but goes in depth and is on master-level
