import time

import numpy as np
import pandas as pd
from tqdm import tqdm
from itertools import product
from smu import SMU

def smu_measure_boost(vs_input, is_input, vs_output) -> pd.DataFrame:
    smu = SMU()
    results_np = np.zeros(shape=(len(vs_input) * len(vs_output) * len(is_input), 8))
    for index, (v_out, v_inp, i_inp) in tqdm(enumerate(product(vs_output, vs_input, is_input)), total=len(results_np)):

        # check if set-point is valid
        v_oc = v_inp*(100/80)
        if v_oc > v_out:
            print("SKIP - V_IN > V_OUT")
            continue

        # prepare set-point
        smu.set_smu_to_vsource(smu.out, value_v=v_out, limit_i=i_inp)
        smu.set_smu_to_isource(smu.inp, value_i=i_inp, limit_v=v_oc)
        vim = iim = vom = iom = 0

        # wait for VOC-Measurement
        is_reached = False
        time_start = time.time()
        while not is_reached:
            iim = smu.inp.measure.i()
            is_reached = abs(iim) < 0.5 * i_inp
            if time.time() - time_start > 2*16:
                print("SKIP - Timeout while looking for VOC")
                break
        if not is_reached:
            continue

        # give time to stabilize
        time.sleep(5)
        is_reached = False
        time_start = time.time()
        while not is_reached:
            vim = smu.inp.measure.v()
            iim = smu.inp.measure.i()
            vom = smu.out.measure.v()
            iom = smu.out.measure.i()
            is_reached = abs(vim / v_inp - 1) < 0.10  or abs(vim - v_inp) < 0.05 # not that important
            is_reached &= abs(iim / i_inp - 1) < 0.05
            is_reached &= abs(vom / v_out - 1) < 0.05
            #is_reached &= iom < 0
            if time.time() - time_start > 1*16:
                smu.set_smu_off(smu.inp)
                smu.set_smu_off(smu.out)
                break

        # store results
        p_inp = vim * iim
        p_out = vom * max(0.0, -iom)
        result = [
            v_out, v_inp, i_inp, vim, iim, vom, iom, p_out / p_inp]
        print(result)
        if not is_reached:
            print(f"SKIP - Timeout while measuring")
            continue
        results_np[index] = result
        time.sleep(1)

    return pd.DataFrame(
        data=results_np,
        columns=["V_out_nom", "V_inp_nom", "I_inp_nom", "V_inp", "I_inp", "V_out", "I_out", "eta"],
        dtype=float,  # np.float256 ?
    )
