from __future__ import annotations

import json
from pathlib import Path


def find_repo_root(start: Path | None = None) -> Path:
    start = Path.cwd().resolve() if start is None else Path(start).resolve()
    for candidate in [start, *start.parents]:
        if (candidate / "config" / "paths.json").exists():
            return candidate
    raise FileNotFoundError("Could not locate public repo root containing config/paths.json")


def load_project_paths(start: Path | None = None) -> dict[str, Path]:
    repo_root = find_repo_root(start)
    config = json.loads((repo_root / "config" / "paths.json").read_text())

    def resolve(value: str | None) -> Path | None:
        if value is None:
            return None
        p = Path(value)
        return p if p.is_absolute() else (repo_root / p)

    outputs_root = resolve(config.get("outputs_root", "outputs"))
    bids_root = resolve(config["bids_root"])

    paths = {
        "repo_root": repo_root,
        "bids_root": bids_root,
        "derivatives_root": bids_root / "derivatives",
        "other_study_data_dir": bids_root / "derivatives" / "01_other_study_data",
        "participants_file": bids_root / "participants.tsv",
        "outputs_root": outputs_root,
        "figures_root": outputs_root / "figures",
        "tables_root": outputs_root / "tables",
        "logs_root": outputs_root / "logs",
        "kinfitr_output_root": outputs_root / "kinfitr",
        "pk_pd_tables_root": outputs_root / "tables" / "pk_pd",
        "pk_pd_figures_root": outputs_root / "figures" / "pk_pd",
        "nca_output_root": outputs_root / "tables" / "pk_pd" / "nca",
        "surface_figures_root": outputs_root / "figures" / "surface_analysis",
        "surface_tables_root": outputs_root / "tables" / "surface_analysis",
        "demographics_tables_root": outputs_root / "tables" / "demographics",
    }
    return paths


def ensure_project_dirs(paths: dict[str, Path] | None = None) -> dict[str, Path]:
    paths = load_project_paths() if paths is None else paths
    for key in (
        "figures_root",
        "tables_root",
        "logs_root",
        "kinfitr_output_root",
        "pk_pd_tables_root",
        "pk_pd_figures_root",
        "nca_output_root",
        "surface_figures_root",
        "surface_tables_root",
        "demographics_tables_root",
    ):
        paths[key].mkdir(parents=True, exist_ok=True)
    return paths
