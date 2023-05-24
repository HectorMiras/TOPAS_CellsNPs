from get_NP_positions import get_positions


positions_file = "positions_in_medium_1308184_AGuIX.txt"
Rmax = 1.25*4800.0
Rmin = 0
H = 200
Rnp = 1.5
N = 1308184
get_positions(N, Rmax, H, Rmin, Rnp, positions_file)

