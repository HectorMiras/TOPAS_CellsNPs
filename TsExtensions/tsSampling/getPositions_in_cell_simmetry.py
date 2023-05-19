#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import numpy as np


def get_rotation_matrix(rotation_angle_radians):
  rotation_matrix = np.array([
    [np.cos(rotation_angle_radians), -np.sin(rotation_angle_radians), 0],
    [np.sin(rotation_angle_radians), np.cos(rotation_angle_radians), 0],
    [0, 0, 1]])
  return rotation_matrix

# Number of small spheres
#N = 369983
N = 10000000


# Minimum distance in nm between the centers of the small spheres (NP diameter)
# min_distance = 1.5
min_distance = 30.01

# Radius of the base in nm
Rmax = 7946 - 10 - min_distance/2
# Radius of the inner cylinder
Rmin = 4200 + min_distance/2
# Half Height of the cylinder in nm
HL = 4200 - min_distance/2
zbins = 10
zbinheight = 2 * HL/zbins
# Generate random positions for the small spheres
positions0 = np.empty((0, 3), dtype=float)
positions1 = np.empty((0, 3), dtype=float)
positions = np.empty((0, 3), dtype=float)
n_part = 0
while n_part < (N/(4*zbins)):
  # Generate random point inside the cylinder
  x = (Rmax * np.random.random())
  y = (Rmax * np.random.random())
  z = (zbinheight * np.random.random())
  point = np.array([x, y, z])
  if (np.sqrt(x * x + y * y) <= Rmax) and \
          (np.sqrt(x * x + y * y) > Rmin) and \
          (np.abs(z) < (zbinheight- min_distance/2)) and \
          (min_distance/2 < np.abs(z)):
    # Check if the point is far enough from the other small spheres
    if len(positions) == 0 or np.min(np.linalg.norm(positions0 - point, axis=1)) >= min_distance:
      positions0 = np.vstack([positions0, point])
      n_part += 1
      if n_part % 10 == 0:
        print(4*zbins*n_part, 'out of', N)

positions1 = np.vstack((positions1, positions0))
for i in range(3):
  rotation_angle_radians = (i+1) * np.pi / 2
  rotated_points = np.dot(positions0,get_rotation_matrix(rotation_angle_radians).T)
  positions1 = np.vstack((positions1, rotated_points))


for i in range(zbins):
  rotation_angle_radians = 2 * np.pi * np.random.random()
  # Apply the rotation to the point
  # Apply the rotation to the stack of points
  rotated_points = np.dot(positions1, get_rotation_matrix(rotation_angle_radians).T)
  zshift = i*zbinheight - 0.5*zbins*zbinheight
  zshift_array = np.full(rotated_points.shape, [0.0, 0.0, zshift])
  shifted_rotated_points = rotated_points + zshift_array
  positions = np.vstack((positions, shifted_rotated_points))

print(f'Total number of points generated: {len(positions)}')

# Print the positions of the small spheres
f = open(f"positions_in_cell_{len(positions)}.txt",'w')
for i, p in enumerate(positions):
  #print(f"Small sphere {i+1}: x={p[0]:.2f}, y={p[1]:.2f}, z={p[2]:.2f}")
  f.write(str(p[0]) + " " + str(p[1]) + " " + str(p[2]) + "\n")
f.close()

