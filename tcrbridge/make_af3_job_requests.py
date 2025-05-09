import json 
import pandas as pd
import argparse

def create_job_request(tcr_df, output_path):
    # Constants for the shared sequences (hla-a2 and b2m)
    seq4 = "MAVMAPRTLVLLLSGALALTQTWAGSHSMRYFFTSVSRPGRGEPRFIAVGYVDDTQFVRFDSDAASQRMEPRAPWIEQEGPEYWDGETRKVKAHSQTHRVDLGTLRGYYNQSEAGSHTVQRMYGCDVGSDWRFLRGYHQYAYDGKDYIALKEDLRSWTAADMAAQTTKHKWEAAHVAEQLRAYLEGTCVEWLRRYLENGKETLQRTDAPKTHMTHHAVSDHEATLRCWALSFYPAEITLTWQRDGEDQTQDTELVETRPAGDGTFQKWAAVVVPSGQEQRYTCHVQHEGLPKPLTLRWEPSSQPTIPIVGIIAGLVLFGAVITGAVVAAVMWRRKSSDRKGGSYSQAASSDSAQGSDVSLTACKV"
    seq5 = "MSRSVALAVLALLSLSGLEAIQRTPKIQVYSRHPAENGKSNFLNCYVSGFHPSDIEVDLLKNGERIEKVEHSDLSFSKDWSFYLLYYTEFTPTEKDEYACRVNHVTLSQPKIVKWDRDM"

    job_requests = []

    for _, row in tcr_df.iterrows():
        job = {
            "name": f"{row['tcr_id']}",
            "modelSeeds": [],
            "sequences": [
                {
                    "proteinChain": {
                        "sequence": row["full_seq_reconstruct_alpha_aa"],
                        "count": 1
                    }
                },
                {
                    "proteinChain": {
                        "sequence": row["full_seq_reconstruct_beta_aa"],
                        "count": 1
                    }
                },
                {
                    "proteinChain": {
                        "sequence": row['epitope_aa'],
                        "count": 1
                    }
                },
                {
                    "proteinChain": {
                        "sequence": seq4,
                        "count": 1
                    }
                },
                {
                    "proteinChain": {
                        "sequence": seq5,
                        "count": 1
                    }
                }
            ]
        }
        job_requests.append(job)
    
    # Write to file
    with open(output_path, 'w') as f:
        json.dump(job_requests, f, indent=4)
    
    print(f"Created {output_path} with {len(job_requests)} jobs")


def main():
    parser = argparse.ArgumentParser(description="Create job requests for TCRs")
    parser.add_argument("tcr_df_csv", type=str, help="Path to the csv file with the TCRs")
    parser.add_argument("output_path", type=str, help="Path to the save the output file (make sure it ends with .json)")
    args = parser.parse_args()

    if not args.output_path.endswith(".json"):
        raise ValueError("Output path must end with .json")
    if not args.tcr_df_csv.endswith(".csv"):
        raise ValueError("TCR dataframe must be a csv file")

    tcr_df = pd.read_csv(args.tcr_df_csv)
    # check if rows 'tcr_id', 'full_seq_reconstruct_alpha_aa', 'full_seq_reconstruct_beta_aa', 'epitope_aa' are in the dataframe
    required_columns = ['tcr_id', 'full_seq_reconstruct_alpha_aa', 'full_seq_reconstruct_beta_aa', 'epitope_aa']
    for col in required_columns:
        if col not in tcr_df.columns:
            raise ValueError(f"Column {col} is missing from the dataframe")
    # check if the dataframe is empty
    if tcr_df.empty:
        raise ValueError("The dataframe is empty")

    create_job_request(
        tcr_df=tcr_df, 
        output_path=args.output_path
        )

if __name__ == "__main__":
    main()
