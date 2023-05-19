from pythonscripts.simulation_manager import Simulation_manager
import json
import os

config_file = "simulation_config.json"
smanager = Simulation_manager(os.getcwd(), config_file)

smanager.map_files()