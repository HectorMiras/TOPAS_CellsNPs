from simulation_manager import Simulation_manager
import json
import os
import sys

sim_path = sys.argv[1]
config_file = "simulation_config.json"
smanager = Simulation_manager(sim_path, config_file)

smanager.map_files()