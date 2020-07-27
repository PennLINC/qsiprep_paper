# Data and Figures for the QSIPrep manuscript

This repository contains the code and data used to process the
reconstructions and calculate the qc scores for the QSIPrep paper.
It contains notes on how and where each data was processed.


# FWHM estimation

A key feature of pipelines is that they perform spatial transformations on
the input data to correct geometric issues like distortion and motion.
The application of these transformations can add an artificial smoothness
to the output data. We want to minimize this artifact while still applying
the corrections for the original artifacts.

We estimate the FWHM using AFNI's `3dFHWMx`. Although not the original intention
of this program, `3dFWHMx` estimates spatial smoothness by calculating the
spatial autocorrelation function (ACF) at each voxel within a brain mask.
Here we use these ACFs to estimate the FWHM of a 3D Gaussian kernel that
best fits the data. These were estimated on the outputs from other pipelines
and from QSIPrep outputs using the script `qc_scripts/multishell_smoothness.sh`.




# QC data sourcing and processing

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
`qc_scripts/download_preprocd_abcd.py`. The completeness of
the data set was checked with `qc_scripts/abcd_info.py`.

## HCP (HCP-Lifespan) data

This data was collected by Dr. Geoff Aguirre at UPenn. His group uploaded
it to FlyWheel and ran the HCP Diffusion pipeline v0.15 on it.

### HCP Diffusion pipeline data and qc

The HCP-preprocessed data was downloaded to `dopamine` using the
`qc_scripts/download_preprocd_hcp.py` and
`qc_scripts/download_preprocd_hcp_grads.py` scripts. The gradients
were later needed to extract b=0 volumes for estimating FWHM.

The qc scores for the HCP-diffusion pipeline data were calculated
using the `qc_scripts/calc_hcp_qc.sh` script.

### Processing HCP data with QSIPrep

#### BIDS curation and download from FlyWheel

This project needed to be BIDS curated before running QSIPrep. This was
done using `fwheudiconv` initially with the heuristic file
`qc_scripts/tome_heuristic.py` and later
`qc_scripts/tome_ses1_heuristic_nonunique.py` to deal with cancelled scans.
The gear was launched using `qc_scripts/tome_fwheudiconv_run.py`.

Once curated, the BIDS data was downloaded to `dopamine` using the FlyWheel
CLI tool with `fw export BIDS`. It was downloaded to
`/storage/mcieslak/multishell_qc/tome`.

#### Patching QSIPrep to match the HCP Diffusion pipeline outputs

The HCP acquisitions acquire the entire 199-direction sampling scheme
twice: once in each phase encoding direction. The HCP pipelines run
`eddy` on the 398 concatenated images and write out the 398
motion/eddy/distortion-corrected images. These images are ultimately
separated and images sampling the same coordinate in q-space in the
original scheme are averaged together.

QSIPrep 0.8.0 does not implement this averaging, so a patch was necessary
to match the outputs from the HCP diffusion pipeline. Version 0.9.0beta1
was released with this functionality and the HCP data were run with this
version. The full patch can be viewed here: https://github.com/PennBBL/qsiprep/commit/997fedb7c8629ff845b65cc0c9dd815b560f8886. The CI didn't pass because of a
CircleCI-related issue that is fixed in the subsequent commit.

#### Running QSIPrep with Docker

Instead of running on FlyWheel, the HCP data was processed locally on
`dopamine`. This was done because there is a NVIDIA GPU on `dopamine` that
sped up the running of `eddy` by more than a factor of 10. Running the CPU
version on FlyWheel was taking up to 56 hours per subject, which was
prohibitive. The results are located in
`/storage/mcieslak/multishell_qc/tome_output`. The run of `eddy` was configured
to both use the GPU and use `--flm quadratic` to match the HCP diffusion pipelines.
The exact eddy params can be found in `qc_scripts/eddy_params.json`.

The qc data were collected
using `qc_scripts/dl_hcp_qc.py`. The script name is misleading because the
data was all located on the local machine. All it really does is aggregate
the qc files.

## PNC (DTI 64) data

### Roalf/Baum preprocessed data

The other-pipeline preprocessed data was stored a NFS drive on `cfn` accessible as
`/data/joy/BBL/studies/pnc/processedData/diffusion/pncDTI_2016_04/`. The preprocessed
data were gathered using `qc_scripts/from_cfn/pnc-link.sh`. QC values were calculated
using `qc_scripts/from_cfn/pnc_qc.sh`. The images and their gradients were copied to
`dopamine`, where the FWHMs were calculated.

### QSIPrep processed data

The PNC cohort had already been run through QSIPrep by Dr. Josiane Bourque, but
she used upsampling, which would interfere with the qc comparison. Therefore,
a random subset of 125 subjects were selected from Josiane's cohort (which had
previously passed qc) using numpy's `random.choice` function.
The QSIPrep gear was run via `qc_scripts/pnc_2mm.py` and the results were
downloaded via `qc_scripts/dl_pnc_qc.py`.

