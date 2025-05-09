#!/bin/bash

# activate conda environment
conda activate tcrbridge_env

# Accept input directory as argument
if [ -z "$1" ]; then
    echo "Usage: $0 <input_directory>"
    exit 1
fi
indirectory="$1"

# also an out_file as argument
if [ -z "$2" ]; then
    echo "Usage: $0 <input_directory> <output_file>"
    exit 1
fi
out_file="$2"

# 1. Define interfaces for each predicted structure
for dir in $indirectory/*/; do
    echo "Calculating ALphaBridge scores for: $dir"
    python3 ../AlphaBridge/define_interfaces.py -i $dir
done

echo "Calculating TCRbridge scores for: $indirectory"
python3 ../tcrbridge/predict.py -i $indirectory -o $out_file


