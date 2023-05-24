import json
import numpy as np
import sys
import shutil
import os
import configparser
from get_NP_positions import get_positions
from cell import Cell_class
from nanoparticles import NP_class

class Simulation_manager:

    def __init__(self, workingDir, config_file):

        #with open(config_file, 'r') as file:
            #json_data = json.load(file)
        
        self.workingDir = workingDir
        self.supportFilesDir = os.path.join(workingDir,"supportFiles")
        self.bashScriptsDir = os.path.join(workingDir, "bashscripts")
        self.simulationFilesDir = os.path.join(workingDir, "simulationFiles")
        self.runFilesDir = os.path.join(workingDir, "runFiles")
        self.pythonScripts = os.path.join(workingDir, "pythonscripts")

        self.NPFilesDict = {
            "AGuIX": "np_parameters_AGuIX.txt",
            "AuNP": "np_parameters_AuNP.txt",
            "AGuIX_Bi": "np_parameters_AGuIX_Bi.txt"
        }
        self.SourceFilesDict = {
            "SARRP": "source_parameters_SARRP.txt",
            "TrueBeam": "source_parameters_TrueBeam.txt",
            "I125": "source_parameters_I125.txt"
        }

        self.read_pyconfig(workingDir, config_file)
        self.cell = Cell_class()
        self.cell.read_file_parameters(os.path.join(self.supportFilesDir,self.cellParametersFile))
        self.np = NP_class()
        self.np.read_file_parameters(os.path.join(self.supportFilesDir, self.NPParametersFile))

        if self.NPsInMedium:
            # Get the number of NPs from the concentration
            vol_medium = 3.1415926 * 0.2 * np.power(1.25 * self.cell.rNucl, 2)
            npart = self.np.number_from_conc_volume(self.NPConcInMedium, vol_medium)
            self.NPNumberInMedium = npart
            self.np_positions_in_medium_file = "positions_in_medium_" + \
                                               str(self.NPNumberInMedium) + "_" + self.NPType + ".txt"
        else:
            self.np_positions_in_medium_file = "positions_in_medium_1_NP.txt"
        if self.NPsInCell:
            self.np_positions_in_cell_file = "positions_in_cell_" + \
                                             str(self.NPNumberInCell) + "_" + self.NPType + ".txt"
        else:
            self.np_positions_in_cell_file = "positions_in_cell_1_NP.txt"

        print("Simulation manager parameters:")
        for attr_name, attr_value in self.__dict__.items():
            print(f"{attr_name}: {attr_value}")
        print("")
        print("Cell parameters:")
        for attr_name, attr_value in self.cell.__dict__.items():
            print(f"{attr_name}: {attr_value}")
        print("")
        print("Nanoparticles parameters:")
        for attr_name, attr_value in self.np.__dict__.items():
            print(f"{attr_name}: {attr_value}")

    def read_pyconfig(self, workingDir, config_file):
        config = configparser.ConfigParser()
        config.read(os.path.join(workingDir, config_file))

        # Assumes the section name in your INI file is 'Simulation'
        simulation = config['Simulation']

        self.simulatePhase1 = simulation.getboolean('simulatePhase1')
        self.simulatePhase2 = simulation.getboolean('simulatePhase2')
        self.simulatePhase3 = simulation.getboolean('simulatePhase3')
        self.BeamSource = simulation["BeamSource"]
        self.NPsInMedium = simulation.getboolean("NPsInMedium")
        self.NPsInCell = simulation.getboolean("NPsInCell")
        self.NPType = simulation["NPType"]
        self.NPConcInMedium = simulation.getfloat("NPConcInMedium")
        self.NPNumberInCell = simulation.getint("NPNumberInCell")
        self.NPNumberInMedium = simulation.getint("NPNumberInMedium")
        self.sortNPPositions = simulation.getboolean("sortNPPositions")
        self.simScriptFile = simulation["simScriptFile"]
        self.cellParametersFile = simulation["cellParametersFile"]
        self.njobs = simulation.getint("njobs")
        self.nhistories = simulation.getint("nhistories")
        self.Phase1File = self.BeamSource + "_PHSP.txt"
        self.Phase2File = "Cell_and_medium_NPs.txt"
        self.Phase3File = None
        self.PHSP1Name = self.BeamSource + "_CellPHSP"
        self.NPParametersFile = "np_parameters_" + self.NPType + ".txt"
        self.SourceParametersFile = "source_parameters_" + self.BeamSource + ".txt"

    def read_json_config(self, workingDir, config_file):
        
        with open(os.path.join(workingDir,config_file), 'r') as file:
            json_data = json.load(file)

        self.simulatePhase1 = json_data['simulatePhase1']
        self.simulatePhase2 = json_data['simulatePhase2']
        self.simulatePhase3 = json_data['simulatePhase3']
        self.BeamSource = json_data["BeamSource"]
        self.NPsInMedium = json_data["NPsInMedium"]
        self.NPsInCell = json_data["NPsInCell"]
        self.NPType = json_data["NPType"]
        self.NPConcInMedium = json_data["NPConcInMedium"]
        self.NPNumberInCell = json_data["NPNumberInCell"]
        self.NPNumberInMedium = json_data["NPNumberInMedium"]
        self.sortNPPositions = json_data["sortNPPositions"]
        self.simScriptFile = json_data["simScriptFile"]
        self.cellParametersFile = json_data["cellParametersFile"]
        self.njobs = json_data["njobs"]
        self.nhistories = json_data["nhistories"]
        self.Phase1File = self.BeamSource + "_PHSP.txt"
        self.Phase2File = "Cell_and_medium_NPs.txt"
        self.Phase3File = None
        self.PHSP1Name = self.BeamSource + "_CellPHSP"
        self.NPParametersFile = "np_parameters_" + self.NPType + ".txt"
        self.SourceParametersFile = "source_parameters_" + self.BeamSource + ".txt"


    def map_files(self):

        # Empty runFilesDir
        runfiles = os.listdir(self.runFilesDir)
        for file in runfiles:
            file_path = os.path.join(self.runFilesDir, file)
            # Check if it's a file or directory
            if os.path.isfile(file_path):
                os.remove(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)

        # Create supportFiles dir and copy files
        destination_dir = os.path.join(self.runFilesDir, 'supportFiles')
        os.makedirs(destination_dir, exist_ok=True)
        for file in [self.NPParametersFile, self.SourceParametersFile, self.cellParametersFile]:
            source_file_path = os.path.join(self.supportFilesDir, file)
            destination_file_path = os.path.join(self.runFilesDir, 'supportFiles', file)
            shutil.copyfile(source_file_path, destination_file_path)
        for file in ["get_NP_positions.py", "sample_positions_in_cell.py", "sample_positions_in_medium.py"]:
            source_file_path = os.path.join(self.pythonScripts, file)
            destination_file_path = os.path.join(self.runFilesDir, 'supportFiles', file)
            shutil.copyfile(source_file_path, destination_file_path)

        # Map the Phase1File
        # check if the file path exists
        if self.simulatePhase1:
            self.map_phase1_file()

        # Map the Phase2File
        # check if the file path exists
        if self.simulatePhase2:
            self.map_phase2_file()

        # Process self.simScriptFile
        self.map_simScriptFile()

        # map python scripts for sampling NPs
        self.map_sample_positions_pyscripts()



    def map_sample_positions_pyscripts(self):
        # Map python scripts for generating np positions
        with open(os.path.join(self.pythonScripts, "sample_positions_in_medium.py"), 'r') as file:
            lines = file.readlines()

        for i in range(len(lines)):
            line = lines[i]
            if "positions_file =" in line:
                old_value = line.split("= ")[-1].strip()
                lines[i] = line.replace(old_value, f'\"{self.np_positions_in_medium_file}\"')
            if "Rmax =" in line:
                old_value = line.split("= ")[-1].strip()
                lines[i] = line.replace(old_value, f'1.25*{1000 * self.cell.rNucl}')
            if "Rnp =" in line:
                old_value = line.split("= ")[-1].strip()
                lines[i] = line.replace(old_value, f'{self.np.rNP}')
            if "N =" in line:
                old_value = line.split("= ")[-1].strip()
                lines[i] = line.replace(old_value, f'{self.NPNumberInMedium}')


        # write the file
        with open(os.path.join(self.runFilesDir, "supportFiles", "sample_positions_in_medium.py"), 'w') as file:
            file.writelines(lines)

        with open(os.path.join(self.pythonScripts, "sample_positions_in_cell.py"), 'r') as file:
            lines = file.readlines()

        for i in range(len(lines)):
            line = lines[i]
            if "positions_file =" in line:
                old_value = line.split("= ")[-1].strip()
                lines[i] = line.replace(old_value, f'\"{self.np_positions_in_cell_file}\"')
            if "Rmax =" in line:
                old_value = line.split("= ")[-1].strip()
                lines[i] = line.replace(old_value, f'{1000 * self.cell.rCell}')
            if "Rmin =" in line:
                old_value = line.split("= ")[-1].strip()
                lines[i] = line.replace(old_value, f'{1000 * self.cell.rNucl}')
            if "H =" in line:
                old_value = line.split("= ")[-1].strip()
                lines[i] = line.replace(old_value, f'{1000 * self.cell.height}')
            if "Rnp =" in line:
                old_value = line.split("= ")[-1].strip()
                lines[i] = line.replace(old_value, f'{self.np.rNP}')
            if "N =" in line:
                old_value = line.split("= ")[-1].strip()
                lines[i] = line.replace(old_value, f'{self.NPNumberInCell}')

        # write the file
        with open(os.path.join(self.runFilesDir, "supportFiles", "sample_positions_in_cell.py"), 'w') as file:
            file.writelines(lines)

    def map_phase1_file(self):
        # read the file Phase1 File
        with open(os.path.join(self.simulationFilesDir, self.Phase1File), 'r') as file:
            lines = file.readlines()

        for i in range(len(lines)):
            line = lines[i]
            # check if the line contains the keywords
            if "NumberOfHistoriesInRun" in line:
                old_file_name = line.split("= ")[-1].strip()
                lines[i] = line.replace(old_file_name, f'{self.nhistories}')
            if "includeFile" in line and "source_parameters_" in line:
                # get the old file name
                old_file_name = line.split("/")[-1].strip()
                # replace the old file name with the new one
                lines[i] = line.replace(old_file_name, self.SourceParametersFile)
            if "includeFile" in line and "np_parameters_" in line:
                old_file_name = line.split("/")[-1].strip()
                lines[i] = line.replace(old_file_name, self.NPParametersFile)
            if "s:Ge/CellPHSPName" in line:
                old_file_name = line.split("= ")[-1].strip()
                lines[i] = line.replace(old_file_name, f'\"{self.PHSP1Name}\"')
            if "s:Sc/DoseCell/OutputFile" in line:
                old_file_name = line.split("= ")[-1].strip()
                lines[i] = line.replace(old_file_name, f"\"DoseToCell_{self.BeamSource}\"")
            if "s:Ge/MediumVol/Material" in line:
                if not self.NPsInMedium:
                    old_values = line.split("= ")[-1].strip()
                    lines[i] = line.replace(old_values, f"\"G4_WATER\"")

            # update medium composition and density values from NPs concentration
            w_water, w_np, dens_tot = self.np.get_relweights_and_dens_from_conc(self.NPConcInMedium)
            if "Ma/MediumMaterial/Fractions" in line:
                old_values = line.split("= ")[-1].strip()
                lines[i] = line.replace(old_values, f"2 {w_water} {w_np}")
            if "Ma/MediumMaterial/Density" in line:
                old_values = line.split("= ")[-1].strip()
                lines[i] = line.replace(old_values, f"{dens_tot} g/cm3")

        # write the file
        with open(os.path.join(self.runFilesDir, self.Phase1File), 'w') as file:
            file.writelines(lines)

    def map_phase2_file(self):
        # read the file Phase2 File
        with open(os.path.join(self.simulationFilesDir, self.Phase2File), 'r') as file:
            lines = file.readlines()

        conc_str = str(self.NPConcInMedium)
        conc_str = conc_str.replace(".", "p")

        for i in range(len(lines)):
            line = lines[i]
            # check if the line contains the keywords
            if "includeFile" in line and "source_parameters_" in line:
                # get the old file name
                old_file_name = line.split("/")[-1].strip()
                # replace the old file name with the new one
                lines[i] = line.replace(old_file_name, self.SourceParametersFile)
            if "includeFile" in line and "np_parameters_" in line:
                old_file_name = line.split("/")[-1].strip()
                lines[i] = line.replace(old_file_name, self.NPParametersFile)
            if "s:Ge/CellPHSPName" in line:
                old_file_name = line.split("= ")[-1].strip()
                lines[i] = line.replace(old_file_name, f"\"{self.PHSP1Name}\"")
            if "s:Sc/NucleusPHSP/OutputFile" in line:
                old_file_name = line.split("= ")[-1].strip()
                new_file_name = f"\"nucleus_PHSP_{conc_str}mgml_{self.NPNumberInCell}_{self.NPType}_electrons\""
                lines[i] = line.replace(old_file_name, new_file_name)
            if "s:Sc/DoseNucleus_e/OutputFile" in line:
                old_file_name = line.split("= ")[-1].strip()
                new_file_name = f"\"DoseToNucleus_{conc_str}mgml_{self.NPNumberInCell}_{self.NPType}_electrons\""
                lines[i] = line.replace(old_file_name, new_file_name)
            if "s:Sc/DoseNucleus_g/OutputFile" in line:
                old_file_name = line.split("= ")[-1].strip()
                new_file_name = f"\"DoseToNucleus_{conc_str}mgml_{self.NPNumberInCell}_{self.NPType}_gammas\""
                lines[i] = line.replace(old_file_name, new_file_name)
            if "s:Ge/MediumNPPositionsFile" in line:
                old_file_name = line.split("= ")[-1].strip()
                new_file_name = f'\"./supportFiles/{self.np_positions_in_medium_file}\"'
                lines[i] = line.replace(old_file_name, new_file_name)
            if "s:Ge/CellNPPositionsFile" in line:
                old_file_name = line.split("= ")[-1].strip()
                new_file_name = f'\"./supportFiles/{self.np_positions_in_cell_file}\"'
                lines[i] = line.replace(old_file_name, new_file_name)
            if "s:Ge/MediumVol/Material" in line:
                if not self.NPsInMedium:
                    old_file_name = line.split("= ")[-1].strip()
                    lines[i] = line.replace(old_file_name, f"\"G4_WATER\"")
            if "s:Ge/MediumDetailed/ElementMaterial" in line:
                if not self.NPsInMedium:
                    old_values = line.split("= ")[-1].strip()
                    lines[i] = line.replace(old_values, f"\"G4_WATER\"")
            if "s:Ge/Cell/ElementMaterial" in line:
                if not self.NPsInCell:
                    old_values = line.split("= ")[-1].strip()
                    lines[i] = line.replace(old_values, f"\"G4_WATER\"")
            if "Ge/CellLayer/Material" in line:
                if not self.NPsInMedium:
                    old_values = line.split("= ")[-1].strip()
                    lines[i] = line.replace(old_values, f"\"G4_WATER\"")

            # update medium composition and density values from NPs concentration
            w_water, w_np, dens_tot = self.np.get_relweights_and_dens_from_conc(self.NPConcInMedium)
            if "Ma/MediumMaterial/Fractions" in line:
                old_values = line.split("= ")[-1].strip()
                lines[i] = line.replace(old_values, f"2 {w_water} {w_np}")
            if "Ma/MediumMaterial/Density" in line:
                old_values = line.split("= ")[-1].strip()
                lines[i] = line.replace(old_values, f"{dens_tot} g/cm3")

        # write the file
        with open(os.path.join(self.runFilesDir, self.Phase2File), 'w') as file:
            file.writelines(lines)

    def map_simScriptFile(self):
        with open(os.path.join(self.bashScriptsDir, self.simScriptFile), 'r') as file:
            lines = file.readlines()

        for i in range(len(lines)):
            line = lines[i]

            if line.startswith("ITER="):
                lines[i] = f'ITER={self.njobs} \n'

            if line.startswith("INFILE1="):
                lines[i] = f'INFILE1=\"{self.Phase1File}\" \n'
            if not self.simulatePhase1:
                if "topas $INFILE1" in line:
                    lines[i] = "#"+line
                if "cp $INFILE1 $DIR" in line:
                    lines[i] = "#"+line
                if "sed -i" and "$DIR/$INFILE1" in line:
                    lines[i] = "#"+line

            if line.startswith("INFILE2="):
                lines[i] = f'INFILE2=\"{self.Phase2File}\" \n'
            if not self.simulatePhase2:
                if "topas $INFILE2" in line:
                    lines[i] = "#"+line
                if "cp $INFILE2 $DIR" in line:
                    lines[i] = "#"+line
                if "sed -i" and "$DIR/$INFILE2" in line:
                    lines[i] = "#"+line

            if line.startswith("INFILE3="):
                lines[i] = f'INFILE3=\"{self.Phase3File}\" \n'
            if not self.simulatePhase3:
                if "topas $INFILE3" in line:
                    lines[i] = "#"+line
                if "cp $INFILE3 $DIR" in line:
                    lines[i] = "#"+line
                if "sed -i" and "$DIR/$INFILE3" in line:
                    lines[i] = "#"+line

            if line.startswith("DELFILE="):
                old_file_name = line.split("=")[-1].strip()
                new_file_name = f'\"{self.PHSP1Name}.phsp\"'
                lines[i] = line.replace(old_file_name, new_file_name)

            if self.sortNPPositions:
                if "DOSAMPLE=" in line:
                    lines[i] = "DOSAMPLE=true"
            else:
                if "DOSAMPLE=" in line:
                    lines[i] = "DOSAMPLE=false"

        # write the bash file
        with open(os.path.join(self.runFilesDir, "submit_script.sh"), 'w') as file:
            file.writelines(lines)
        
