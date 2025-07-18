import os
from simulation_manager import Simulation_manager
from cell import Cell_class
from nanoparticles import NP_class
from get_NP_positions import get_positions, get_positions_clustered


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
    wd = r'/home/hector/mytopassimulations/MGHsimulations/tests/np_sample_clustered/'
    cellParametersFile='cell_parameters.txt'
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

    cluster_distribution = 'LogNormal'  # Options: 'LogNormal', 'Gamma', 'Gaussian'

    npart, cluster_radii = get_positions_clustered(npart, Rmax, H, Rmin, Rnp, os.path.join(wd,positions_file),shape="Cylindrical", cluster_distribution= cluster_distribution)
    
    # cluster radii is a list of the radii of the clusters generated. Plot histogram of cluster_radii
    import matplotlib.pyplot as plt
    plt.hist(cluster_radii, bins=20)
    plt.xlabel('Cluster radius (nm)')
    plt.ylabel('Number of clusters')
    plt.title('Distribution of cluster radii')
    plt.savefig(os.path.join(wd, 'cluster_radii_histogram.png'))
    plt.show()
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
