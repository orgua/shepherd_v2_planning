import time
from itertools import product

import pandas as pd
from keithley2600.keithley_driver import KeithleyClass
from smu import SMU
from tqdm import tqdm


def smu_measure_boost(vs_input, is_input, vs_output) -> pd.DataFrame:
    smu = SMU()
    results: list = []  # np.zeros(shape=(len(vs_input) * len(vs_output) * len(is_input), 8))
    total = len(vs_input) * len(vs_output) * len(is_input)
    for index, (v_out, v_inp, i_inp) in tqdm(
        enumerate(product(vs_output, vs_input, is_input)), total=total
    ):
        # check if set-point is valid
        v_oc = v_inp * (100 / 78)
        if v_oc > v_out:
            print("SKIP - V_IN > V_OUT")
            continue

        # prepare set-point
        smu.set_smu_to_vsource(smu.out, value_v=v_out, limit_i=i_inp)
        smu.set_smu_to_isource(smu.inp, value_i=i_inp, limit_v=v_oc)

        # wait for VOC-Measurement
        is_reached = False
        time_start = time.time()
        while not is_reached:
            iim = smu.inp.measure.i()
            is_reached = abs(iim) < 0.5 * i_inp
            if time.time() - time_start > 2 * 16:
                print("SKIP - Timeout while looking for VOC")
                break
        if not is_reached:
            continue

        # give time to stabilize, measure & store
        time.sleep(5)
        time_start = time.time()
        while time.time() < time_start + 5:
            vim = smu.inp.measure.v()
            iim = smu.inp.measure.i()
            vom = smu.out.measure.v()
            iom = smu.out.measure.i()

            # store results
            p_inp = vim * iim
            p_out = vom * max(0.0, -iom)
            try:
                eta = p_out / p_inp
            except ZeroDivisionError:
                continue
            result = [v_out, v_inp, i_inp, vim, iim, vom, iom, eta]
            results.append(result)

    smu.set_smu_off(smu.inp)
    smu.set_smu_off(smu.out)
    return pd.DataFrame(
        data=results,
        columns=["V_out_nom", "V_inp_nom", "I_inp_nom", "V_inp", "I_inp", "V_out", "I_out", "eta"],
        dtype=float,  # np.float256 ?
    )


def smu_measure_buck(v_input: list, v_output: float, i_output: list) -> pd.DataFrame:
    smu = SMU()
    results: list = []
    total = len(v_input) * len(i_output)
    # initial set
    smu.set_smu_off(smu.out)
    smu.set_smu_to_vsource(smu.inp, value_v=2, limit_i=100e-3)
    time.sleep(5)

    for index, (v_inp, i_out) in tqdm(enumerate(product(v_input, i_output)), total=total):
        # prepare set-point
        smu.set_smu_to_vsource(smu.inp, value_v=v_inp, limit_i=4 * i_out)
        time.sleep(1)
        # smu.inp.source.levelv = min(max(v_inp, 0.0), 5.5)
        # smu.inp.source.limiti = min(max(6*i_out, -0.080), 0.080)
        smu.set_smu_to_isource(smu.out, value_i=-i_out, limit_v=2.0)
        # smu.out.source.leveli = min(max(-i_out, -0.080), 0.080)

        # measure, verify, store
        counter = 0
        time_start = time.time()
        while counter < 10:
            vim = smu.inp.measure.v()
            vom = smu.out.measure.v()
            iim = smu.inp.measure.i()
            iom = smu.out.measure.i()

            is_reached = abs(vim / v_inp - 1) < 0.03 or abs(vim - v_inp) < 0.05  # % & V
            is_reached &= iim > 0
            is_reached &= abs(vom / v_output - 1) < 0.05  # %
            is_reached &= abs(iom / i_out + 1) < 0.05  # %

            p_inp = vim * iim
            p_out = vom * max(0.0, -iom)
            try:
                eta = p_out / p_inp
            except ZeroDivisionError:
                continue
            result = [v_inp, i_out, vim, iim, vom, iom, eta]

            is_reached &= eta >= 0.0
            is_reached &= eta <= 1.0

            # store results
            results.append(result)

            if time.time() - time_start > 60:
                print(f"SKIP - Timeout while stabilizing (n={counter}, last: {result}")
                break
            if not is_reached:
                # do not count invalid measurements
                continue
            counter += 1
        smu.set_smu_off(smu.out)

    smu.set_smu_off(smu.inp)
    smu.set_smu_off(smu.out)
    return pd.DataFrame(
        data=results,
        columns=["V_inp_nom", "I_out_nom", "V_inp", "I_inp", "V_out", "I_out", "eta"],
        dtype=float,  # np.float256 ?
    )


def old_meas_loop(smu: KeithleyClass, v_inp, i_inp, v_out):
    is_reached = False
    time_start = time.time()
    while time.time() < time_start + 5:
        vim = smu.inp.measure.v()
        iim = smu.inp.measure.i()
        vom = smu.out.measure.v()
        iom = smu.out.measure.i()
        is_reached = abs(vim / v_inp - 1) < 0.10 or abs(vim - v_inp) < 0.05  # not that important
        is_reached &= abs(iim / i_inp - 1) < 0.05
        is_reached &= abs(vom / v_out - 1) < 0.05
        is_reached &= iom < 0
        if time.time() - time_start > 1 * 16:
            smu.set_smu_off(smu.inp)
            smu.set_smu_off(smu.out)
            break
    if not is_reached:
        print("SKIP - Timeout while measuring")
        # continue
