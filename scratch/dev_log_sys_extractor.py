from pathlib import Path
from typing import NoReturn
import h5py
import numpy as np
from datetime import datetime

# data-structure-assumptions:
# groups have datasets for 'time' and various custom data (ie. 'voltage'
# datasets have attributes for "unit" and "description" (string-message-logs are an exception)
# -> "unit" - currently unused, but should name the SI-Units for the data
# -> "description" - can contain name, unit or list of that for a pretty csv-header
#       -> example for multidimensional dataset: "cpu_util [%], io_read [n], nw_recv [byte]"


def csv_writer(file_path, h5_group, h5_datasets: list, separator: str = "; ") -> int:
    if len(h5_group["time"]) < 1:
        return 0
    ds_time = h5_group["time"][:].astype(float) / 1e9
    header = h5_group["time"].attrs["description"] + separator + \
             separator.join(
                 [h5_group[content].attrs["description"].replace(", ", separator) for content in h5_datasets])
    with open(file_path, "w") as csv_file:
        csv_file.write(header + "\n")
        for i in range(len(ds_time)):
            timestamp = datetime.utcfromtimestamp(ds_time[i])
            csv_file.write(timestamp.strftime("%Y-%m-%d %H:%M:%S.%f"))
            for var in h5_datasets:
                values = h5_group[var][i]
                if isinstance(values, np.ndarray):
                    values = separator.join([str(value) for value in values])
                csv_file.write(f"{separator}{values}")
            csv_file.write("\n")
    return len(ds_time)


def log_writer(file_path, h5_group, h5_datasets: list) -> int:
    if len(h5_group["time"]) < 1:
        return 0
    ds_time = h5_group["time"][:].astype(float) / 1e9
    with open(file_path, "w") as log_file:
        for i in range(len(ds_time)):
            timestamp = datetime.utcfromtimestamp(ds_time[i])
            log_file.write(timestamp.strftime("%Y-%m-%d %H:%M:%S.%f"))
            for var in h5_datasets:
                try:
                    message = str(h5_group[var][i])
                except OSError:
                    message = "[[[ extractor - faulty element ]]]"
                log_file.write(f": {message}")
            log_file.write("\n")
    return len(ds_time)


def group_extractor(file: Path, group: str, datasets: list, only_log: bool = False) -> NoReturn:
    if file is not None:
        file = Path(file)
    if not isinstance(datasets, list):
        datasets = [str(datasets)]
    with h5py.File(file, "r") as hf:  # TODO: this solution is sleek, but does not allow subgroups
        if group in hf:
            ending = ".log" if only_log else ".csv"
            out_file = file.parent / (file.stem + "_" + group + ending)
            if only_log:
                n = log_writer(out_file, hf[group], datasets)
            else:
                n = csv_writer(out_file, hf[group], datasets)
            print(f"[Extractor] found n={n} elements in '{group}'-group")
        else:
            print(f"[Extractor] did not find '{group}'-group")


def h5_extractor(file: Path) -> NoReturn:
    group_extractor(file, "system", ["cpu_util", "ram_util", "io_util", "net_util"])
    group_extractor(file, "dmesg", ["message"], only_log=True)
    group_extractor(file, "timesync", ["values"])
    group_extractor(file, "exceptions", ["message"], only_log=True)
    group_extractor(file, "uart", ["message"], only_log=True)


if __name__ == "__main__":
    h5_extractor("./test_sys_log.h5")
