import argparse
import pathlib
from tcrbridge.parse_output import TCR_STRUCTURE_DATA
import pandas as pd

def predict():
    parser = argparse.ArgumentParser(description="Calculate TCRbridge scores for predicted structures")
    parser.add_argument("-i", "--input_path", type=str, required=True, help="Path to the input directories (should contain TCR ID directories with AlphaBridge interface scores)")
    parser.add_argument("-o", "--output_path", type=str, required=True, help="Path to the output CSV file for TCRbridge scores")
    args = parser.parse_args()

    input_path = args.input_path
    output_path = args.output_path
    if not pathlib.Path(input_path).exists():
        raise ValueError(f"Input directory {input_path} does not exist")
    if not pathlib.Path(input_path).is_dir():
        raise ValueError(f"Input path {input_path} is not a directory")   
    if not pathlib.Path(input_path).joinpath("AlphaBridge").exists():
        raise ValueError(f"AlphaBridge directory does not exist in {input_path}, make sure AlphaBridge was run correctly")
    if not output_path.endswith(".csv"):
        raise ValueError("Output path must end with .csv")


    input_path = pathlib.Path(input_path)
    tcr_id_entries = [
        entry.name
        for entry in input_path.iterdir()
        if entry.is_dir()
    ]
    
    structure_df = pd.DataFrame()
    for tcr_id in tcr_id_entries:
        try:
            alphabridge_path = pathlib.Path(input_path).joinpath(tcr_id, "AlphaBridge", "alphabridge_data.json")
            if not alphabridge_path.exists():
                print(f"Warning: No AlphaBridge data found for {tcr_id}, skipping...")
                continue
            tcr = TCR_STRUCTURE_DATA(
                                    data_dir=str(input_path),
                                    tcr_id=tcr_id,
                                    )

            if tcr is not None:
                tcr_structure_df = tcr.get_structure_df()
                structure_df = pd.concat([structure_df, tcr_structure_df])
        except Exception as e:
            print(f"Error processing {tcr_id}: {e}")
            continue
    
    structure_df.columns = structure_df.columns.str.replace('AC_', 'tcra-p_').str.replace('BC_', 'tcrb-p_').str.replace('CD_', 'p-mhc_').str.replace('AD_', 'tcra-mhc_').str.replace('BD_', 'tcrb-mhc_').str.replace('_contact', '')
    structure_df['tcra-p_ABi'] = structure_df['tcra-p_ABi'].fillna(0)
    structure_df['tcrb-p_ABi'] = structure_df['tcrb-p_ABi'].fillna(0)
    structure_df['TCRbridge_score'] = (structure_df['tcra-p_ABi'] + structure_df['tcrb-p_ABi'])/2

    prediction_df = structure_df[['tcr_id', 'TCRbridge_score']]
    prediction_df.to_csv(output_path, index=False)
    print(f"Saved TCRbridge scores to {output_path}")

if __name__ == "__main__":
    predict()
