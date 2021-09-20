#######################
# searchlight svm 1.0 #
#######################

logs_dir=/home/data/sparse_dense/BIDS/sparseDense/code/sl_logs/
# create the logs dir if it doesn't exist
[ ! -d "$logs_dir" ] && mkdir -p "$logs_dir"

printf "# The environment
universe       = vanilla
getenv         = True
request_cpus   = 8
request_memory = 20G

# Execution
initial_dir    = /home/data/sparse_dense/BIDS/sparseDense/code/sl_submit/
executable     = spack_wrapper_linear-kfold.sh
\n"

for sub in 0{0..9} {10..20};
    do
        printf "arguments = ${sub}\n"
        printf "log       = ${logs_dir}/sub-${sub}_\$(Cluster).\$(Process).log\n"
        printf "output    = ${logs_dir}/sub-${sub}_\$(Cluster).\$(Process).out\n"
        printf "error     = ${logs_dir}/sub-${sub}_\$(Cluster).\$(Process).err\n"
        printf "Queue\n\n"
done