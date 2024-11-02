from pathlib import Path

import pandas as pd

path_there = Path(__file__).parent / "capacitors_real"
cap_charge = [
    path_there / "cap1_s1_chg.csv",
    path_there / "cap1_s2_chg.csv",
    path_there / "cap2_s1_chg.csv",
    path_there / "cap2_s2_chg.csv",
    path_there / "cap3_s1_chg.csv",
    path_there / "cap3_s2_chg.csv",
]
cap_discharge = [
    path_there / "cap1_s1_dis.csv",
    path_there / "cap1_s2_dis.csv",
    path_there / "cap2_s1_dis.csv",
    path_there / "cap2_s2_dis.csv",
    path_there / "cap3_s1_dis.csv",
    path_there / "cap3_s2_dis.csv",
]
cap_selfdis = [
    path_there / "cap1_selfdis.csv",
    path_there / "cap2_selfdis.csv",
    path_there / "cap3_selfdis.csv",
    # varying charging-durations
    path_there / "cap1_selfdis_charge010s.csv",
    path_there / "cap1_selfdis_charge020s.csv",
    path_there / "cap1_selfdis_charge050s.csv",
    path_there / "cap1_selfdis_charge100s.csv",
    path_there / "cap1_selfdis_charge200s.csv",
    path_there / "cap1_selfdis_charge400s.csv",
    path_there / "cap1_selfdis_charge800s.csv",
    path_there / "cap1_selfdis_charge010s_check.csv",
]

cap_cyclic = [
    path_there / "cap1_cycle_3V0_to_5V0_40ms.csv",
    path_there / "cap1_cycle_3V0_to_5V0_228ms.csv",
]

cap_real_chg = []
for path in cap_charge:
    cap = pd.read_csv(path, sep=",", decimal=".")
    cap = cap.rename(columns={"Time [s]": "time", "Dbg10": "voltage"})
    cap_real_chg.append(cap)

cap_real_dis = []
for path in cap_discharge:
    cap = pd.read_csv(path, sep=",", decimal=".")
    cap = cap.rename(columns={"Time [s]": "time", "Dbg10": "voltage"})
    cap_real_dis.append(cap)

cap_real_self = []
for path in cap_selfdis:
    cap = pd.read_csv(path, sep=",", decimal=".")
    cap = cap.rename(columns={"Time [s]": "time", "Dbg10": "voltage"})
    cap_real_self.append(cap)

cap_real_cyclic = []
for path in cap_cyclic:
    cap = pd.read_csv(path, sep=",", decimal=".")
    cap = cap.rename(columns={"Time [s]": "time", "Dbg10": "voltage"})
    cap_real_cyclic.append(cap)