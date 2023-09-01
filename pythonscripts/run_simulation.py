from simulation_manager import Simulation_manager
import json
import os
import sys

sim_path = sys.argv[1]
config_file = sys.argv[2]
smanager = Simulation_manager(sim_path, config_file)

smanager.map_files()