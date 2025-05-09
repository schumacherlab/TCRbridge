# TCRbridge
TCRbridge predicts TCR-pMHC reactivity from AlphaFold3 output.

<!-- Installation -->

## Installation

### Conda from yaml
1. Clone the repo:
   ```sh
   git clone https://github.com/schumacherlab/TCRbridge.git
   ```
2. Navigate to the project directory:
   ```sh
   cd TCRbridge
   ```
3. Create conda environment:
   ```sh
   conda env create -f tcrbridge_env.yml
   conda activate tcrbridge_env
   ```

### Alphafold3 
#### Option1: Alphafold3 structure predictions using alphafoldserver
For smaller sets of TCR-pMHC complexes [alphafoldserver.com](https://alphafoldserver.com/) should suffice. The webserver allows for up to 20 protein complex predictions per day.
#### Option2: Alphafold3 structure predictions using a local installation
Follow instructions from https://github.com/google-deepmind/alphafold3 for local installation. 

### AlphaBridge
TCRbridge builds upon AlphaBridge (commit 3be1a44). To setup AlphaBridge:

1. Clone TCRbridge
```sh
cd TCRbridge
git clone https://github.com/PDB-REDO/AlphaBridge.git
cd AlphaBridge
git checkout 3be1a44
```

2. Inside `/TCRbridge/AlphaBridge/define_interfaces.py` adapt `define_interfaces()` function to only calculate the metrics for `contact_threshold_list = [0.4]`.


<!-- ~Performance -->
## Performance 
We ran all AlphaFold3 structure predictions on a sinlge A100 GPU. 
Calculating the TCRbridge score from AlphaFold3 output can be done on any machine in minutes.

<!-- Running -->
## Running

0. Generate the input files for Alphafold3
   Input data requirements:
   - CSV file with columns: `tcr_id`, `full_seq_reconstruct_alpha_aa`, `full_seq_reconstruct_beta_aa`, `epitope_aa`
   - The TCR alpha and beta sequences must be full-length sequences
   - The epitope sequence must match the peptide presented by HLA-A2 (otherwise you will need to adapt the .py script)

   ```sh
   python tcrbridge/make_af3_job_requests.py input_data.csv af3_job_requests/af3_job_request.json
   ```

1. Generate the AF3 structures 
   Option 1: Using [alphafoldserver.com](https://alphafoldserver.com/) (recommended for <20 structures)
   - Upload the generated json file to alphafoldserver.com
   - Download and extract the results to your output directory

   Option 2: Using local AlphaFold3 installation
   ```sh
   # Adapt paths in scripts/predict_structure_with_af3.sh to match your installation
   sbatch scripts/predict_structure_with_af3.sh af3_job_requests/af3_job_request.json /your/output/path/
   ```

2. Calculate interfaces and TCRbridge scores
   ```sh 
   # The script will:
   # 1. Calculate interfaces using AlphaBridge
   # 2. Generate TCRbridge scores for each structure
   bash scripts/predict_tcrbridge.sh
   ```

   Output: `tcrbridge_scores.csv` containing TCR IDs and their TCRbridge scores


<!-- Citing This Work -->
## Citing This Work
(<a href="https://www.biorxiv.org/content/10.1101/2025.04.28.651095v2" target="_blank">biorxiv</a>).

<!-- LICENSE -->
## License

Distributed under the Apache 2.0 License.


