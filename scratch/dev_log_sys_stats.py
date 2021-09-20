import multiprocessing
import subprocess
import time
from pathlib import Path
from typing import NoReturn
import h5py
import psutil


class LogWriter(object):

    compression_level = 1
    compression_algo = "lzf"
    sys_log_intervall_ns = 1 * (10 ** 9)  # step-size is 1 s
    sys_log_last_ns = 0

    def __init__(self, store_path: Path):

        self._h5file = h5py.File(store_path, "w")

        # Create sys-Logger
        self.sys_grp = self._h5file.create_group("system")
        self.sys_grp.create_dataset(
            "time",
            (0,),
            dtype="u8",
            maxshape=(None,),
            chunks=True,
            #compression=LogWriter.compression_algo,
        )
        self.sys_grp["time"].attrs["unit"] = "system time in nano seconds"
        self.sys_grp.create_dataset("cpu_util", (0,), dtype="u1", maxshape=(None,), chunks=True) # TODO add chunks to other data as well
        self.sys_grp["cpu_util"].attrs["unit"] = "%"
        self.sys_grp.create_dataset("ram_util", (0, 2), dtype="u1", maxshape=(None, 2), chunks=True)
        self.sys_grp["ram_util"].attrs["unit"] = "%"
        self.sys_grp["ram_util"].attrs["description"] = "[available, free]"
        self.sys_grp.create_dataset("io_util", (0, 4), dtype="u8", maxshape=(None, 4), chunks=True)
        self.sys_grp["io_util"].attrs["unit"] = "n"
        self.sys_grp["io_util"].attrs["description"] = "[read_count, write_count, read_bytes, write_bytes], total"
        self.sys_grp.create_dataset("net_util", (0, 2), dtype="u8", maxshape=(None, 2), chunks=True)
        self.sys_grp["net_util"].attrs["unit"] = "n"
        self.sys_grp["net_util"].attrs["description"] = "[bytes_sent, bytes_recv], total"


        # Create dmesg-Logger
        self.dmesg_grp = self._h5file.create_group("dmesg")
        self.dmesg_grp.create_dataset(
            "time",
            (0,),
            dtype="u8",
            maxshape=(None,),
            chunks=True,
            #compression=LogWriter.compression_algo,
        )
        self.dmesg_grp["time"].attrs["unit"] = f"system time in nano seconds"
        # Every log entry consists of a timestamp and a message
        self.dmesg_grp.create_dataset(
            "message",
            (0,),
            dtype=h5py.special_dtype(vlen=str), # h5py.string_dtype(),  # h5py.special_dtype(vlen=str),
            maxshape=(None,),
            chunks=True,
        )

        # Create timesync-Logger
        self.timesync_grp = self._h5file.create_group("timesync")
        self.timesync_grp.create_dataset(
            "time",
            (0,),
            dtype="u8",
            maxshape=(None,),
            chunks=True,
            #compression=LogWriter.compression_algo,
        )
        self.timesync_grp["time"].attrs["unit"] = f"system time in nano seconds"
        self.timesync_grp.create_dataset("values", (0, 3), dtype="i8", maxshape=(None, 3), chunks=True)
        self.timesync_grp["values"].attrs["unit"] = "[ns, Hz, ns]"
        self.timesync_grp["values"].attrs["description"] = "[master offset, s2 freq, path delay]"

        # start subprocesses for monitoring the system-states
        self.dmesg_mon_p = multiprocessing.Process(target=dmesg_monitor, args=(logger,))
        self.dmesg_mon_p.start()
        self.ptp4l_mon_p = multiprocessing.Process(target=ptp4l_monitor, args=(logger,))
        self.ptp4l_mon_p.start()

    def __exit__(self, *exc):

        if self.dmesg_mon_p is not None:
            print("[LogWriter] Terminate Dmesg-Monitor")
            self.dmesg_mon_p.terminate()
        if self.ptp4l_mon_p is not None:
            print("[LogWriter] Terminate PTP4L-Monitor")
            self.ptp4l_mon_p.terminate()
        print("flushing hdf5 file")
        self._h5file.flush()
        print("closing  hdf5 file")
        self._h5file.close()

    def log_sys_stats(self) -> NoReturn:
        """ captures state of system in a fixed intervall
            takes ~ 58 ms on BBG
        :return: none
        """
        ts_now_ns = int(time.time() * (10 ** 9))
        if ts_now_ns >= (self.sys_log_last_ns + self.sys_log_intervall_ns):
            self.sys_log_last_ns = ts_now_ns
            dataset_length = self.sys_grp["time"].shape[0]
            self.sys_grp["time"].resize((dataset_length + 1,))
            self.sys_grp["time"][dataset_length] = ts_now_ns

            # CPU https://psutil.readthedocs.io/en/latest/#cpu
            self.sys_grp["cpu_util"].resize((dataset_length + 1,))
            self.sys_grp["cpu_util"][dataset_length] = int(round(psutil.cpu_percent(0)))

            # Memory https://psutil.readthedocs.io/en/latest/#memory
            self.sys_grp["ram_util"].resize((dataset_length + 1, 2))
            mem_stat = psutil.virtual_memory()[0:3]
            self.sys_grp["ram_util"][dataset_length, 0:2] = [int(100 * mem_stat[1] / mem_stat[0]), int(mem_stat[2])]

            # IO https://psutil.readthedocs.io/en/latest/#psutil.disk_io_counters
            self.sys_grp["io_util"].resize((dataset_length + 1, 4))
            self.sys_grp["io_util"][dataset_length, :] = psutil.disk_io_counters()[0:4]  # TODO: should be delta

            # Network https://psutil.readthedocs.io/en/latest/#psutil.net_io_counters
            self.sys_grp["net_util"].resize((dataset_length + 1, 2))
            self.sys_grp["net_util"][dataset_length, :] = psutil.net_io_counters()[0:2]  # TODO: should be delta

            # TODO: add temp, not working: https://psutil.readthedocs.io/en/latest/#psutil.sensors_temperatures
            print(f"sysLog took {round(time.time() * 10**3 - ts_now_ns / 10**6, 2)} ms")

    def log_dmesg(self, line):
        dataset_length = self.dmesg_grp["time"].shape[0]
        self.dmesg_grp["time"].resize((dataset_length + 1,))
        self.dmesg_grp["time"][dataset_length] = int(time.time() * (10 ** 9))
        self.dmesg_grp["message"].resize((dataset_length + 1,))
        self.dmesg_grp["message"][dataset_length] = line

    def log_ptp4l(self, val_list):
        dataset_length = self.dmesg_grp["time"].shape[0]
        self.timesync_grp["time"].resize((dataset_length + 1,))
        self.timesync_grp["time"][dataset_length] = int(time.time() * (10 ** 9))
        self.timesync_grp["values"].resize((dataset_length + 1, 3))
        self.timesync_grp["values"][dataset_length, :] = val_list[0:3]


