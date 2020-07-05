#!/bin/bash
BASE=/storage/mcieslak/multishell_qc
mkdir -p ${BASE}

qsiprep-docker \
    --image pennbbl/qsiprep:0.9.0beta1 \
    --gpus all \
    ${BASE}/tome ${BASE}/tome_output participant \
    --hmc-model eddy \
    -w ${BASE}/tome_work \
    --nthreads 8 \
    --combine-all-dwis \
    --eddy-config eddy_params.json \
    --distortion-group-merge average \
    --denoise-before-combining \
    --output-resolution 1.5 \
    --fs-license-file /opt/freesurfer/license.txt
