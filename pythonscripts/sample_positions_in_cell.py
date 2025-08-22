from get_NP_positions import get_positions_binned, get_positions_clustered
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

# cluster_distribution = 'LogNormal'  # Options: 'LogNormal', 'Gamma', 'Gaussian'
cluster_distribution = None  # If you want to sample positions without clustering

numberNPs, cluster_radii = get_positions_clustered(Nrand, Rmax, H, Rmin, Rnp, positions_file,shape="Cylindrical", cluster_distribution=cluster_distribution)
    
with open('./../np_number.txt', "w") as f:
    f.write(str(numberNPs))




