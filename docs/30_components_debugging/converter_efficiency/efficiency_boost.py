"""Sources:
- https://www.electronicdesign.com/technologies/power/article/21190563/boost-converter-efficiency-through-accurate-calculations
- slva372d.pdf - Basic Calculation of a Boost Converter's Power Stage
- sluuaa7a.pdf - BQ25570 EVM users guide
"""

# inductor
R_L = 0.360
L_L = 22e-6
# mosfet
R_DS_4V2 = 0.700
R_DS_2V1 = 0.800
R_DS_delta = (R_DS_4V2 - R_DS_2V1) / (4.2 - 2.1)

Q_G = 0.36e-9
f_SW = 1e6
# diode
R_D = 2.3
V_F = 0  # because of mosfet instead of diode
# IC
I_quiet = 488e-9


def efficiency_boost(V_In: float, I_In: float, V_Out: float) -> float:
    PL: dict = {}  # losses

    # starting values
    eta = 0.9
    for _ in range(10):
        duty = 1 - V_In * eta / V_Out
        I_Out = I_In * (1 - duty)
        P_In = V_In * I_In
        P_Out = V_Out * I_Out

        # dI_L = V_In * duty / (f_SW * L_L)
        # I_out_max = (I_sw_max - dI_L/2) * (1-duty)

        # conduction loss
        PL["L"] = R_L * I_In**2
        R_DS = R_DS_4V2 + R_DS_delta * (V_Out - 4.2)
        PL["SW"] = R_DS * duty * I_In**2
        PL["D"] = R_D * I_Out**2 + V_F * I_Out

        # other effects
        PL["IC"] = I_quiet * V_Out
        PL["GC"] = min(Q_G * 0.7 * f_SW, PL["IC"])
        # TODO: P_GC is probably part of PL_IC
        # TODO: switching loss with P_SW = 1/2 * V_IN * I_D * (t_R + t_F) * f_SW

        p_loss = sum(PL.values())
        eta = max(0.01, (P_In - p_loss) / P_In)
    return eta


from matplotlib import pyplot as plt

v_storage = 3.0
vcc: list[float] = []
eta: list[float] = []
for vcc_mV in range(100, 3000, 10):
    V_CC = vcc_mV * 1e-3
    vcc.append(V_CC)
    eta.append(efficiency_boost(V_CC, 10e-6, v_storage))

print(efficiency_boost(3.0, 10e-6, v_storage))
fig = plt.figure(figsize=(10, 4), layout="tight")
plt.plot(vcc, eta, label="stor=3V")

v_storage = 2.0
vcc: list[float] = []
eta: list[float] = []
for vcc_mV in range(100, 2000, 10):
    V_CC = vcc_mV * 1e-3
    vcc.append(V_CC)
    eta.append(efficiency_boost(V_CC, 10e-6, v_storage))
plt.plot(vcc, eta, label="stor=2V")

plt.xlabel("V_CC [V]")
plt.xticks([x / 10 for x in range(0, 31, 2)])
plt.ylabel("efficiency [n]")
plt.yticks([y / 10 for y in range(11)])
plt.grid(True)
plt.legend(loc="lower right")
# plt.show()
plt.savefig("./efficiency_boost1.png")
plt.close(fig)
