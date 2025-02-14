#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import numpy as np
import sys

def get_positions_efficient(N, Rcyl, Hcyl, Rsph, Rnp, positions_file):
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
    numberNPs = len(filtered_points)
    print(f'Total number of points generated: {numberNPs}')

    # Print the positions of the small spheres
    f = open(positions_file, 'w')
    for i, p in enumerate(filtered_points):
        if N == 1 and i > 0:
            break
        # print(f"Small sphere {i+1}: x={p[0]:.2f}, y={p[1]:.2f}, z={p[2]:.2f}")
        f.write(str(p[0]) + " " + str(p[1]) + " " + str(p[2]) + "\n")
    f.close()



    return numberNPs

def get_positions_binned(N, Rcyl, Hcyl, Rsph, Rnp, positions_file):
    """
    More efficient sampling inside a cylinder (cytoplasm) excluding the nucleus region,
    with overlap testing via spatial binning.
    All distances are in nm.
    """
    import math
    min_distance = 2 * Rnp + 0.001
    Rmax = Rcyl - min_distance / 2
    Rmin = Rsph + Rnp
    zmin = -Hcyl/2 + min_distance/2
    zmax = Hcyl/2 - min_distance/2
    # Adjust bin_size to be the max of Hcyl/10 or min_distance*4 to prevent too many bins.
    bin_size = max(Hcyl/100, min_distance * 4)

    # dictionary: key=(i,j,k), value=list of points in that bin
    bins = {}
    positions = []

    def get_bin_index(point):
        return (int(math.floor(point[0] / bin_size)),
                int(math.floor(point[1] / bin_size)),
                int(math.floor(point[2] / bin_size)))
    
    def neighbor_bins(bin_index):
        bx, by, bz = bin_index
        # range(b-1, b+2) iterates over b-1, b, and b+1, which is sufficient.
        for i in range(bx-1, bx+2):
            for j in range(by-1, by+2):
                for k in range(bz-1, bz+2):
                    yield (i, j, k)
    
    count = 0
    max_attempts = N * 100  # safety for infinite loops
    attempts = 0
    while count < N and attempts < max_attempts:
        attempts += 1
        x = (Rmax * (2 * np.random.random() - 1))
        y = (Rmax * (2 * np.random.random() - 1))
        if np.sqrt(x*x + y*y) > Rmax:
            continue
        z = np.random.uniform(zmin, zmax)
        if np.sqrt(x*x+y*y+z*z) <= Rmin:
            continue

        candidate = np.array([x, y, z])
        bin_idx = get_bin_index(candidate)
        overlap_found = False
        for nb in neighbor_bins(bin_idx):
            for pt in bins.get(nb, []):
                if np.linalg.norm(candidate - pt) < min_distance:
                    overlap_found = True
                    break
            if overlap_found:
                break
        if overlap_found:
            continue

        positions.append(candidate)
        bins.setdefault(bin_idx, []).append(candidate)
        count += 1
        if count % 1000 == 0:
            print(count, "out of", N)

    print(f"Total generated points: {len(positions)} after {attempts} attempts")
    with open(positions_file, 'w') as f:
        for i, p in enumerate(positions):
            if N == 1 and i > 0:
                break
            f.write(f"{p[0]} {p[1]} {p[2]}\n")
    return len(positions)

def get_positions(N, Rcyl, Hcyl, Rsph, Rnp, positions_file):
    """
    " Fuinction to sample N positons inside a cylinder of radius Rcyl and height Hcyl, excluding the inner volume of
    " a sphere of radius Rsph.
    " All distances are given in nm.
    " The sampled positions are printed to the txt file positions_file
    """

    # If the number of NPs is large, calls the effiecient sammpling method
    if N>50000:
        return get_positions_efficient(N, Rcyl, Hcyl, Rsph, Rnp, positions_file)

    min_distance = 2*Rnp + 0.001
    Rmax = Rcyl - min_distance / 2
    Rmin = Rsph + Rnp
    # Half Height of the cylinder in nm
    HL = Hcyl - min_distance / 2
    zbins = 1
    zbinheight = Hcyl


    if zbinheight < 2 * Rnp:
        print(f'Height of the zbin {zbinheight} smaller than particle diameter')

    # Generate random positions for the small spheres
    positions = np.empty((0, 3), dtype=float)
    n_part = 0
    while n_part < N:
        # Generate random point inside the cylinder
        x = (Rmax * (2*np.random.random()-1.0))
        y = (Rmax * (2*np.random.random()-1.0))
        z = zbinheight*(np.random.random()-0.5)
        point = np.array([x, y, z])

        # sample the positions in 1 quadrant of one zbin
        if (np.sqrt(x * x + y * y) <= Rmax) and \
                (np.sqrt(x * x + y * y + z * z) > Rmin) and \
                (np.abs(z) < 0.5*(zbinheight - min_distance)):
            # Check if the point is far enough from the other small spheres
            if len(positions) == 0 or np.min(np.linalg.norm(positions - point, axis=1)) >= min_distance:
                positions = np.vstack([positions, point])
                n_part += 1
                if n_part % 1000 == 0:
                    print(n_part, 'out of', N)

    numberNPs = n_part
    print(f'Total number of points generated: {numberNPs}')

    # Print the positions of the small spheres
    f = open(positions_file, 'w')
    for i, p in enumerate(positions):
        if N == 1 and i > 0:
            break
        # print(f"Small sphere {i+1}: x={p[0]:.2f}, y={p[1]:.2f}, z={p[2]:.2f}")
        f.write(str(p[0]) + " " + str(p[1]) + " " + str(p[2]) + "\n")
    f.close()



    return numberNPs
