from pathlib import Path

import numpy as np
from capacitor_real import cap_real_dis
from capacitor_shepherd import shp_cap_sim
from matplotlib import pyplot as plt

runtime = 1.0

shp_cap1 = shp_cap_sim(U_start_V=5.0, U_inp_V=0.0, R_inp_Ohm=1000, runtime=runtime)

fig = plt.figure(figsize=(9, 8), layout="tight")

plt.plot(shp_cap1["time"], shp_cap1["voltage"], label="100uF shepherd (RC, 1k)")
plt.plot(cap_real_dis[0]["time"], cap_real_dis[0]["voltage"], label="100uF MLCC1 run1 (RC, 1k)")
plt.plot(cap_real_dis[1]["time"], cap_real_dis[1]["voltage"], label="100uF MLCC1 run2 (RC, 1k)")
plt.plot(cap_real_dis[2]["time"], cap_real_dis[2]["voltage"], label="100uF MLCC2 run1 (RC, 1k)")
plt.plot(cap_real_dis[3]["time"], cap_real_dis[3]["voltage"], label="100uF MLCC2 run2 (RC, 1k)")
plt.plot(cap_real_dis[4]["time"], cap_real_dis[4]["voltage"], label="100uF Tantal run1 (RC, 1k)")
plt.plot(cap_real_dis[5]["time"], cap_real_dis[5]["voltage"], label="100uF Tantal run2 (RC, 1k)")
# plt.plot(shp_cap2["time"], shp_cap2["voltage"], label="100uF shepherd (I_inp)")

plt.suptitle("Discharging of CapacitorModels")
plt.xlabel("time [s]")
plt.ylabel("voltage [V]")
plt.xticks(np.arange(0.0, runtime + 0.1, 0.1))
plt.yticks(np.arange(0.0, 5.6, 0.5))
plt.ylim(bottom=0.0)  # , top=1.0)
plt.grid(True)
plt.legend(loc="lower right")
plt.tight_layout()
# force direct values on axis
for ax in fig.get_axes():
    ax.get_yaxis().get_major_formatter().set_useOffset(False)
    ax.get_xaxis().get_major_formatter().set_useOffset(False)
plt.savefig(Path(__file__).with_suffix(".svg"))  # PNG / SVG
plt.close(fig)
