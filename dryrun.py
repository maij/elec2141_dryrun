#!/usr/bin/env python3.4
import sys
import os
from glob import glob
print(sys.version)

print(
    """
#    This is a simple python script that will take a set of Xilinx ISE project files and compile them for simulation.
#    Once compiled, the simulation will be run with a specified testbench, and the output of each simulation will be 
#    diff'ed against a standard implementation's output.
#    
#    Written by Mark Johnson for the use of the UNSW School of Electrical Engineering.
    """
)

project_files = glob("*.prj");
print("Found Projects :")
for project in project_files:
    print("\t" + project)

print(
"""


"""        
)
tool_path = r"C:/Xilinx/14.4/ISE_DS/ISE/bin/nt64/"

command_arguments = {"fuse.exe" : "-intstyle ise -incremental -lib unisims_ver -lib unimacro_ver -lib xilinxcorelib_ver -o {output} -prj {prj} work.{top_level} work.glbl"}
ordered_commands = ["fuse.exe"]


# Run fuse.exe first to compile and elaborate the design
command = "fuse.exe"
for prj_file in project_files:
    unit_name = prj_file.strip(".prj")
    print("Processing project: " + unit_name + "\n")

    output_path = unit_name + "_isim.exe"
    print(tool_path + command + " " + command_arguments[command].format(prj = prj_file, output = output_path, top_level = unit_name))
    os.system(tool_path + command + " " + command_arguments[command].format(prj = prj_file, output = output_path, top_level = unit_name))
        
# Finished, wait on input
print("Done, press enter to terminate")
sys.stdin.readline()
