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
input_data_file_name_full = "5_DHTP_PKdata_preprocessed_V4_nano_molar_NCA.csv"
output_data_file_name_full = "DHTP_PKdata_preprocessed_V4_ng_ml_NCA.csv"
input_data_file_name_auc = "5_DHTP_PKdata_preprocessed_V4_nano_molar_NCA_AUC_last_selected.csv"
output_data_file_name_auc = "DHTP_PKdata_preprocessed_V4_ng_ml_NCA_AUC_last_selected.csv"

# Convert the data from nano mole / L to ng/ml
# Molecular weights in g/mol
molecular_weights = {
    'DMT': 188.27,
    'Harmine': 212.25,
}

def convert_nmoleL_ngml(value_nmoleL, drug, molecular_weights):
    value_ngml = value_nmoleL * molecular_weights[drug] / 1000
    value_ngml = round(value_ngml, 2)
    return value_ngml

parameter_list = ['AUClast',
                  ]

full_parameter_list = ['C0',
                       'Cmax',
                       'simCmax',
                       'Clast',
                       'AUClast',
                       'simAUClast',
                       'AUMClast',
                       'simAUMClast',
                       'AUClower_upper',
                       'simAUClower_upper',
                       'AUCINF_obs',
                       'simAUCINF_obs',
                       'AUCINF_pred',
                       'simAUCINF_pred',
                       'AUMCINF_obs',
                       'AUMCINF_pred',
                       'Cmin',
                       'Cavg',
                       'AUCtau',
                       'AUMCtau']

def convert_dataframe(input_data, parameter_list):
    output_data = input_data.copy()
    for parameter in parameter_list:
        output_data.loc[output_data['Parameter'] == parameter, 'Value'] = output_data.loc[
            output_data['Parameter'] == parameter
        ].apply(lambda x: convert_nmoleL_ngml(x['Value'], x['Metabolite'], molecular_weights), axis=1)
    return output_data

input_data_full = pd.read_csv(f'{base_dir}/{input_data_file_name_full}')
input_data_auc = pd.read_csv(f'{base_dir}/{input_data_file_name_auc}')

output_data_full = convert_dataframe(input_data_full, full_parameter_list)
output_data_auc = convert_dataframe(input_data_auc, parameter_list)

output_data_full.to_csv(f'{base_dir}/{output_data_file_name_full}', index=False)
output_data_auc.to_csv(f'{base_dir}/{output_data_file_name_auc}', index=False)

print("Done")
