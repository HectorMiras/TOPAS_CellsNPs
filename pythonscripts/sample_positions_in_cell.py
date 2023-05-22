from get_NP_positions import get_positions


positions_file = "positions_in_cell.txt"
Rmax = 7290 # cylindric cell A549 radius
Rmin = 4800 # spheric nucleus radius
H = 10000 # cylindric cell height
Rnp = 15 # AGuIX: 1.5, AuNP15: 15 (7.5 np Au core + 7.5 PEG shell)
N = 5000 # AGuIX: 400000, AuNP: 5000
get_positions(N, Rmax, H, Rmin, Rnp, positions_file)

