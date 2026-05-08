get_script_dir <- function() {
  cmd_args <- commandArgs(trailingOnly = FALSE)
  file_arg <- grep("^--file=", cmd_args, value = TRUE)
  if (length(file_arg) > 0) {
    return(dirname(normalizePath(sub("^--file=", "", file_arg[1]), winslash = "/", mustWork = TRUE)))
  }

  frame_files <- vapply(sys.frames(), function(env) {
    if (!is.null(env$ofile)) env$ofile else NA_character_
  }, character(1))
  frame_files <- frame_files[!is.na(frame_files)]
  if (length(frame_files) > 0) {
    return(dirname(normalizePath(frame_files[1], winslash = "/", mustWork = TRUE)))
  }

  if (requireNamespace("rstudioapi", quietly = TRUE) && rstudioapi::isAvailable()) {
    active_path <- rstudioapi::getActiveDocumentContext()$path
    if (nzchar(active_path)) {
      return(dirname(normalizePath(active_path, winslash = "/", mustWork = TRUE)))
    }
  }

  stop("Could not determine the script location. Run the script with Rscript, source() it from file, or open it directly in RStudio.")
}

find_repo_root <- function(start) {
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

repo_root <- find_repo_root(get_script_dir())
source(file.path(repo_root, "code", "utils", "project_paths.R"))
paths <- load_project_paths(repo_root)
nca_output_dir <- file.path(paths$outputs_root, "tables", "pk_pd", "nca")
dir.create(nca_output_dir, recursive = TRUE, showWarnings = FALSE)

library(ncappc)
library(dplyr)
library(tidyverse)

dataset <- read.csv(file.path(nca_output_dir, "DMTHAR_DMT.csv"))

filtered_dataset <- dataset %>%
  filter(TIME <= 540)

out_full <- ncappc(obsFile = filtered_dataset,
                   onlyNCA = TRUE,
                   str1Nm = "DOSE",
                   doseType = "ns",
                   adminTyp = "extravascular",
                   method = "linearup-logdown",
                   LambdaTimeRange = NULL,
                   LambdaExclude = NULL,
                   extrapolate = TRUE,
                   AUCTimeRange = NULL,
                   printOut = FALSE,
                   evid = FALSE,
                   noPlot = FALSE)

nca_results_full <- out_full$ncaOutput
AUC_timewindow <- out_full$ncaOutput %>%
  select(ID, DOSE, AUClast)

write.csv(nca_results_full, file.path(nca_output_dir, "nca_results_full_DMT.csv"))
write.csv(AUC_timewindow, file.path(nca_output_dir, "nca_results_AUC_180_DMT.csv"))
