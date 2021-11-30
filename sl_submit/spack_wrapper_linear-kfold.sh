#!/bin/bash

echo "checking python version prior to spack load"
python --version

echo "activating env"
. /home/data/software/experimental/ipsy-env/activate

echo "python version after spack load python"
python --version

echo "calling python script with for sub-$1"
python3 searchlight_svm-linear-kfold.py $1
