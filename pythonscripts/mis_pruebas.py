import os
from simulation_manager import Simulation_manager
from cell import Cell_class
from nanoparticles import NP_class
from get_NP_positions import get_positions, get_positions_clustered
import numpy


def prueba_np_sample():
    wd = r'/home/hector/mytopassimulations/MGHsimulations/tests/np_sample/'
    cellParametersFile='cell_parameters_A549.txt'
    NPParametersFile='np_parameters_AuNP15.txt'
    positions_file = 'positions_in_cell.txt'
    cell = Cell_class()
    cell.read_file_parameters(os.path.join(wd, cellParametersFile))
    np = NP_class()
    np.read_file_parameters(os.path.join(wd, NPParametersFile))
    NPConcInCell=1.0     # mg Au / ml
    npart = np.number_from_conc_volume(NPConcInCell, cell.volume_cytoplasm())
    Rmax = cell.rCell*1000
    Rmin = cell.rNucl*1000
    H = cell.height*1000
    Rnp = np.rNP
    npart = get_positions(npart, Rmax, H, Rmin, Rnp, os.path.join(wd,positions_file))    
    a=1

def prueba_np_sample_clustered():
    wd = r'/home/radiofisica/hector/mytopassimulations/tests/clusteredNPs/'
    cellParametersFile='cell_parameters_MDAMB231.txt'
    NPParametersFile='np_parameters_AuNP15.txt'
    positions_file = 'positions_in_cell.txt'
    cell = Cell_class()
    cell.read_file_parameters(os.path.join(wd, cellParametersFile))
    np = NP_class()
    np.read_file_parameters(os.path.join(wd, NPParametersFile))
    NPConcInCell=5.0     # mg Au / ml
    npart = np.number_from_conc_volume(NPConcInCell, cell.volume_cytoplasm())
    Rmax = cell.rCell*1000
    Rmin = cell.rNucl*1000
    H = cell.height*1000
    Rnp = np.rNP

    cluster_distribution = 'LogNormal'  # Options: 'LogNormal', 'Gamma', 'Gaussian'

    npart, cluster_radii = get_positions_clustered(npart, Rmax, H, Rmin, Rnp, os.path.join(wd,positions_file),shape="Cylindrical", cluster_distribution= cluster_distribution)
    
    # cluster radii is a list of the radii of the clusters generated. Plot histogram of cluster_radii
    import matplotlib.pyplot as plt
    plt.hist(cluster_radii, bins=50)
    plt.xlabel('Cluster radius (nm)')
    plt.ylabel('Number of clusters')
    plt.title('Distribution of cluster radii')
    plt.savefig(os.path.join(wd, 'cluster_radii_histogram.png'))
    plt.show()
    plt.close()

    # Histogram: sum of NPs per radius bin (proportional to volume)
    cluster_radii = numpy.array(cluster_radii)
    weights = (cluster_radii ** 3) * 21529 / 476.7 ** 3
    plt.hist(cluster_radii, bins=50, weights=weights)
    plt.xlabel('Cluster radius (nm)')
    plt.ylabel('Sum of NPs in clusters')
    plt.title('NPs per cluster radius')
    plt.savefig(os.path.join(wd, 'nps_per_cluster_radius_histogram.png'))
    plt.show()
    plt.close()

    import matplotlib.pyplot as plt

    # Prepare data
    cluster_radii = numpy.array(cluster_radii)
    weights = (cluster_radii ** 3) * 21529 / 476.7 ** 3

    fig, ax1 = plt.subplots(figsize=(8,6))

    # Histogram 1: Number of clusters (left y-axis)
    color1 = 'tab:blue'
    n1, bins1, patches1 = ax1.hist(cluster_radii, bins=50, alpha=0.6, color=color1)
    ax1.set_xlabel('Cluster radius (nm)', fontsize=16)
    ax1.set_ylabel('Number of clusters', color=color1, fontsize=16)
    ax1.tick_params(axis='y', labelcolor=color1, labelsize=14)
    ax1.tick_params(axis='x', labelsize=14)

    # Histogram 2: NPs in clusters (right y-axis)
    ax2 = ax1.twinx()
    color2 = 'tab:red'
    n2, bins2, patches2 = ax2.hist(cluster_radii, bins=50, weights=weights, alpha=0.4, color=color2)
    ax2.set_ylabel('Sum of NPs in clusters', color=color2, fontsize=16)
    ax2.tick_params(axis='y', labelcolor=color2, labelsize=14)

   # plt.title('Cluster radii and NPs per cluster radius', fontsize=16)
    plt.tight_layout()
    plt.savefig(os.path.join(wd, 'combined_cluster_histogram.png'))
    plt.show()
    plt.close()

    a=1


def prueba_merge_topascellnp():
    sim_path = '/home/hector/mytopassimulations/MGHsimulations/TOPAS_CellsNPs'
    config_file = 'SimulationConfigFile.txt'
    smanager = Simulation_manager(sim_path, config_file)

    smanager.merge_DoseToNucleus_results()
    smanager.collect_np_number()


def prueba_np_number_calc():
    wd = r'/home/radiofisica/hector/mytopassimulations/TOPAS_CellsNPs/work/test-med1-smallcell1/supportFiles'
    cellParametersFile='cell_parameters_SmallCell.txt'
    NPParametersFile='np_parameters_AuNP15.txt'
    cell = Cell_class(shape="Cylindrical")
    cell.read_file_parameters(os.path.join(wd, cellParametersFile))
    np = NP_class()
    np.read_file_parameters(os.path.join(wd, NPParametersFile))
    NPConcInCell=1.0     # mg Au / ml
    npart = np.number_from_conc_volume(NPConcInCell, cell.volume_cytoplasm())
    a=1


prueba_np_sample_clustered()
#prueba_merge_topascellnp()

#prueba_np_number_calc()
