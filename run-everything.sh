set -eux

./for-each-project.sh  # checkout all projects
./make-runner.sh  # generate script for running mutations
./run_experiment-ALL.sh  # run mutations (by default with ALL operators)
./run-no-mutations.sh
