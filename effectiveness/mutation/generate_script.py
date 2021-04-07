__author__ = "Giovanni Grano"
__license__ = "MIT"
__email__ = "grano@ifi.uzh.ch"

from effectiveness.mutation.scan_project import *
from effectiveness.settings import *

import os
import subprocess
import pandas as pd
import sys
import re
import platform
import shutil


def get_script(project_list, operator='ALL'):
    """Write the script for the experiment on file
    
    Arguments
    -------------
    :param project_list: the list of the project to mutate
    :param operator: the name of the mutation operator
    :return the path name of the script generated
    """
    path = './run_experiment_{}.sh'.format(operator)
    try:
        os.mkdir(RESULTS_DIR)
        os.remove(path)
    except OSError as e:
        pass

    script = open(path, 'a')
    script.write(get_script_head())
    script.write('rm -rf {} logs\n'.format(MUTATION_RESULTS_DIR))
    script.write('mkdir {} logs\n'.format(MUTATION_RESULTS_DIR))

    for i, project in enumerate(project_list):
        test_counter = 0
        name = get_project_name(project)
        script.write('echo \'* {} out of {} -> {}\'\n'.format(i+1, len(project_list), name))
        script.write('mkdir {}/{}\n'.format(MUTATION_RESULTS_DIR, name))
        # move in, compile and test
        script.write('\n\necho \'* Compiling {}\'\n'.format(name))
        script.write(move_in(name))

        print('* Processing {}'.format(name))
        # look for submodules
        project_path = PROJECTS_DIR / name
        # copy the pom
        script.write(copy_pom())
        sub_modules = get_submodules(project_path)
        if sub_modules:
            # the project has submodules
            for module in sub_modules:
                sub_modules_path = project_path / module
                no_tests = write_mutation_per_unit(path_module=sub_modules_path,
                                                   script=script,
                                                   name=name,
                                                   module_name=module,
                                                   submodules=sub_modules,
                                                   operator=operator)
                test_counter += no_tests
            print('* Total tests for {} = {}'.format(name, test_counter))
        else:
            # the project has not submodules
            write_mutation_per_unit(path_module=project_path,
                                    script=script,
                                    name=name,
                                    operator=operator)
        script.write('echo \'* Restoring original pom\'\n')
        restore_pom(script)
        script.write(go_back())
    script.write(rename_results(operator))
    script.close()
    return path+'\n'


def rename_results(operator):
    """
    Renames the directory with the results at the end of the pipeline
    :param operator: the operator
    :return: the command to rename
    """
    new_name = MUTATION_RESULTS_DIR.with_name(MUTATION_RESULTS_DIR.name + '-' + operator)
    return 'mv {} {}\n'.format(MUTATION_RESULTS_DIR, new_name)


def write_mutation_per_unit(path_module, script, name, module_name=None, submodules=None, operator='ALL'):
    """
    Writes the commands for the mutation for a given units, either a project with no modules or a sub-module of a
    Maven project
    :param path_module: the path for the project of the path for the sub-module
    :param script: the output file
    :param name: the name of the project
    :param module_name: the name of the module
    :param submodules: the eventual list of submodules
    :return the number of pairs found
    """
    pairs = get_test_and_classes(project_path=path_module, project_name=name, module_name=module_name, save=True)
    generate_sequence_for_each_project(name, script, pairs,
                                       module=module_name,
                                       submodules=submodules,
                                       operator=operator)
    return len(pairs)


def calculate_results():
    """Returns the string used to call the compute results
    N.b: not used anymore, moved in the run.sh general script
    """
    python_command = 'python' if platform.system() == 'Darwin' else 'python3'
    return "{} {}/calculate_results.py".format(python_command, MUTATION_PACKAGE)


def generate_sequence_for_each_project(project, script, pairs, module=None, submodules=None, operator='ALL'):
    """Generates the code used to run maven for each of the classes in the project
    :param project: the name of the directory of the project
    :param script: the file to write on
    :param pairs: the list of Pair class that store the matches between tests and classes
    :param module: the name of the module. It can be None. If none, there are no modules
    :param submodules: the other submodules for this project. Is None if there are no submodules
    """
    timeout_command = 'gtimeout' if platform.system() == 'Darwin' else 'timeout'
    for pair in pairs:
        class_to_mutate = pair.get_qualified_source_name()
        test_to_run = pair.get_qualified_test_name()
        python_command = 'python' if platform.system() == 'Darwin' else 'python3'
        script.write('\n{} {}/pom_changer.py {} {} {} {}\n'.format(python_command, MUTATION_PACKAGE,
                                                                project, class_to_mutate, test_to_run, operator))
        script.write('echo \'* Mutating {} with operator {}\'\n'.format(class_to_mutate, operator))
        if not module:
            # the project has no modules
            script.write('{} 20m mvn org.pitest:pitest-maven:mutationCoverage -X -DoutputFormats=HTML '
                         '--log-file ../../logs/{}.txt\n'.format(timeout_command, test_to_run))
            script.write('mv target/pit-reports target/{}\n'.format(test_to_run))
            script.write('cp -r target/{} {}/{}\n\n'.format(test_to_run, MUTATION_RESULTS_DIR, project))
            # clean the target directory
            script.write('rm -rf target/{}\n'.format(test_to_run))
        else:
            # the project has modules
            script.write('{} 20m mvn org.pitest:pitest-maven:mutationCoverage -X -DoutputFormats=HTML '
                         '--log-file ../../logs/{}-{}.txt\n'.format(timeout_command, module, test_to_run))
            # the pattern for saving the directory when there are modules is the following:
            # module_name-fully.qualified.name
            script.write('mv {}/target/pit-reports {}/target/{}-{}\n'.format(module, module, module, test_to_run))
            for sub_module in submodules:
                script.write('rm -rf {}/target/pit-reports\n'.format(sub_module))
            script.write('cp -r {}/target/{}-{} {}/{}\n\n'.format(module, module, test_to_run, MUTATION_RESULTS_DIR,
                                                                  project))
            # clean the target directory
            script.write('rm -rf {}/target/{}-{}\n'.format(module, module, test_to_run))


