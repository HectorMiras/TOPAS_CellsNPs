from get_NP_positions import get_positions


positions_file = "positions_in_medium_663_AuNP.txt"
Rmax = 1.25*4800.0
Rmin = 0
H = 200
Rnp = 7.5
N = 663
get_positions(N, Rmax, H, Rmin, Rnp, positions_file)

