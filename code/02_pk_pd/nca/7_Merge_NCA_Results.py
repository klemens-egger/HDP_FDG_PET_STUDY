from pathlib import Path
import sys
import pandas as pd

UTILS_DIR = Path(__file__).resolve().parents[2] / "utils"
if str(UTILS_DIR) not in sys.path:
    sys.path.append(str(UTILS_DIR))

from project_paths import ensure_project_dirs, load_project_paths

PATHS = ensure_project_dirs(load_project_paths(Path(__file__).resolve()))
base_dir = PATHS["nca_output_root"]

input_data_file_name_full = "DHTP_PKdata_preprocessed_V4_ng_ml_NCA.csv"
input_data_file_name_AUC_last_selected = "DHTP_PKdata_preprocessed_V4_ng_ml_NCA_AUC_last_selected.csv"
output_data_file_name = "DHTP_PKdata_preprocessed_V4_ng_ml_NCA_merged.csv"

data_full = pd.read_csv(base_dir / input_data_file_name_full)
data_AUC_last_selected = pd.read_csv(base_dir / input_data_file_name_AUC_last_selected)

data_merged = pd.concat([data_full, data_AUC_last_selected], ignore_index=True)
data_merged.to_csv(base_dir / output_data_file_name, index=False)
print("Done")
