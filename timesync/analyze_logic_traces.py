import pandas as pd
import matplotlib.pyplot as plt

# saleae logic outputs:
# Time[s], Channel 0, Channel 1
# 0.000000000000000, 1, 1
# 7.642110550000000, 1, 0

files = [
    "timesync2BB_n20_12_pru_opt.csv",
    #"timesync2BB_n20_11_pru_opt.csv",
    #"timesync2BB_n20_10_pru_opt.csv",
    #"timesync2BB_n20_08_pru_opt.csv",
    #"timesync2BB_n20_07_kernel_opt.csv",
    #"timesync2BB_n20_06_kernel_opt.csv",
    #"timesync2BB_n20_05_pru_opt.csv",
    #"timesync2BB_n20_crystal_2h.csv",
    #"timesync2BB_n20_4h.csv",
    #"timesync2BB_n20_30min.csv",
    "timesync2BB_n10_30min.csv",
]

sample_frequency = 100e6
data_list = list([])


def series_statistics(data: pd.Series, name: str):
    dmin = round(data.min(), 4)
    dmax = round(data.max(), 4)
    dq05 = round(data.quantile(0.05), 4)
    dq95 = round(data.quantile(0.95), 4)
    dmean = round(data.mean(), 4)
    print(f"       \t[  min  <|  q05%  ||  mean  ||  q95%  |>  max  ]")
    print(f"{name} \t[ {dmin} <| {dq05} || {dmean} || {dq95} |> {dmax} ]")


def plot_graph(x:list, y: list, filename: str, size:tuple = (18, 8)):
    plt.figure(figsize=size)
    plt.plot(x, y)
    plt.savefig(filename)
    plt.close()


for file in files:
    data = pd.read_csv(file, delimiter=",", decimal=".", float_precision="high", index_col=False)  #index_col="Time[s]"
    data.columns = data.columns.str.strip()  # fixes weird space before column-names
    # values are binary -> get timestamps of chipselect-start (falling Edge)
    # - first calc the derivative (current value - previous value)
    # - second filter for "-1" and keep only these
    # - now subtract the timestamps
    dtime = data["Time[s]"].iloc[1:]
    ch0 = data.loc[:, "Channel 0"]
    ch0d = pd.Series(ch0.values[1:] - ch0.values[:-1], index=ch0.index[1:])
    ch0t = dtime[ch0d < 0]
    ch1 = data.loc[:, "Channel 1"]
    ch1d = pd.Series(ch1.values[1:] - ch1.values[:-1], index=ch1.index[1:])
    ch1t = dtime[ch1d < 0]
    # filter time-series for start and end that both series cover
    time_start = max(ch0t.min(), ch1t.min()) - 5e-6
    time_stop = min(ch0t.max(), ch1t.max()) - 5e-6
    ch0t = ch0t[(ch0t > time_start) & (ch0t < time_stop)].reset_index(drop=True)
    ch1t = ch1t[(ch1t > time_start) & (ch1t < time_stop)].reset_index(drop=True)
    min_length = min(ch0t.shape[0], ch1t.shape[0])
    # cut series to proper length and determine channel offset
    time_delta = (ch1t.iloc[0:min_length] - ch0t.iloc[0:min_length])*1e9

    print(f"\n\nFILE: {file}")
    series_statistics(time_delta, "dt_ns")
    ch0td = (pd.Series(ch0t.values[1:] - ch0t.values[:-1], index=ch0t.index[1:]) * 1e6).round(4)
    series_statistics(ch0td, "Ch0_us")
    ch1td = (pd.Series(ch1t.values[1:] - ch1t.values[:-1], index=ch1t.index[1:]) * 1e6).round(4)
    series_statistics(ch1td, "Ch1_us")

    plot_graph(ch0t.values, time_delta.values, file + "_sync_overview.png")
    plot_graph(ch0t.values[0:22000], time_delta.values[0:22000], file + "_sync_detail.png", (30,8))
    plot_graph(ch0t.values[:22000], ch0td.values[:22000], file + "_trigger_period_ch0.png", (30,8))
    plot_graph(ch1t.values[:22000], ch1td.values[:22000], file + "_trigger_period_ch1.png", (30,8))
    data_list.append(time_delta)

plt.figure(figsize=(12, 8))
df = pd.concat(data_list, axis=1)
df.columns = files
df.plot.box()
plt.savefig("statistic_boxplot.png")
plt.close()
