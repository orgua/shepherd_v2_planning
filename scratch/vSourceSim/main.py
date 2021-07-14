from virtual_source import VirtualSource
from calibration import CalibrationData
import numpy as np
import matplotlib.pyplot as plt
import yaml

cal = CalibrationData.from_default()

N = 500_000
ts = np.arange(0, N * 10e-6, 10e-6)
vcaps = np.empty((N, 3))

vs_cfg = yaml.safe_load("virtsource.yml")
vs = VirtualSource(vs_cfg, cal)

I_out_adc_sleep = cal.convert_value_to_raw("emulation", "adc_current", 200e-9)
I_out_adc_active = cal.convert_value_to_raw("emulation", "adc_current", 10e-3)

I_out = I_out_adc_sleep
N_good = 0
for i in range(N):
    # Harvest at 1V 100uA
    vs.calc_inp_power(1e6, 100e3)
    vs.calc_out_power(I_out)
    vs.update_capacitor()
    out_raw = vs.update_boostbuck()
    out_V = cal.convert_raw_to_value("emulation", "dac_voltage_b", out_raw)
    if vs.get_power_good():
        I_out = I_out_adc_active
        N_good += 1
    else:
        I_out = I_out_adc_sleep

    vcaps[i] = [vs.get_storage_Capacitor_uV() / 1e6, out_V, vs.get_power_good()]

print(f"Power-Good ratio is {round(100*N_good/N,3)} %")

plt.figure(figsize=(20, 8))
plt.plot(ts, vcaps)
plt.xlabel("time [s]")
plt.ylabel("[V]")
plt.legend(["V_Cap", "V_Out", "PGood"], loc='upper right')
plt.show()
