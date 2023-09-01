#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import numpy as np
import sys

def get_positions(N, Rcyl, Hcyl, Rsph, Rnp, positions_file):
    """
    " Fuinction to sample N positons inside a cylinder of radius Rcyl and height Hcyl, excluding the inner volume of
    " a sphere of radius Rsph.
    " All distances are given in nm.
    " The sampled positions are printed to the txt file positions_file
    """

    def filter_points_outside_sphere(points, center, radius):
        # Calculate the squared distance from each point to the sphere's center
        squared_distances = np.sum((points - center) ** 2, axis=1)

        # Filter points with squared distance greater than the squared radius
        outside_sphere = points[squared_distances > radius ** 2]

        return outside_sphere

    def get_rotation_matrix(rotation_angle_radians):
        rotation_matrix = np.array([
            [np.cos(rotation_angle_radians), -np.sin(rotation_angle_radians), 0],
            [np.sin(rotation_angle_radians), np.cos(rotation_angle_radians), 0],
            [0, 0, 1]])
        return rotation_matrix

    # correct the number of particles by the nucleus/cell volume fraction
    # At the end of the function the positions are filtered to exclude those that fall inside the Rsph sphere.
    # This correction allows to mantain the original number of positions N after the filter.
    Naux = N
    if N > 1:
        Naux = int(N / (1.0 - 4 * np.power((Rsph+Rnp),3) / (3 * Hcyl * np.power(Rcyl-Rnp,2))))
        print(f'N corrected: {N}')
    else:
        Naux = 10
        print(f'N corrected: {N}')

    min_distance = 2*Rnp + 0.001
    Rmax = Rcyl - min_distance / 2
    # Half Height of the cylinder in nm
    HL = Hcyl - min_distance / 2
    zbins = 1
    zbinheight = Hcyl
    if N > 1000000:
        #zbins = N // 100000
        #zbinheight = Hcyl / zbins
        # the zbin must has the height of 10 np diameters
        zbins = int(Hcyl // (20*Rnp))
        zbinheight = Hcyl / zbins

    print(f'Number of z bins: {zbins}. Height of zbins: {zbinheight}.')
    if zbinheight < 2 * Rnp:
        print(f'Height of the zbin {zbinheight} smaller than particle diameter')

    # Generate random positions for the small spheres
    positions0 = np.empty((0, 3), dtype=float)
    positions1 = np.empty((0, 3), dtype=float)
    positions = np.empty((0, 3), dtype=float)
    n_part = 0
    while n_part < int(Naux / (4 * zbins)):
        # Generate random point inside the cylinder
        x = (Rmax * np.random.random())
        y = (Rmax * np.random.random())
        z = zbinheight*(np.random.random()-0.5)
        point = np.array([x, y, z])

        # sample the positions in 1 quadrant of one zbin
        if (np.sqrt(x * x + y * y) <= Rmax) and \
                (np.sqrt(x * x + y * y + z * z) > 0) and \
                (np.abs(z) < 0.5*(zbinheight - min_distance)):
            # Check if the point is far enough from the other small spheres
            if len(positions) == 0 or np.min(np.linalg.norm(positions0 - point, axis=1)) >= min_distance:
                positions0 = np.vstack([positions0, point])
                n_part += 1
                if n_part % 1000 == 0:
                    print(4 * zbins * n_part, 'out of', N)

    # obtain positions of other 3 quadrants applying pi/2 rotations
    positions1 = np.vstack((positions1, positions0))
    for i in range(3):
        rotation_angle_radians = (i + 1) * np.pi / 2
        rotated_points = np.dot(positions0, get_rotation_matrix(rotation_angle_radians).T)
        positions1 = np.vstack((positions1, rotated_points))

    # Generate position for each zbin by applying random rotations
    for i in range(zbins):
        rotation_angle_radians = 2 * np.pi * np.random.random()
        # Apply the rotation to the point
        # Apply the rotation to the stack of points
        rotated_points = np.dot(positions1, get_rotation_matrix(rotation_angle_radians).T)
        # zshift = i * zbinheight - 0.5 * zbins * zbinheight
        zshift = 0.5 * Hcyl * (2 * i / zbins + 1 / zbins - 1)
        zshift_array = np.full(rotated_points.shape, [0.0, 0.0, zshift])
        shifted_rotated_points = rotated_points + zshift_array
        positions = np.vstack((positions, shifted_rotated_points))

    # Filter the positions that are outside the sphere of radius Rsph and center at (0,0,0)
    center = np.array([0.0, 0.0, 0.0])  # Sphere's center
    Rmin = Rsph + Rnp
    filtered_points = filter_points_outside_sphere(positions, center, Rmin)
    np.random.shuffle(filtered_points)
    print(f'Total number of points generated: {len(filtered_points)}')

    # Print the positions of the small spheres
    f = open(positions_file, 'w')
    for i, p in enumerate(filtered_points):
        if N == 1 and i > 0:
            break
        # print(f"Small sphere {i+1}: x={p[0]:.2f}, y={p[1]:.2f}, z={p[2]:.2f}")
        f.write(str(p[0]) + " " + str(p[1]) + " " + str(p[2]) + "\n")
    f.close()
