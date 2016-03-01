#!/usr/bin/env python3.4
import sys
import os
from glob import glob

# Just a simple "new line" function
def nl():
    print(None)

def about_message():
    return \
    """
#    This is a simple python script that will take a set of Xilinx ISE project files and compile them for simulation.
#    Once compiled, the simulation will be run with a specified testbench, and the output of each simulation will be 
#    diff'ed against a standard implementation's output.
#    
#    Written by Mark Johnson for the use of the UNSW School of Electrical Engineering.
    """

def usage():
    return \
    """
    To use this program you needs to have a list of project files (.prj) with all source contained within them
    also stored in the relevant directories. Then run with the lab number provided as an argument.
    
    usage examples:
    ./dryrun.py lab1
    ./dryrun.py lab2
    """
    
# To help with booking showing which version of python is being used
print(sys.version + "\n")

# Exit with usage message if no arguments given
if len(sys.argv) <= 1: sys.exit(usage())

# Use the correct test bench for the current run
lab = sys.argv[1]
if   (lab == "lab1"): import conf.lab1 as lab_module
elif (lab == "lab2"): import conf.lab2 as lab_module
elif (lab == "lab3"): import conf.lab3 as lab_module
elif (lab == "lab4"): import conf.lab4 as lab_module
elif (lab == "lab5"): import conf.lab5 as lab_module
elif (lab == "lab6"): import conf.lab6 as lab_module
elif (lab == "lab7"): import conf.lab7 as lab_module
elif (lab == "lab8"): import conf.lab8 as lab_module
else                : sys.exit("ERROR : argument must be one of lab[1-8]\n\n" + usage())

test_bench_file = lab_module.test_bench_file

# After all the setup has completed successfully, print the header and 
print(about_message())

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
    #unit_name = prj_file.strip(".prj")
    unit_name = test_bench_file.strip(".v")
    nl()
    print("Processing project: " + unit_name)
    nl()

    print('Adding test bench "{tb_f}" to compile project file'.format(tb_f = test_bench_file))
    with open(prj_file, 'a') as file_handler:
        file_handler.write('verilog work "test_benches/{tb_f}"\n'.format(tb_f = test_bench_file))

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
