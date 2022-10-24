# Solver interface

## Required files

Regardless of the implementation language, the solver must contain the scripts __RUN.sh__ and __PREPARE.sh__ in its base directory. 

The script __PREPARE.sh__ is responsible for compilation and similar preparation steps. The script must be present even if it is not necessary (e.g. for Python implementations). 

The script __RUN.sh__ is responsible for running your solver on a given instance. The script takes two arguments, the first is a path to the instance JSON to be solved, and the second is a path to which the solver will save its solution. The script is responsible for passing these values to the solver.

During the evaluation, both the scripts __PREPARE.sh__ and __RUN.sh__ will be executed with the solver base directory as the current working directory.

## Solver IO

Your solver should take the same two arguments as the __RUN.sh__ script. You are guaranteed that absolute paths will be provided during the evaluation (for both instance and output). 

The solver must read the instance from the provided input path and save its solution to the provided output path.

Formats (structure, attributes) of input and output JSON files are described separately in the README_data.md.

# Evaluation environment

The evaluation will be held on __aisa.fi.muni.cz__. Please make sure that everything works properly in this environment. If you wish to test your code before submission on __aisa.fi.muni.cz__, make yourself familiar with the rules which apply to longer calculations (https://www.fi.muni.cz/tech/unix/computation.html.en). Namely, it is required to set lower priority to your calculation (command __nice__). Note that the evaluation run will be also executed under the __nice__ command.


## Modules

Your build may require additional tools not directly available on __aisa.fi.muni.cz__. If this is the case, tools such as cmake, 
maven etc. may be provided via the system of modules (https://www.fi.muni.cz/tech/unix/modules.html.en).
Any necessary modules should be added within the __PREPARE.sh__ script. Please double-check whether you load any modules 
upon login (e.g. __.bashrc__ file in your home directory) as such modules could be missing during the evaluation.


# Solver implementation

The solver is required to be coded either in C++, Java, or Python.

## Templates

All of the provided templates comply with the described requirements and may be compiled and executed on __aisa.fi.muni.cz__. You may 
adopt these templates or write the whole solver from scratch based on your preference. Especially for Java and C++, 
the templates may save you some time with loading and writing the JSON files.

## Libraries

The solver should not use any additional libraries apart from those for working with the JSON files.


# Submission recommendations

Before you submit your work, verify that your ZIP archive works on __aisa.fi.muni.cz__ as intended. Take the archive to be submitted, 
extract it on __aisa.fi.muni.cz__, compile the code by executing __PREPARE.sh__ and test your __RUN.sh__ script on some instances. 

It is important (especially for Windows users) to verify the submission ZIP rather than a git repository clone as git 
tends to convert between Windows and Linux end of lines. Windows-style end of lines may be problematic on __aisa.fi.muni.cz__ so make sure 
that the ZIP is OK in this regard.

Both stdout and stderr will be collected during the evaluation. Make sure that your solver does not produce excessive 
amounts of logging information. It is definitely OK to log the evolution of your objective function and similar information, 
but please refrain from logging whole solutions or even complete neighborhoods.
