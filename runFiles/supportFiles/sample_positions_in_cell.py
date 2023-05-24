from get_NP_positions import get_positions


positions_file = "positions_in_cell_400000_AGuIX.txt"
Rmax = 7290.9
Rmin = 4800.0
H = 10000.0
Rnp = 1.5
N = 400000
get_positions(N, Rmax, H, Rmin, Rnp, positions_file)

