# Data and Figures for the QSIPrep manuscript

This repository contains the code and data used to process the
reconstructions and calculate the qc scores for the QSIPrep paper.
It contains notes on how and where each data was processed.



# QC data

## ABCD data

### MMPS-processed data

Official ABCD data was downloaded from NDAR using the first major
release of the ABCD preprocessed diffusion data. The data were
downloaded to `dopamine` using their java-based web downloader.

The subjects that overlapped with our internal ABCD BIDS data were
determined using `qc_scripts/abcd_check.py`

#### Concatenating data and calculating qc

The downloaded data could have more than 1 preprocessed dwi NIfTI file
and gradient set depending on the scanner used to collect the data.
My best guess is that their pipeline writes out as many images as are
supplied as input. Scanners that broke up the sampling scheme into
multiple scans would result in multiple preprocessed outputs.

To address this, special steps were taken in `qc_scripts/calc_mmps_qc.sh`
and in `qc_scripts/multishell_smoothness.sh` to concatenate the images
and their gradients if multiple were found.

### QSIPrep processed data

The ABCD BIDS data were curated before uploading to flywheel, so there
is no heuristic file for them. The QSIPrep preprocessing run was done
with `qc_scripts/abcd_run.py` and the qc values were downloaded using
`qc_scripts/dl_abcd_qc.py`.

The processed data was downloaded from FlyWheel using
`qc_scripts/download_preprocd_abcd.py`.
