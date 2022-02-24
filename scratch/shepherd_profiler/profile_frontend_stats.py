import itertools
import os
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats

file_name_stats = "profile_analysis.csv"

cgain = 1
coffset = 0
vgain = 1
voffset = 0

adict = {"voltage_shp_V": 0,
         "voltage_shp_raw": 1,
         "voltage_ref_V": 2,
         "current_shp_A": 3,
         "current_shp_raw": 4,
         "current_ref_A": 5,
         }
alist = ["v_shp_V", "v_shp_raw", "v_ref_V", "c_shp_A", "c_shp_raw", "c_ref_A"]

target_dict = {"a": "emu_a",
               "b": "emu_b",
               "h": "hrv",
               "emu_a": "emu_a",
               "emu_b": "emu_b",
               "hrv": "hrv"
               }

def learn_cal_current(result: pd.DataFrame):
    # chose first voltage above 2.4 V as base, currents range from 60 uA to 14 mA
    result = result.groupby(by=["c_ref_A", "v_shp_V"]).mean().reset_index(drop=False)
    v1 = result[result.v_shp_V >= 2.4].sort_values(by=["v_shp_V"], ignore_index=True).at[0, "v_shp_V"]
    filter0 = (result.c_ref_A >= 60e-6) & (result.c_ref_A <= 14e-3) & (result.v_shp_V == v1)
    result = result[filter0].reset_index(drop=True)
    if filter0.sum() <= 1:
        print("WARNING: skipped a current_calibration")
        return
    global cgain, coffset
    cgain, coffset = measurements_to_calibration(result.c_ref_A, result.c_shp_raw)
    print(f"->resulting C-Cal: gain = {cgain}, offset = {coffset}")


def learn_cal_voltage(result: np.ndarray):
    # chose first current above 60 uA as base, voltages range from 0.3 V to 2.6 V
    result = result.groupby(by=["c_ref_A", "v_shp_V"]).mean().reset_index(drop=False)
    c1 = result[result.c_ref_A >= 60e-6].sort_values(by=["c_ref_A"], ignore_index=True).at[0, "c_ref_A"]
    filter0 = (result.v_shp_V >= 0.3) & (result.v_shp_V <= 2.6) & (result.c_ref_A == c1)
    result = result[filter0].reset_index(drop=True)
    if filter0.sum() <= 1:
        print("WARNING: skipped a voltage_calibration")
        return
    global vgain, voffset
    vgain, voffset = measurements_to_calibration(result.v_ref_V, result.v_shp_raw)
    print(f"->resulting V-Cal: gain = {vgain}, offset = {voffset}")


def cal_convert_current_raw_to_A(input):
    global cgain, coffset
    return input * cgain + coffset


def measurements_to_calibration(ref, raw) -> tuple:
    result = stats.linregress(raw, ref)
    offset = float(result.intercept)
    gain = float(result.slope)
    if result.rvalue < 0.999:
        print(f"WARNING: a calibration had a low rvalue = {result.rvalue}")
    return float(gain), float(offset)


