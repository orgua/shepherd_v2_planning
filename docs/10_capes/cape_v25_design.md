# Cape PCB v2.5

Status 2024-02: still not produced - maybe skipped for switching platform

# Implemented Changes

- lower current-limiting resistors from 470 R to 240 R (see new target)
- emu U32 replace OPA189 bei OPA388
- LP for InAmp AD8421 -> 80kHz with 2x 100R, +2x 1nF to GND
- change invNr-Sys to solid white rect
- Emu - use 10mV Ref directly, without Switch
- Rec - use GND as Ref directly
- stabilize 10 mV -> 1uF increase to 2x 10uF, 2R increase to 10R
- replace electrolytic Caps by MLCC (Optionals on Backside)

-> implemented in V2.5 - https://github.com/orgua/shepherd_v2_planning/tree/main/PCBs/shepherd_cape_v2.5a

- xp: add 150R as LP for Emu-InAmp (~50kHz)
- xp: double C141, C3 (Emu around U32 Opa)
- xp: 10mV Ref input - C149 - 1uF + 10uF
