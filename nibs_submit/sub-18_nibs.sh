#!/bin/bash

sub=18

singularity run --cleanenv -B /home/data/sparse_dense/BIDS/sparseDense/:/bids_dir \
-B /home/data/sparse_dense/BIDS/sparseDense/derivatives/:/out_dir \
-B /home/data/sparse_dense/scratch/:/work_dir \
 /home/data/sparse_dense/BIDS/sparseDense/code/nibetaseries-v0.6.0.simg \
				 nibs -c trans_x trans_x_derivative1 trans_x_power2 trans_x_derivative1_power2 \
				 trans_y trans_y_derivative1 trans_y_power2 trans_y_derivative1_power2 \
				 trans_z trans_z_derivative1 trans_z_power2 trans_z_derivative1_power2 \
				 rot_x rot_x_derivative1 rot_x_power2 rot_x_derivative1_power2 \
				 rot_y rot_y_derivative1 rot_y_power2 rot_y_derivative1_power2 \
				 rot_z rot_z_derivative1 rot_z_power2 rot_z_derivative1_power2 \
				 --participant-label $sub \
				 -w /work_dir \
				 --estimator lss \
				 -hp 0.01 \
				 -sm 0 \
				 --hrf-model 'spm + derivative' \
				 /bids_dir \
				 fmriprep \
				 /out_dir \
				 participant