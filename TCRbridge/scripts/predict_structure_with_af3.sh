#!/bin/bash
#SBATCH -t 72:00:00
#SBATCH -p a100
#SBATCH --gres=gpu:1

# example usage: with json file name and output directory
# sbatch predict_structure_with_af3.sh GLC_jobs_requests.json /projects/alphafold3_tcr_pmhc

json_file_name=$1
if [ -z "$json_file_name" ]; then
    echo "Usage: $0 <json_file_name> <output_dir>"
    exit 1
fi

project_dir=$2
if [ -z "$output_dir" ]; then
    echo "Usage: $0 <json_file_name> <output_dir>"
    exit 1
fi

# run name is the name of the json file without the .json extension
run_name=$(basename "$json_file_name" .json)
date=$(date '+%Y-%m-%d_%H-%M-%S')
run_output_dir=${date}_${run_name}
# create the output directory if it doesn't exist
output_dir_base=$project_dir/af_output
if [ ! -d "$output_dir_base" ]; then
    mkdir -p "$output_dir_base"
fi
# create the output directory for this run
output_dir=$project_dir/af_output/$run_output_dir
mkdir -p "$output_dir"


echo "Running AlphaFold3 for $json_file_name"
echo "Output directory: $output_dir"
date
## adapt this to match your system
time apptainer exec --nv --no-home \
    --bind /projects/alphafold3_tcr_pmhc/af_input:$HOME/af_input \
    --bind /projects/alphafold3_tcr_pmhc/af_output/$date:$HOME/af_output \
    --bind /processing/alphafold3:$HOME/models \
    --bind /processing/alphafold3:$HOME/public_databases \
    --env DB_DIR=$HOME/public_databases \
    /processing/alphafold3/alphafold3.sif \
    python /app/alphafold/run_alphafold.py \
    --json_path=$HOME/af_input/$json_file_name \
    --model_dir=$HOME/models \
    --output_dir=$HOME/af_output
echo "AlphaFold3 finished"
date
