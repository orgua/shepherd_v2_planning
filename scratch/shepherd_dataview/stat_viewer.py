# -*- coding: utf-8 -*-
import os
from pathlib import Path

import numpy as np
import h5py


if __name__ == '__main__':

    flist = os.listdir("./")
    for file in flist:
        if not os.path.isfile(file):
            continue
        if not "h5" in Path(file).suffix:
            continue
        with h5py.File(file, "r") as hf:

            dc = dict()
            for var in ["voltage", "current"]:
                ds = hf["data"][var]
                # Apply the calibration settings (gain and offset)
                dc[var] = ds[:] * ds.attrs["gain"] + ds.attrs["offset"]
                #dc[var][dc[var] < 0] = 0
                dc[var][ds[:] <= 0] = 0  # adc 0 gets replaced by converted 0

            if abs(np.max(dc["current"]) / np.min(dc["current"])) < 40:
                continue
            dc["current"] = dc["current"][1:] - dc["current"][:-1]

            cmean = np.mean(dc['current']) * 1e3
            cmin = np.min(dc["current"]) * 1e3
            cmax = np.max(dc["current"]) * 1e3
            cstd = np.std(dc["current"]) * 1e3
            print(f"{file}: \t current/mA mean={cmean:.6f}, min={cmin:.6f}, max={cmax:.6f}, std={cstd:.6f}")
