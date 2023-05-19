import json
import numpy as np
import sys
import shutil
import os

class Simulation_manager:

    def __init__(self, workingDir, config_file):

        with open(config_file, 'r') as file:
            json_data = json.load(file)
        
        self.workingDir = workingDir
        self.supportFilesDir = os.path.join(workingDir,"supportFiles")
        self.bashScriptsDir = os.path.join(workingDir, "bashscripts")
        self.simulationFilesDir = os.path.join(workingDir, "simulationFiles")
        self.runFilesDir = os.path.join(workingDir, "runFiles")
        self.read_config(workingDir, config_file)
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

    def read_config(self, workingDir, config_file):
        
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
        if self.NPsInMedium:
            self.np_positions_in_medium_file = "positions_in_medium_" + \
                                               str(self.NPNumberInMedium) + "_" + self.NPType + ".txt"
        else:
            self.np_positions_in_medium_file = "positions_in_medium_1_NP.txt"
        if self.NPsInCell:
            self.np_positions_in_cell_file = "positions_in_cell_" + \
                                             str(self.NPNumberInCell) + "_" + self.NPType + ".txt"
        else:
            self.np_positions_in_cell_file = "positions_in_cell_1_NP.txt"


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

        # Map the Phase1File
        # check if the file path exists
        if self.simulatePhase1:
            # read the file Phase1 File
            with open(os.path.join(self.simulationFilesDir,self.Phase1File), 'r') as file:
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

        # write the file
        with open(os.path.join(self.runFilesDir, self.Phase1File), 'w') as file:
            file.writelines(lines)

        # Map the Phase2File
        # check if the file path exists
        if self.simulatePhase2:
            # read the file Phase1 File
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
                    new_file_name = f'\"./supporFiles/{self.np_positions_in_medium_file}\"'
                    lines[i] = line.replace(old_file_name, new_file_name)
                if "s:Ge/CellNPPositionsFile" in line:
                    old_file_name = line.split("= ")[-1].strip()
                    new_file_name = f'\"./supporFiles/{self.np_positions_in_cell_file}\"'
                    lines[i] = line.replace(old_file_name, new_file_name)

        # write the file
        with open(os.path.join(self.runFilesDir, self.Phase2File), 'w') as file:
            file.writelines(lines)

        # Process self.simScriptFile
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
                if "$SEED >> $DIR/$INFILE1" in line:
                    lines[i] = "#"+line

            if line.startswith("INFILE2="):
                lines[i] = f'INFILE2=\"{self.Phase2File}\" \n'
            if not self.simulatePhase2:
                if "topas $INFILE2" in line:
                    lines[i] = "#"+line
                if "cp $INFILE2 $DIR" in line:
                    lines[i] = "#"+line
                if "$SEED >> $DIR/$INFILE2" in line:
                    lines[i] = "#"+line

            if line.startswith("INFILE3="):
                lines[i] = f'INFILE3=\"{self.Phase3File}\" \n'
            if not self.simulatePhase3:
                if "topas $INFILE3" in line:
                    lines[i] = "#"+line
                if "cp $INFILE3 $DIR" in line:
                    lines[i] = "#"+line
                if "$SEED >> $DIR/$INFILE3" in line:
                    lines[i] = "#"+line

            if line.startswith("DELFILE="):
                old_file_name = line.split("=")[-1].strip()
                new_file_name = f'\"{self.PHSP1Name}.phsp\"'
                lines[i] = line.replace(old_file_name, new_file_name)

            if not self.sortNPPositions:
                if "python $PYFILE" in line:
                    lines[i] = "#"+line
                if "cp $PYFILE $DIR" in line:
                    lines[i] = "#"+line

        # write the file
        with open(os.path.join(self.runFilesDir, "submit_script.sh"), 'w') as file:
            file.writelines(lines)