def restore_pom(write, modified='pom.xml', cached='cached_pom.xml'):
    """Restore the original pom after all the executions

    Arguments
    -------------
    - write: the script
    - modified: the current version of the pom to delete
    - cached: the version to restore
    """
    write.write('rm -rf {}\n'.format(modified))
    write.write('mv {} {}\n'.format(cached, modified))


def copy_pom(new_name='cached_pom.xml'):
    """Copy the original pom in the cached version

    Arguments
    -------------
    - new_name: new name for the pom
    """
    return_string = '\n' \
                    'echo \'* Caching original pom\'\n' \
                    'cp pom.xml {}\n'.format(new_name)
    return return_string



def mvn_compile():
    """Returns the maven command needed to compile and package the project"""
    return "mvn clean install -DskipTests\n"


def mvn_test():
    """Returns the maven command needed to execute the test suite"""
    return "mvn test -Dmaven.test.failure.ignore=true\n"


def go_back():
    """Returns the command to go back to the main directory of the experiment"""
    return "cd ../..\n\n"


def move_in(dir_name):
    """Returns the command to move in the directory

    Arguments
    -------------
    - dir_name: the directory of the project under mutation analysis
    """
    return 'cd {}/'.format(PROJECTS_DIR) + dir_name + '\n'


def get_git_clone(project, name):
    """Returns the git clone command

    Arguments
    -------------
    - project: the name of the project, composed by both userid and repo name
    - name: the name of the folder in which clone the project to
    """
    return 'git clone https://github.com/' + project + '.git ' + name + '\n'


def get_project_name(name):
    """Returns the name of the project given the full name of github

    Arguments
    -------------
    - name: the full github name
    """
    m = re.search(r'^.*\/([^*]*).*$', name, re.M)
    return m.group(1)


def get_script_head():
    """Return the script for the bash script"""
    return "#!/bin/bash\n"


def get_homer():
    """ Funny header for the script"""
    homer = """
       ___  _____    
     .'/,-Y"     "~-.  
     l.Y             ^.           
     /\               _\_      "Let's generate the script for our mutation analysis!"   
    i            ___/"   "\ 
    |          /"   "\   o !   
    l         ]     o !__./   
     \ _  _    \.___./    "~\  
      X \/ \            ___./  
     ( \ ___.   _..--~~"   ~`-.  
      ` Z,--   /               \    
        \__.  (   /       ______) 
          \   l  /-----~~" /      
           Y   \          / 
           |    "x______.^ 
           |           \    
           j            Y

    """
    return homer


def generate():
    """
    Entry point for the elaboration
    """
    DEFAULT_OPERATORS = ['CONDITIONALS_BOUNDARY',
                         'NEGATE_CONDITIONALS',
                         'MATH',
                         'INCREMENTS',
                         'INVERT_NEGS',
                         'RETURN_VALS',
                         'VOID_METHOD_CALLS']
    ADDITIONAL_OPERATORS = ['CONSTRUCTOR_CALLS',
                           'INLINE_CONSTS',
                           'NON_VOID_METHOD_CALLS',
                           'REMOVE_CONDITIONALS',
                           'EXPERIMENTAL_MEMBER_VARIABLE',
                           'EXPERIMENTAL_SWITCH']
    ALL_OPERATORS = DEFAULT_OPERATORS + ADDITIONAL_OPERATORS

    if len(sys.argv) != 2:
        print("* Wrong usage!")
        print(f"* Usage: {sys.argv[0]} <csv_file_with_project_list.csv>")
        exit()

    print('Which kind of operators you want to run?')
    mode = input('1 = ALL (together)\n'
                 '2 = DEFAULTS (together)\n'
                 '3 = ALL (one at time)\n'
                 '4 = DEFAULTS (one at time)')
    try:
        mode = int(mode)
    except:
        print('invalid mode')
        exit(1)

    projects_csv = sys.argv[1]
    projects = pd.read_csv(projects_csv)['project'].unique().tolist()

    print(get_homer())

    print('* We are going to generate the mutation for the following projects:')
    for project in projects:
        print('- {}'.format(project))

    if not RESULTS_DIR.exists():
        print("* Creating the directory for the results")
        RESULTS_DIR.mkdir()
    else:
        if input("* Delete old results? [Y/N]") == "Y":
            for file in RESULTS_DIR.glob("*"):
                if file.is_dir():
                    shutil.rmtree(file)
                else:
                    file.unlink()

    with open('./run.sh', 'w') as script:
        if mode == 3:
            for operator in ALL_OPERATORS:
                print('Generating script for {}'.format(operator))
                script.write(get_script(projects, operator))
        elif mode == 4:
            for operator in DEFAULT_OPERATORS:
                print('Generating script for {}'.format(operator))
                script.write(get_script(projects, operator))
        elif mode == 2:
            print('Generating script for DEFAULT')
            script.write(get_script(projects, 'DEFAULT'))
        else:
            print('Generating script for ALL')
            script.write(get_script(projects))
