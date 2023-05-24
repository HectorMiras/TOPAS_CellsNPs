from get_NP_positions import get_positions


positions_file = "positions_in_cell_5000_AuNP.txt"
Rmax = 7290.9
Rmin = 4800.0
H = 10000.0
Rnp = 7.5
N = 5000
get_positions(N, Rmax, H, Rmin, Rnp, positions_file)

