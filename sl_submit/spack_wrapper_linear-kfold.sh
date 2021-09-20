#!/bin/bash
echo "activating env"
. /home/data/software/current/share/spack/setup-env.sh

echo "checking python version prior to spack load"
python --version

echo "spack load python being called"
spack load python
spack load py-scikit-learn
spack load py-nilearn
spack load py-numpy
spack load py-nibabel

echo "python version after spack load python"
python --version

echo "calling python script with for sub-$1"
python searchlight_svm-linear-kfold.py $1