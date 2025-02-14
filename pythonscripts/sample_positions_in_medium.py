from get_NP_positions import get_positions_binned


positions_file = "positions_in_medium.txt"
Rmax = 1.25*4800
Rmin = 0
H = 200
Rnp = 15 # AGuIX: 1.5, AuNP15: 15 (7.5 np Au core + 7.5 PEG shell)
N = 1179 # AGuIX: 1308200, AuNP: 1179 (values for 1 mg/ml concentration)
get_positions_binned(N, Rmax, H, Rmin, Rnp, positions_file)

