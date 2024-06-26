'''
 Python script that takes as first argument a number SPLITNUM, SPLITINDEX as second and the rest of arguments are filenames of files to be processed.
 For each file, find the number of histories line that contains the string 'NumberOfHistoriesInRun', read the number of histories, divide it by SPLITNUM and replace the line with the new value (must be integer).
 For example, line "i:So/I125Beam/NumberOfHistoriesInRun = 400000 # 19000000 histories correspond to 1 Gy if no phsp recycles" should be replaced by "i:So/I125Beam/NumberOfHistoriesInRun = 400000 # 19000000 histories correspond to 1 Gy if no phsp recycles" if SPLITNUM=4
 Also, line containing s:Ge/CellPHSPName, such as "s:Ge/CellPHSPName    = "SARRP_CellPHSP"  # some comment", should be replaced by "s:Ge/CellPHSPName    = "SARRP_CellPHSP_SPLITINDEX"  # some comment".
 Finally, all lines containing the strings "s:Sc" and "/OutputFile", such as "s:Sc/NucleusPHSP/OutputFile	= "outfilename"   # some comment", should be replaced as "s:Sc/NucleusPHSP/OutputFile	= "outfilename_SPLITINDEX"   # some comment"
'''

import sys
import re
import os


def process_file(input_file, splitnum, splitindex):
    output_file = f"{os.path.splitext(input_file)[0]}_part{splitindex}.txt"

    with open(input_file, 'r') as file:
        lines = file.readlines()

    with open(output_file, 'w') as file:
        for line in lines:
            # Find and process the NumberOfHistoriesInRun line
            if 'NumberOfHistoriesInRun' in line:
                match = re.search(r'NumberOfHistoriesInRun\s*=\s*(\d+)', line)
                if match:
                    original_value = int(match.group(1))
                    new_value = original_value // splitnum
                    line = re.sub(r'(NumberOfHistoriesInRun\s*=\s*)(\d+)', lambda m: m.group(1) + str(new_value), line,
                                  1)

            # Find and process the CellPHSPName line
            if 's:Ge/CellPHSPName' in line:
                line = re.sub(r's:Ge/CellPHSPName\s*=\s*"(.*?)"',
                              lambda m: f's:Ge/CellPHSPName = "{m.group(1)}_part{splitindex}"', line)

            # Find and process the OutputFile line
            if 's:Sc' in line and '/OutputFile' in line:
                line = re.sub(r's:Sc/(.*?)/OutputFile\s*=\s*"(.*?)"',
                              lambda m: f's:Sc/{m.group(1)}/OutputFile = "{m.group(2)}_part{splitindex}"', line)

            file.write(line)

    return output_file


def main():
    if len(sys.argv) != 4:
        print("Usage: {} <SPLITNUM> <SPLITINDEX> <input_file>".format(sys.argv[0]))
        sys.exit(1)

    splitnum = int(sys.argv[1])
    splitindex = int(sys.argv[2])
    input_file = sys.argv[3]

    if os.path.isfile(input_file):
        output_file = process_file(input_file, splitnum, splitindex)
        print(output_file)
    else:
        print(input_file)


if __name__ == "__main__":
    main()

