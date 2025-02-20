from get_NP_positions import get_positions_binned
import numpy as np


positions_file = "positions_in_cell.txt"
shape="Cylindrical"
Rmax = 7290 # cylindric cell A549 radius
Rmin = 4800 # spheric nucleus radius
H = 10000 # cylindric cell height
Rnp = 15 # AGuIX: 1.5, AuNP15: 15 (7.5 np Au core + 7.5 PEG shell)
N = 5000 # AGuIX: 400000, AuNP: 5000
sN = 500  # N sigma
Nrand = int(np.random.normal(N, sN))
numberNPs = get_positions_binned(Nrand, Rmax, H, Rmin, Rnp, positions_file, shape=shape)
with open('./../np_number.txt', "w") as f:
    f.write(str(numberNPs))




