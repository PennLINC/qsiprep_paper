#!/bin/bash
BASE=/storage/mcieslak/multishell_qc/hbn_dmriprep
mkdir -p ${BASE}/src

for subdir in ${BASE}/*
do
    subject=$(basename $subdir)
    nii=$(ls ${subdir}/dmriprep/dwi_eddy/*.nii*)
    bvec=$(ls ${subdir}/dmriprep/dwi_eddy/*.bvec)
    bval=$(ls ${subdir}/dmriprep/dwi_eddy/*.bval)
    src_file=${BASE}/src/${subject}_dwi.src.gz
    if [ ! -f ${src_file} ]; then
    docker run --rm -t \
        --entrypoint dsi_studio \
	    -v /storage:/storage \
	    pennbbl/qsiprep:0.9.0beta1 \
	    --action=src \
	    --source=$nii \
        --bval=$bval \
        --bvec=$bvec \
        --output=$src_file

    fi

done

docker run --rm -t --entrypoint dsi_studio \
    -v ${BASE}/src:/storage \
    pennbbl/qsiprep:0.9.0beta1 \
    --action=qc \
    --source=/storage






