from pathlib import Path

import numpy as np
from PIL.ImageColor import colormap
from matplotlib import pyplot as plt
from capacitor_shepherd import shp_cap_sim_boost
from capacitor_shepherd import shp_cap_sim_current

runtime = 0.5

# simulate shepherd @ 3 V, 1 mA for 1 s
shp_cap1 = shp_cap_sim_boost(V_start_V=3.0, P_inp_W=-3 * 1e-3, runtime=runtime)
shp_cap2 = shp_cap_sim_current(V_start_V=3.0, I_inp_A=-1e-3, V_max_V=3.0, runtime=runtime)

fig = plt.figure(figsize=(9, 8), layout="tight")

plt.plot(shp_cap1["time"], shp_cap1["voltage"], label="100uF shepherd (P_inp, wrong)")
plt.plot(shp_cap2["time"], shp_cap2["voltage"], label="100uF shepherd (I_inp)")

plt.suptitle(f"Charging of CapacitorModels")
plt.xlabel("time [s]")
plt.ylabel("voltage [V]")
plt.xticks(np.arange(0.0, runtime+0.1, 0.1))
plt.yticks(np.arange(0.0, 5.6, 0.5))
plt.ylim(bottom=0.0) #, top=1.0)
plt.grid(True)
plt.legend(loc="lower right")
plt.tight_layout()
# force direct values on axis
for ax in fig.get_axes():
    ax.get_yaxis().get_major_formatter().set_useOffset(False)
    ax.get_xaxis().get_major_formatter().set_useOffset(False)
plt.savefig(Path(__file__).with_suffix(".svg"))  # PNG / SVG
plt.close(fig)
