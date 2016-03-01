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

# Just a simple "new line" function
def nl():
    print("")

# Environment variables used during simulation
env_vars = {
    "XILINX"          : r"C:\Xilinx\14.4\ISE_DS\ISE",
    "PLATFORM"        : r"nt",
    "LD_LIBRARY_PATH" : r"%XILINX%\lib\%PLATFORM%",
    "PATH"            : os.environ["PATH"] + r";%XILINX%\lib\%PLATFORM%;%XILINX%\bin\%PLATFORM%",
}
for env in env_vars.keys():
    print("{env: <16} := {value}".format(env = env, value = env_vars[env]))
    os.environ[env] = env_vars[env]
#for env in os.environ.keys():
#    print("{env: <16} := {value}".format(env = env, value = os.environ[env]))

project_files = glob("*.prj")
nl()
print("Found Projects :")
for project in project_files:
    print("\t" + project)

print(
"""


"""        
)
tool_path = r"C:/Xilinx/14.4/ISE_DS/ISE/bin/nt64/"

command_arguments = {
                    "fuse.exe" : '-intstyle ise -incremental -lib unisims_ver -lib unimacro_ver -lib xilinxcorelib_ver -o {output} -prj {prj} -top "work.{top_level}" -top "work.glbl"',
                    "isim"     : '-intstyle ise -tclbatch isim.cmd -wdb {top_level}.wdb'
                    }
ordered_commands = ["fuse.exe"]


# Run fuse.exe first to compile and elaborate the design
print(
"""

#####################################
Compiling and elaborating all designs
#####################################
"""
)
command = "fuse.exe"
for prj_file in project_files:
    unit_name = prj_file.strip(".prj")
    nl()
    print("Processing project: " + unit_name)
    nl()

    output_path = unit_name + "_isim.exe"
    print("Running " + tool_path + command + " " + command_arguments[command].format(prj = prj_file, output = output_path, top_level = unit_name))
    os.system(tool_path + command + " " + command_arguments[command].format(prj = prj_file, output = output_path, top_level = unit_name))
        
# Run each isim wrapper to simulate each design
print(
"""

#####################################
       Simulating all designs
#####################################
"""
)

command = "isim"
for sim in glob("*_isim.exe"):
    unit_name = sim.strip(".exe")
    nl()
    print("Simulating project: " + unit_name)
    nl()

    print("Running " + sim + " " + command_arguments[command].format(top_level = unit_name))
    os.system(         sim + " " + command_arguments[command].format(top_level = unit_name))

    
# Finished, wait on input
print("Done, press enter to terminate")
sys.stdin.readline()