if __name__ == '__main__':

    stats_list = list()
    slist = list()

    if Path(file_name_stats).exists():
        stats_base = pd.read_csv(file_name_stats, sep=";", decimal=",", index_col=False)
        stats_list.append(stats_base)
        if "origin" in stats_base.columns:
            slist = stats_base["origin"].tolist()

    flist = os.listdir("./")
    for file in flist:
        fpath = Path(file)
        if not os.path.isfile(file):
            continue
        if not "npz" in fpath.suffix:
            continue
        if fpath.stem in slist:
            continue

        print(f"processing {file}")
        fprofile = np.load(file, allow_pickle=True)

        for target in target_dict:

            if target not in fprofile:
                continue
            if (fprofile[target] is None) or (fprofile[target].size < 2):
                continue

            result_np = fprofile[target]
            result_pd = pd.DataFrame(np.transpose(result_np), columns=alist)

            # get the inner 100k-array out - similar to pd.ungroup, but without special cmd
            segment_list = list()
            for idx, row in result_pd.iterrows():
                # c_shp_raw is always np.array, but v_shp_raw only when
                segment_df = pd.DataFrame(row.c_shp_raw, columns=["c_shp_raw"])
                segment_df["c_ref_A"] = row.c_ref_A
                segment_df["c_shp_A"] = row.c_shp_A
                segment_df["v_ref_V"] = row.v_ref_V
                segment_df["v_shp_V"] = row.v_shp_V
                segment_df["v_shp_raw"] = row.v_shp_raw
                segment_list.append(segment_df)
            result_df = pd.concat(segment_list, axis=0)

            # fragment to fix old profiles -> special case when measuring without SourceMeter, but with resistor
            filter_v = result_df.v_ref_V <= -3
            result_df.loc[filter_v, "v_ref_V"] = result_df.loc[filter_v, "v_shp_V"]
            result_df.loc[filter_v, "c_ref_A"] = result_df.loc[filter_v, "c_shp_A"]

            learn_cal_current(result_df)
            learn_cal_voltage(result_df)

            result_df["c_shp_A"] = cal_convert_current_raw_to_A(result_df.c_shp_raw)
            result_df["c_shp_A"] = result_df.c_shp_A.apply(lambda x: x if x >= -1e-3 else -1e-3)
            result_df["v_error_mV"] = 1e3 * (result_df.v_ref_V - result_df.v_shp_V)
            result_df["v_error_abs_mV"] = result_df.v_error_mV.abs()
            result_df["c_error_mA"] = 1e3 * (result_df.c_ref_A - result_df.c_shp_A)
            result_df["c_error_abs_mA"] = result_df.c_error_mA.abs()

            result_condensed = result_df.groupby(by=["c_ref_A", "v_shp_V"]).mean().reset_index(drop=False)
            result_condensed["v_error_mean_mV"] = result_df.groupby(by=["c_ref_A", "v_shp_V"]).v_error_mV.mean().reset_index(drop=True)
            result_condensed["v_error_max_mV"] = result_df.groupby(by=["c_ref_A", "v_shp_V"]).v_error_abs_mV.max().reset_index(drop=True)
            result_condensed["v_error_stddev_mV"] = result_df.groupby(by=["c_ref_A", "v_shp_V"]).v_error_abs_mV.std().reset_index(drop=True)
            result_condensed["c_error_mean_mA"] = result_df.groupby(by=["c_ref_A", "v_shp_V"]).c_error_mA.mean().reset_index(drop=True)
            result_condensed["c_error_max_mA"] = result_df.groupby(by=["c_ref_A", "v_shp_V"]).c_error_abs_mA.max().reset_index(drop=True)
            result_condensed["c_error_stddev_mA"] = result_df.groupby(by=["c_ref_A", "v_shp_V"]).c_error_abs_mA.std().reset_index(drop=True)

            filter_c = (result_df.c_ref_A >= 3e-6) & (result_df.c_ref_A <= 40e-3)
            filter_v = (result_df.v_shp_V >= 1.0) & (result_df.v_shp_V <= 3.9)
            result_filtered = result_df[filter_c & filter_v]

            # stat-generator
            # - every dataset is a row
            # - v_diff_mean @all, @1-4V;0-40mA, over each voltage + each current
            # - v_diff_max @all, @1-4V;0-40mA, over each ...
            # - c_error_mean @all, @1-4V;0-40mA -> abs-value?
            #   min, max, stddev, minmax-intervall, mean

            for decision in [False, True]:
                stat_values = pd.DataFrame()
                result_now = result_filtered if decision else result_df
                stat_values["origin"] = [fpath.stem]  # in braces to create first row
                stat_values["component"] = target_dict[target].upper()
                stat_values["range"] = "limited" if decision else "full"

                stat_values["v_error_mean_mV"] = result_now.v_error_abs_mV.mean()
                stat_values["v_error_max_mV"] = result_now.v_error_abs_mV.max()
                stat_values["v_error_std_mV"] = result_now.v_error_abs_mV.std()

                stat_values["c_error_mean_mA"] = result_now.c_error_abs_mA.mean()
                stat_values["c_error_max_mA"] = result_now.c_error_abs_mA.max()
                stat_values["c_error_std_mA"] = result_now.c_error_abs_mA.std()

                stats_list.append(stat_values)

    stat_df = pd.concat(stats_list, axis=0, ignore_index=True)
    stat_df.to_csv(file_name_stats, sep=";", decimal=",", index=False)