def dmesg_monitor(datalog: LogWriter):
    # var1: ['dmesg', '--follow']
    # var2: ['journalctl', '--dmesg', '--follow', '--lines=40', '--output=short-precise']
    cmd_dmesg = ['sudo', 'journalctl', '--dmesg', '--follow', '--lines=40', '--output=short-precise']
    proc_dmesg = subprocess.Popen(cmd_dmesg, stdout=subprocess.PIPE, universal_newlines=True)

    for line in iter(proc_dmesg.stdout.readline, ""):
        line = str(line).strip()[:128]
        try:
            datalog.log_dmesg(line)
        except OSError:
            print(f"[DmesgMonitor] Caught a Write Error for Line: [{type(line)}] {line}")
        time.sleep(0.1)  # rate limiter
    print(f"[DmesgMonitor] ended itself")


def ptp4l_monitor(datalog: LogWriter):
    # example: Feb 16 10:58:37 sheep1 ptp4l[378]: [821.629] master offset      -4426 s2 freq +285889 path delay     12484
    cmd_ptp4l = ['sudo', 'journalctl', '--unit=ptp4l', '--follow', '--lines=1', '--output=short-precise']  # for client
    proc_ptp4l = subprocess.Popen(cmd_ptp4l, stdout=subprocess.PIPE, universal_newlines=True)

    for line in iter(proc_ptp4l.stdout.readline, ""):
        try:
            words = str(line).split()
            i_start = words.index("offset")
            values = [int(words[i_start + 1]), int(words[i_start + 4]), int(words[i_start + 7])]
        except ValueError:
            continue
        try:
            datalog.log_ptp4l(values)
        except OSError:
            print(f"[PTP4lMonitor] Caught a Write Error for Line: [{type(line)}] {line}")
        time.sleep(0.25)  # rate limiter
    print(f"[PTP4lMonitor] ended itself")

def LogExtracter(file: Path):
    with h5py.File(file, "r") as db_in:
        print("test")

if __name__ == "__main__":

    logger = LogWriter(Path("./test_sys_log.h5"))

    ts_end = time.time() + 60
    while time.time() < ts_end:
        logger.log_sys_stats()
        time.sleep(0.01)

    logger.__exit__()
