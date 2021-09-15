from virtual_source import VirtualSource
from calibration import CalibrationData
import numpy as np
import matplotlib.pyplot as plt
import yaml

sample_list = [4_000, 40_000, 400_000]
vs_list = ["direct", "dio_cap", "dio_res_cap", "BQ25504", "BQ25504-Schmitt", "BQ25570", "BQ25570-Schmitt"]
#vs_list = ["diode+resistor+capacitor"]
vs_cfg = yaml.safe_load("virtual_source_defs.yml")

for vs_setting in vs_list:
    for samples in sample_list:
        ts = np.arange(0, samples * 10e-6, 10e-6)
        vcaps = np.empty((samples, 3))

        cal = CalibrationData.from_default()
        vs = VirtualSource(vs_setting, cal)
        #vs.set_V_intermediate_uV(10 * 10**3)

        I_out_adc_sleep = cal.convert_value_to_raw("emulation", "adc_current", 200e-9)
        I_out_adc_active = cal.convert_value_to_raw("emulation", "adc_current", 10e-3)

        I_out = I_out_adc_sleep
        N_good = 0
        for i in range(samples):
            # Harvest at 1V 100uA
            if (i % 1000) < 500:
                vs.calc_inp_power(4e6, 400e3)
            else:
                vs.calc_inp_power(1.1e6, 200e3)
            vs.calc_out_power(I_out)
            vs.update_cap_storage()
            out_raw = vs.update_states_and_output()
            out_V = cal.convert_raw_to_value("emulation", "dac_voltage_b", out_raw)
            if vs.get_power_good():
                I_out = I_out_adc_active
                N_good += 1
            else:
                I_out = I_out_adc_sleep

            vcaps[i] = [vs.get_V_intermediate_uV() / 1e6, out_V, vs.get_power_good()]

        print(f"Power-Good ratio is {round(100 * N_good / samples, 3)} % (for {vs_setting}, {samples})")

        plt.figure(figsize=(20, 8))
        plt.plot(ts, vcaps)
        plt.xlabel("time [s]")
        plt.ylabel("[V]")
        plt.legend(["V_Cap", "V_Out", "PGood"], loc='upper right')
        plt.savefig(f"./performance_vsource_{vs_setting}_s{samples}")
