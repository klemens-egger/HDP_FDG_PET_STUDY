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
input_data = pd.read_csv(PATHS["other_study_data_dir"] / "blood_concentrations.tsv", sep="\t")


def convert_dataframe(input_data, metabolite):

    # Only keep the rows where 'metabolite' is the required metabolite
    if metabolite == "DMT":
        metabolite_admin = "DMT admin"
    elif metabolite == "Harmine":
        metabolite_admin = "HAR admin"
    else:
        raise ValueError("Invalid metabolite name")
    metabolites = [metabolite_admin, metabolite]
    input_data = input_data[input_data["metabolite"].isin(metabolites)]
    # Create a new dataframe with the required columns
    output_data = input_data.copy()

    # Rename the "SubjectID" column to "ID"
    output_data = output_data.rename(columns={"participant_id": "ID"})
    # Transform the values in the "ID" column: "DHTP-01" -> 1, "DHTP-16" -> 16, ...
    output_data["ID"] = output_data["ID"].apply(lambda x: int(x.split("P")[1]))

    # Rename columns and add condition column
    output_data = output_data.rename(columns={"Timepoint_actual": "TIME"})
    output_data = output_data.rename(columns={"metabolite": "Metabolite"})
    output_data = output_data.rename(columns={"Molar_concentration [nM]": "Value"})
    output_data['Condition'] = '90(D)-120(H)'

    # Where 'Value' is 0.00 or NaN, replace the "Value" column with . (dot)
    output_data.loc[(output_data["Value"] == 0.00) | (output_data["Value"].isna()), "Value"] = "."

    # Create an editable copy of the "Value" column
    output_data["DV"] = output_data["Value"]
    # Where 'Metabolite' is metabolite_admin, replace the "DV" column with . (dot)
    output_data.loc[output_data["Metabolite"] == metabolite_admin, "DV"] = "."

    # Create an editable copy of the "Molar_concentration [nM]" column
    output_data["AMT"] = output_data["Value"]
    # Where 'Metabolite' is metabolite, replace the "AMT" column with . (dot)
    output_data.loc[output_data["Metabolite"] == metabolite, "AMT"] = "."


    # Drop the "Value" column
    output_data = output_data.drop(columns=["Value"])

    # Where 'DV' is a . (dot), make the 'MDV' column 1
    output_data["MDV"] = output_data["DV"].apply(lambda x: 1 if x == "." else 0)

    # Where 'AMT' is a . (dot), make the 'CMT' column 2 else 1
    output_data["CMT"] = output_data["AMT"].apply(lambda x: 2 if x == "." else 1)

    # Generate the "DOSE" column
    output_data["DOSE"] = output_data["Condition"]
    # Generate the "DOSE_DMT" column from the "DOSE" column: "60(D)-120(H)" -> 60, "90(D)-0(H)" -> 90
    output_data["DOSE_DMT"] = output_data["DOSE"].apply(lambda x: int(x.split("(")[0]))
    # Generate the "DOSE_HAR" column from the "DOSE" column: "60(D)-120(H)" -> 120, "90(D)-0(H)" -> 0
    output_data["DOSE_HAR"] = output_data["DOSE"].apply(lambda x: int(x.split("-")[1].split("(")[0]))
    # Modify the "DOSE" column from the "DOSE_DMT" and "DOSE_HAR" columns: "60(D)-120(H)" -> "60120", "90(D)-0(H)" -> "900"
    output_data["DOSE"] = output_data["DOSE_DMT"].astype(str) + output_data["DOSE_HAR"].astype(str)
    # Convert the "DOSE" column to integer
    output_data["DOSE"] = output_data["DOSE"].astype(int)
    # Rename the "DOSE_DMT" column to "DOSD" and the "DOSE_HAR" column to "DOSH"
    output_data = output_data.rename(columns={"DOSE_DMT": "DOSD", "DOSE_HAR": "DOSH"})


    # Create an empty "EVID" column (nan)
    output_data["EVID"] = None
    # Create an empty "STRT" column (nan)
    output_data["STRT"] = None

    if metabolite == "DMT":
        # Drop rows where "DOSD" is 0
        output_data = output_data[output_data["DOSD"] != 0]
        # Drop the "DOSD" column
        output_data = output_data.drop(columns=["DOSD"])
        control_dose_column = "DOSH"
    elif metabolite == "Harmine":
        # Drop rows where "DOSH" is 0
        output_data = output_data[output_data["DOSH"] != 0]
        # Drop the "DOSH" column
        output_data = output_data.drop(columns=["DOSH"])
        control_dose_column = "DOSD"

    # Reorder the columns
    output_data = output_data[["ID", "TIME", "AMT", "EVID", "DV", "MDV", "CMT", "DOSE", "STRT", control_dose_column, "Metabolite"]]

    return output_data

# # DMT
output_data = convert_dataframe(input_data, "DMT")
output_data_file_name = "DMTHAR_DMT.csv"
output_data.to_csv(f'{base_dir}/{output_data_file_name}', index=False)

# # Harmine
output_data = convert_dataframe(input_data, "Harmine")
output_data_file_name = "DMTHAR_HAR.csv"
output_data.to_csv(f'{base_dir}/{output_data_file_name}', index=False)

print(output_data)