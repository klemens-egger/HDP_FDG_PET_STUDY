# HaD-PET FDG-PET Analysis

Reproducible analysis code for the human FDG-PET DMT + harmine study.

## Publication and Dataset

- Publication: `[Link to be added after publication release]`
- Dataset: `[OpenNeuro link to be added after dataset release]`

This repository is intended to rerun the main manuscript analyses from the curated OpenNeuro-ready BIDS dataset and write regenerated results into repo-local `outputs/` folders.

## Data source

The workflow expects a local copy of the curated BIDS dataset. In the current setup this is:

`/Volumes/X9_Pro_4TB/BIDS_HDP_data/01_Study_data_Openneuro_v1`

The imaging data are not stored in this repository. Paths are resolved through `config/paths.json`.

## Repository layout

- `code/01_kinfitr`: kinetic modeling in R (`kinfitr`) for preprocessing, Patlak modeling, and two-tissue modeling
- `code/02_pk_pd`: pharmacokinetic, pharmacodynamic, and subjective-intensity analyses
- `code/02_pk_pd/nca`: numbered NCA workflow scripts
- `code/03_surface_analysis`: whole-brain, surface, network, and figure-assembly notebooks
- `code/utils`: shared path helpers used by both Python and R scripts
- `config`: local path configuration
- `outputs`: regenerated figures, tables, model fits, and intermediate derived outputs

## Configuration

Before running the analyses, review `config/paths.json`. The key entries are:

- `bids_root`: path to the curated BIDS dataset
- `outputs_root`: repo-local output directory, typically `outputs`

Use `config/paths.example.json` as the template when setting this up on another machine.

## Running the analyses

At a broad level, the expected order is:

1. Run the `kinfitr` preprocessing and modeling scripts.
2. Run the numbered NCA workflow to generate pharmacokinetic summary tables.
3. Run the PK/PD and subjective-intensity notebooks.
4. Run the surface-analysis notebooks and composite-figure notebooks.

Some notebooks assume upstream outputs already exist, so the run order matters.

## Outputs

The scripts write regenerated files into repo-local folders, including:

- `outputs/kinfitr`
- `outputs/tables/pk_pd/nca`
- `outputs/figures/pk_pd`
- `outputs/figures/surface_analysis`

## Notes

- The repository is intended as a reproducible manuscript-analysis repo, not as a mirror of the original working directory.
- The numbered NCA scripts produce both full NCA tables and AUClast-only tables used in the manuscript analyses.
