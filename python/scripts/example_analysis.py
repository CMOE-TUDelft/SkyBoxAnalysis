"""Example analysis script using fsslib.

Run with the fss conda environment active and fsslib installed in editable mode:

    cd python
    pip install -e .
    python scripts/example_analysis.py
"""

import numpy as np
from fsslib import dummy_catenary, example_mooring_stiffness

def main() -> None:
    x = np.linspace(-5, 5, 201)
    y = dummy_catenary(x, H=10.0, w=2.0)
    k = example_mooring_stiffness(L=100.0, EA=1e6)

    print("Catenary y-range:", float(y.min()), "to", float(y.max()))
    print("Example mooring stiffness:", k)

if __name__ == "__main__":
    main()
