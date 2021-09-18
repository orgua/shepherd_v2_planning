import numpy as np
from pathlib import Path
import click
import h5py

@click.command()
@click.argument("database", type=click.Path(exists=True, dir_okay=False))
def cli(database):
    with h5py.File(database, "r") as db:
        print(f"File got {len(db['gpio']['value'])} entries for GPIO")
        tt = db["gpio"]["value"][:] & (int(2**9) + int(2**10))  # BitPosition r30_09/out  TARGET_BAT_OK
        counts = np.unique(tt, return_counts=True)
        print(f"got the following result:")
        print(counts)


if __name__ == "__main__":
    cli()
