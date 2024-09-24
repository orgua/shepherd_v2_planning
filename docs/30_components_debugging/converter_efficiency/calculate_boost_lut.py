from efficiency_boost import efficiency_boost
# configure your set-point
v_out = 2.88  # 2.52 .. 3.32

# LUT
v_inp_min = (2**17)*1e-6
v_inp_low = [v_inp_min * x for x in range(12)]
v_inp_mid = [v_inp_min/2 + v_inp_min * x for x in range(12)]
v_inp_hig = [v_inp_min * (x + 1) for x in range(12)]

i_inp_min = (2**13)*1e-9
i_inp_mid = [i_inp_min/2 * 2**x for x in range(12)]

LUT_inp_eff_model: list = []

for v_inp in v_inp_mid:
    row: list = []
    for i_inp in i_inp_mid:
        row.append(efficiency_boost(v_inp, i_inp, v_out))
    LUT_inp_eff_model.append(row)
    print(row)
