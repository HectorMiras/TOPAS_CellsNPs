#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import numpy as np
import sys

# Number of small spheres
#N = 35370 # 1 mg/ml of 15nm AuNPs in a (1670-volnucl) um3 cell
N = int(sys.argv[1])

# Minimum distance in nm between the centers of the small spheres (NP diameter)
# min_distance = 1.5
min_distance = 30.01

# Radius of the base in nm
Rmax = 7291 - 10 - min_distance/2
# Radius of the inner sphere
Rmin = 4800 + min_distance/2
# Half Height of the cylinder in nm
HL = 5000 - 10

# Generate random positions for the small spheres
positions = np.empty((0, 3), dtype=float)
while len(positions) < N:
  # Generate random point inside the cylinder
  x = (2 * Rmax * np.random.random()) - Rmax
  y = (2 * Rmax * np.random.random()) - Rmax
  z = (2 * HL * np.random.random()) - HL
  point = np.array([x, y, z])
  if (np.sqrt(x * x + y * y) <= Rmax) and (np.sqrt(x * x + y * y + z * z) > Rmin) and (np.abs(z) <= HL):
    # Check if the point is far enough from the other small spheres
    if len(positions) == 0 or np.min(np.linalg.norm(positions - point, axis=1)) >= min_distance:
      positions = np.vstack([positions, point])
      if len(positions) % 1000 == 0:
        print(len(positions), 'out of', N)

# Print the positions of the small spheres
f = open(f"./supportFiles/positions_in_cell_{N}_AuNP.txt",'w')
for i, p in enumerate(positions):
  #print(f"Small sphere {i+1}: x={p[0]:.2f}, y={p[1]:.2f}, z={p[2]:.2f}")
  f.write(str(p[0]) + " " + str(p[1]) + " " + str(p[2]) + "\n")
f.close()

