find_repo_root <- function(start = getwd()) {
  current <- normalizePath(start, winslash = "/", mustWork = TRUE)
  repeat {
    if (file.exists(file.path(current, "config", "paths.json"))) {
      return(current)
    }
    parent <- dirname(current)
    if (identical(parent, current)) {
      stop("Could not locate repo root containing config/paths.json")
    }
    current <- parent
  }
}

load_project_paths <- function(start = getwd()) {
  repo_root <- find_repo_root(start)
  config <- jsonlite::read_json(file.path(repo_root, "config", "paths.json"), simplifyVector = TRUE)

  resolve_path <- function(path_value) {
    if (is.null(path_value) || identical(path_value, "")) {
      return(NULL)
    }
    if (grepl("^/", path_value)) {
      return(path_value)
    }
    return(file.path(repo_root, path_value))
  }

  outputs_root <- resolve_path(ifelse(is.null(config$outputs_root), "outputs", config$outputs_root))
  bids_root <- resolve_path(config$bids_root)

  paths <- list(
    repo_root = repo_root,
    bids_root = bids_root,
    derivatives_root = file.path(bids_root, "derivatives"),
    other_study_data_dir = file.path(bids_root, "derivatives", "01_other_study_data"),
    participants_file = file.path(bids_root, "participants.tsv"),
    outputs_root = outputs_root,
    figures_root = file.path(outputs_root, "figures"),
    tables_root = file.path(outputs_root, "tables"),
    logs_root = file.path(outputs_root, "logs"),
    kinfitr_output_root = file.path(outputs_root, "kinfitr")
  )

  dir.create(paths$figures_root, recursive = TRUE, showWarnings = FALSE)
  dir.create(paths$tables_root, recursive = TRUE, showWarnings = FALSE)
  dir.create(paths$logs_root, recursive = TRUE, showWarnings = FALSE)
  dir.create(paths$kinfitr_output_root, recursive = TRUE, showWarnings = FALSE)

  paths
}
