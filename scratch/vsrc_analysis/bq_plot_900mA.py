from pathlib import Path

from shepherd_core.vsource import ResistiveTarget
from matplotlib import pyplot as plt

from bq_shepherd import simulate_source

path_input = Path(__file__).parent / "bq-characteristics/solar-iv-900mA.ivcurve.csv"
target = ResistiveTarget(R_Ohm=983, controlled=False)


stats_internal = simulate_source(
    target=target,
    path_ivcurve=path_input,
    runtime=18,
    # path_output=file_output,
)


fig, axs = plt.subplots(4, 1, sharex="all", figsize=(20, 4 * 6), layout="tight")
fig.suptitle(f"BQ25570-Sim with Inp={path_input.name}") #, E={e_out_Ws} Ws")
axs[0].set_ylabel("Voltages [V]")
axs[0].plot(stats_internal[:, 0], stats_internal[:, 1:5])
axs[0].legend(["V_cv_hold", "V_inp_Req", "V_cv_set", "V_cap"], loc="upper right")

axs[1].set_ylabel("Current [mA]")
axs[1].plot(stats_internal[:, 0], stats_internal[:, 5:8])
axs[1].legend(["C_cv_hold", "C_cv_delta", "C_out"], loc="upper right")

axs[2].set_ylabel("Power [mW]")
axs[2].plot(stats_internal[:, 0:1], stats_internal[:, 8:10])
axs[2].legend(["P_inp", "P_out"], loc="upper right")

axs[3].set_ylabel("PwrGood [n]")
axs[3].plot(stats_internal[:, 0], stats_internal[:, 10])
axs[3].legend(["PwrGood"], loc="upper right")

axs[3].set_xlabel("Runtime [s]")

for ax in axs:
    # deactivates offset-creation for ax-ticks
    ax.get_yaxis().get_major_formatter().set_useOffset(False)
    ax.get_xaxis().get_major_formatter().set_useOffset(False)

plt.savefig(Path(__file__).with_suffix(".png"))
plt.close(fig)
plt.clf()

print(f"PowerGood - Ratio: {stats_internal[:, 10].sum() / stats_internal.shape[0]:.3f}")