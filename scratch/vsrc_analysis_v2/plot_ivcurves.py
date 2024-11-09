from pathlib import Path

from matplotlib import pyplot as plt

from solar import paths_ivcurve
from solar import open_ivcurve

fig, axs = plt.subplots(3, 1, sharex="all", figsize=(10, 2 * 6), layout="tight")

fig.suptitle("Voltage, current & power of IVCurves")

axs[0].set_ylabel("voltage [V]")
axs[1].set_ylabel("current [mA]")
axs[2].set_ylabel("power [mW]")

axs[2].set_xlabel("time [s]")

for name, path in paths_ivcurve.items():
    ivcurve = open_ivcurve(path)
    ivcurve["Time [s]"] = ivcurve["Time [s]"] - ivcurve["Time [s]"][0]
    ivcurve["Power [W]"] = ivcurve["Voltage [V]"] * ivcurve["Current [A]"]
    axs[0].plot(ivcurve["Time [s]"], ivcurve["Voltage [V]"], label=name)
    axs[1].plot(ivcurve["Time [s]"], 1e3 * ivcurve["Current [A]"], label=name)
    axs[2].plot(ivcurve["Time [s]"], 1e3 * ivcurve["Power [W]"], label=name)

axs[0].legend(paths_ivcurve.keys(), loc="upper right")

for ax in axs:
    # deactivates offset-creation for ax-ticks
    ax.get_yaxis().get_major_formatter().set_useOffset(False)
    ax.get_xaxis().get_major_formatter().set_useOffset(False)
    # add grid
    ax.grid(True)


plt.savefig(Path(__file__).with_suffix(".png"))
plt.savefig(Path(__file__).with_suffix(".svg"))
plt.close(fig)
plt.clf()
