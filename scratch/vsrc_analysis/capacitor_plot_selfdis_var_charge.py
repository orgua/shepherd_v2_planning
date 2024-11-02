from pathlib import Path

import numpy as np
from capacitor_real import cap_real_self
from matplotlib import pyplot as plt

runtime = 100

fig = plt.figure(figsize=(9, 8), layout="tight")

plt.plot(cap_real_self[3]["time"], cap_real_self[3]["voltage"], label="10s pre-charge @5V")
plt.plot(cap_real_self[4]["time"], cap_real_self[4]["voltage"], label="20s pre-charge @5V")
plt.plot(cap_real_self[5]["time"], cap_real_self[5]["voltage"], label="50s pre-charge @5V")
plt.plot(cap_real_self[6]["time"], cap_real_self[6]["voltage"], label="100s pre-charge @5V")
plt.plot(cap_real_self[7]["time"], cap_real_self[7]["voltage"], label="200s pre-charge @5V")
plt.plot(cap_real_self[8]["time"], cap_real_self[8]["voltage"], label="400s pre-charge @5V")
plt.plot(cap_real_self[9]["time"], cap_real_self[9]["voltage"], label="800s pre-charge @5V")
plt.plot(cap_real_self[10]["time"], cap_real_self[10]["voltage"], label="10s pre-charge @5V - recheck")


plt.suptitle("Self-Discharge of 100 uF MLCC1 Capacitor")
plt.xlabel("time [s]")
plt.ylabel("voltage [V]")
plt.xticks(np.arange(0.0, runtime + 0.1, 5))
plt.yticks(np.arange(0.0, 5.6, 0.2))
plt.ylim(bottom=1.5, top=5.0)
#plt.yscale("log")
plt.grid(True)
plt.legend(loc="upper right")
plt.tight_layout()
# force direct values on axis
for ax in fig.get_axes():
#    ax.get_yaxis().get_major_formatter().set_useOffset(False)
    ax.get_xaxis().get_major_formatter().set_useOffset(False)
plt.savefig(Path(__file__).with_suffix(".svg"))  # PNG / SVG

plt.ylim(bottom=1.6, top=2.0)
#plt.yscale("log")
plt.xlim(left=90, right=100)
plt.savefig(Path(__file__).with_suffix(".detail.svg"))  # PNG / SVG
plt.close(fig)
