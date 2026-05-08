from pathlib import Path
import sys
import pandas as pd

UTILS_DIR = Path(__file__).resolve().parents[2] / "utils"
if str(UTILS_DIR) not in sys.path:
    sys.path.append(str(UTILS_DIR))

from project_paths import ensure_project_dirs, load_project_paths

PATHS = ensure_project_dirs(load_project_paths(Path(__file__).resolve()))
REPO_ROOT = PATHS["repo_root"]
base_dir = PATHS["nca_output_root"]

input_data_file_name_DMT_full = "nca_results_full_DMT.csv"
input_data_file_name_HAR_full = "nca_results_full_HAR.csv"
input_data_file_name_DMT_180 = "nca_results_AUC_180_DMT.csv"
input_data_file_name_HAR_180 = "nca_results_AUC_180_HAR.csv"

output_data_file_name_full = "5_DHTP_PKdata_preprocessed_V4_nano_molar_NCA.csv"
output_data_file_name_auc = "5_DHTP_PKdata_preprocessed_V4_nano_molar_NCA_AUC_last_selected.csv"

def relabel_condition(df):
    relabel_dict = {
        120: "0(D)-120(H)",
        60120: "60(D)-120(H)",
        90120: "90(D)-120(H)",
        120120: "120(D)-120(H)",
        900: "90(D)-0(H)",
        9060: "90(D)-60(H)",
        90180: "90(D)-180(H)"
    }
    df["Condition"] = df["Condition"].map(relabel_dict)
    return df

def backconvert_nca_outputs(input_data_dmt, input_data_har):
    input_data_dmt = input_data_dmt.copy()
    input_data_har = input_data_har.copy()

    input_data_dmt["Metabolite"] = "DMT"
    input_data_har["Metabolite"] = "Harmine"

    input_data = pd.concat([input_data_dmt, input_data_har], ignore_index=True)
    input_data = input_data.round(3)
    input_data.drop("Unnamed: 0", axis=1, inplace=True, errors="ignore")

    input_data.rename(columns={"ID": "participant_id"}, inplace=True)
    input_data["participant_id"] = input_data["participant_id"].apply(lambda x: "sub-HDP" + str(x).zfill(2))

    input_data.rename(columns={"DOSE": "Condition"}, inplace=True)
    input_data = relabel_condition(input_data)

    input_data = pd.melt(
        input_data,
        id_vars=["participant_id", "Condition", "Metabolite"],
        var_name="Parameter",
        value_name="Value",
    )

    input_data = input_data.dropna(subset=["Value"])
    return input_data


input_data_DMT_full = pd.read_csv(f'{base_dir}/{input_data_file_name_DMT_full}')
input_data_HAR_full = pd.read_csv(f'{base_dir}/{input_data_file_name_HAR_full}')
input_data_DMT_180 = pd.read_csv(f'{base_dir}/{input_data_file_name_DMT_180}')
input_data_HAR_180 = pd.read_csv(f'{base_dir}/{input_data_file_name_HAR_180}')

output_data_full = backconvert_nca_outputs(input_data_DMT_full, input_data_HAR_full)
output_data_auc = backconvert_nca_outputs(input_data_DMT_180, input_data_HAR_180)

output_data_full.to_csv(f'{base_dir}/{output_data_file_name_full}', index=False)
output_data_auc.to_csv(f'{base_dir}/{output_data_file_name_auc}', index=False)
