# Sync-Analyzer

Collection of tools to analyze Sync-behavior, recorded with saleae logic pro

## HowTo

### Hardware

- connect channels + Ground
- activate sync mode (sudo shepherd-sheep pru sync)

### Capture with Logic 2 Software

- select used channels (Digital, NOT Analog)
- select highest sampling Rate (500 MS/s)
- Range: 3.3+ Volts
- Timer: 100s

### Prepare data for this tool 

- Logic 2 -> File -> Export Data
- select channels: 1-3 ???
- Time Range: All Time
- Format: CSV
- DON'T use ISO8601 timestamps
- Export and rename file to meaningful description

### Expected Data-Format

```csv
Time[s], Channel 0, Channel 1
0.000000000000000, 1, 1
7.642110550000000, 1, 0
```

Note: Name of channels is ignored
