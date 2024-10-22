"""
Simulates charging and discharging of the capacitor-model integrated into shepherd.

"""
import numpy as np
import pandas as pd
from shepherd_core.data_models import VirtualSourceConfig
from shepherd_core.data_models.content.virtual_source import ConverterPRUConfig
from shepherd_core.vsource import PruCalibration
from shepherd_core.vsource.virtual_source_model import VirtualConverterModel
from shepherd_core.commons import samplerate_sps_default

cnv = VirtualConverterModel(
    cfg=ConverterPRUConfig.from_vsrc(
        data=VirtualSourceConfig(name="BQ25570", C_intermediate_uF=100)
    ),
    cal=PruCalibration(),
)

def shp_cap_sim_boost(V_start_V: float, P_inp_W: float, runtime: float = 1) -> pd.DataFrame:
    """ wrong approach - as the power-calc is only acceptable for the boost-case """
    cnv.V_mid_uV = V_start_V * 1e6
    if P_inp_W > 0.0:
        cnv.P_out_fW = 0
        cnv.P_inp_fW = P_inp_W * 1e15
    else:
        cnv.P_out_fW = - P_inp_W * 1e15
        cnv.P_inp_fW = 0
    timestamps = np.arange(0.0, runtime, 1.0 / samplerate_sps_default)
    voltages = np.zeros(shape=len(timestamps))

    voltages[0] = 0.0
    for idx in range(1, len(voltages)):
        voltages[idx] = cnv.update_cap_storage()

    result = pd.DataFrame(columns=["time", "voltage"])
    result["time"] = timestamps
    result["voltage"] = voltages * 1e-6
    return result

def shp_cap_sim_current(V_start_V: float, I_inp_A: float, V_max_V: float, runtime: float = 1) -> pd.DataFrame:
    """ deconstructed VirtualConverterModel.update_cap_storage() """
    cnv.V_mid_uV = V_start_V * 1e6
    timestamps = np.arange(0.0, runtime, 1.0 / samplerate_sps_default)
    voltages = np.zeros(shape=len(timestamps))

    voltages[0] = 0.0
    for idx in range(1, len(voltages)):
        dV_mid_uV = I_inp_A * 1e9 * cnv.Constant_us_per_nF
        cnv.V_mid_uV += dV_mid_uV
        cnv.V_mid_uV = min(cnv.V_mid_uV, cnv._cfg.V_intermediate_max_uV, V_max_V*1e6)
        cnv.V_mid_uV = max(cnv.V_mid_uV, 1)
        voltages[idx] = cnv.V_mid_uV * 1e-6

    result = pd.DataFrame(columns=["time", "voltage"])
    result["time"] = timestamps
    result["voltage"] = voltages
    return result