The preprocessed images and gradients were downloaded to `dopamine` via
`qc_scripts/download_preprocd_pnc.py` and `qc_scripts/download_preprocd_pnc_grads.py`.
These were used as inputs for FWHM calculation.

## GRMPY (MultiShell 113) data

### Pines preprocessed data

The other-pipeline data for was also stored on `cfn` and was gathered to one place
using `qc_scripts/from_cfn/grmpy-link.sh`. These images and gradients were used to calculate
the qc metric via `qc_scripts/from_cfn/grmpy_qc.sh`. The images and gradients were
downloaded to `dopamine` where they were used to estimate FWHM. The original images
were located at `/data/jux/BBL/projects/multishell_diffusion/processedData/multishellPipelineFall2017`.

### QSIPrep processing

The GRMPY data on FlyWheel needed to be re-curated so fieldmaps would be correctly
represented in BIDS. Once this was done QSIPrep was run on them using
`qc_scripts/grmpy_run.py`. The qc values were downloaded using `qc_scripts/dl_grmpy_qc.py`,
the images were downloaded using `qc_scripts/download_preprocd_grmpy.py` and the gradients
were downloaded using `qc_scripts/download_preprocd_grmpy_grads.py`.

## Pitt DSI (DSI 113)

### Raw data and QSIPrep
These images were processed by Laura Cabral and Will Foran at Pitt. The QC files were
provided by them.

## CRASH DSI Q5 (DSI 258)

### Raw data

BIDS data were copied from the BIC compute cluster at UCSB to the `CUBIC` cluster.
They exist on `CUBIC` at `/cbica/projects/GURLAB/projects/shoreline/crash_data`.


## SuperShell Q7 (DSI 789)

Both the raw and preprocessed data were downloaded from FlyWheel. The QC metrics
were downloaded using `qc_scripts/dl_q7_qc.py`. The data was processed on
FlyWheel by Panos Fotiadis.


## CS-DSI

The CS-DSI scans were collected as part of a pilot study. There are 20 subjects,
each of which has 4 separate CS-DSI sequences. The data were BIDS curated on
FlyWheel and the QSIPrep gear was run using `qc_scripts/csdsi_sep_run.py`.
This script is named this way because `--combine-all-dwis` was not used
so each scan would be processed separately. The


## HBN data

### Legacy dMRIPrep data

These were provided by Ariel Rokem as a download from an S3 bucket. These were
downloaded to `/storage/mcieslak/multishell_qc/hbn_dmriprep` on `dopamine` using
the command `aws s3 sync --exclude '*' --include '*dwi_eddy*' --acl public-read  s3://legacy-hbn-preprocessing .`. The QC scores were calculated using
`qc_scripts/calc_hbn_qc.sh`.


### QSIPrep processing

Valerie Sydnor ran the QSIPrep processing on the FlyWheel version of these subjects. The
script for downloading the qc scores is `qc_scripts/dl_hbn_qc.py` and the script for
downloading the preprocssed dwi and gradients is `qc_scripts/download_preprocd_hbn.py`.


# Statistics and Figures

## Combining data from the many studies

The csvs created from the earlier steps get combined for statistics and plots.
The entrypoint for the csv data into the rest of the modeling is
`qc_scripts/gather_qc_values.rmd`. This script reads the csv's downloaded from
FlyWheel and copied from `dopamine`. The output is `qc_scripts/qc_metrics.csv`.

Next, the subject IDs are anonymized using
`qc_scripts/anonymize_for_github.Rmd`. This loads/merges the smoothness and
qc csvs and anonymizes (via salt and hash) the subject names. The anonymized
data is stored in

  * `qc_scripts/qc_multivolfwhm_spherical.csv` for the shelled schemes
  * `qc_scripts/qc_multivolfwhm_cartesian.csv` for the non-shelled schemes


## Linear mixed effects on QC and FWHM

The QC and FWHM data are used in `qc_scripts/multivolsmoothness_v_qc_stats_lmer.Rmd`
and`qc_scripts/multivolsmoothness_v_qc_stats_cartesian_lmer.Rmd`. These produce the
csv's that are displayed as supplementary tables 2.1-2.4. They also produce the 
FWHM-corrected data that are plotted in Figures 2,3. Their outputs are

 * `qc_scripts/nonspherical_fwhm-corrected_qcs.csv`: the qc values for non-shelled schemes with the effect of FWHM partialled out.
  * `qc_scripts/spherical_fwhm-corrected_qcs.csv`: the qc values for shelled schemes with the effect of FWHM partialled out.
 * `qc_scripts/(cart|sphere)_fwhm_stats.txt`: table of model params for `FWHM ~ pipeline + ( 1 | subject)`
 * `qc_scripts/cart_qc_stats.txt`: table of model params for `QC ~ centered.FWHM + pipeline + ( 1 | subject)`
