from pathlib import Path

import pandas as pd

path_here = Path(__file__).parent.absolute()

data: dict = {
    "MLCC Charge Run 1": "cap_charge_1.pickle",
    "MLCC Charge Run 2": "cap_charge_2.pickle",
    "MLCC Charge Run 3": "cap_charge_3.pickle",
    "MLCC Discharge Run 1": "cap_discharge_1.pickle",
    "MLCC Discharge Run 2": "cap_discharge_2.pickle",
    "MLCC Discharge Run 3": "cap_discharge_3.pickle",
}

paths_analog: dict = {name: path_here / value for name, value in data.items()}

def get_analog(path: Path) -> pd.DataFrame:
    _data = pd.read_pickle(path, compression="zstd")
    _data["Time [s]"] -= 0.016364380
    return _data

