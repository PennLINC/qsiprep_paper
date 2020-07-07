import sys
import os.path as op
from glob import glob
import numpy as np

bval_file = sys.argv[1]


if not op.exists(bval_file):
    bval_files = glob(bval_file.replace("run-01", "run-*"))
    if not bval_files:
        print("None")
        sys.exit(0)
    bval_file = sorted(bval_files)[0]


bvals = np.loadtxt(bval_file)

b0s = np.flatnonzero(bvals < 200)
if not b0s.size:
    print("None")
else:
    print(b0s[0])
sys.exit(0)

