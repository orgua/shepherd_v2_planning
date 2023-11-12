import pandas as pd


def filter_cs_falling_edge(data: pd.Series, falling: bool = True) -> pd.Series:
    data.columns = data.columns.str.strip()  # fixes weird space before column-names
    # values are binary -> get timestamps of chipselect-start (falling Edge)
    # - first calc the derivative (current value - previous value)
    # - second filter for "-1" and keep only these
    # - now subtract the timestamps
    # data = data[data["Time[s]"] > 1]
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
    data_new = [ch0t.iloc[0:min_length].mul(1e9).round(0),
                ch1t.iloc[0:min_length].mul(1e9).round(0)]
    df = pd.concat(data_new, axis=1)
    df.columns = ["Ch0", "Ch1"]
    return df
