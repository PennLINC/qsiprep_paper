#!/bin/bash
#cd /storage/mcieslak/ndar_minimal/abcdtestdmri/fmriresults01
BASE=/storage/mcieslak/multishell_qc/hcp_preprocd

for nii in ${BASE}/*_dwi.nii.gz
do
    subject=$(echo $nii | cut -d '/' -f 6 | cut -d '_' -f 1 | cut -d '-' -f 2)
    bval=$(ls ${BASE}/sub-${subject}_*bval)
    bvec=$(ls ${BASE}/sub-${subject}_*bvec)

    src_file=${BASE}/sub-${subject}_ses-1_dwi.src.gz
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
    -v ${BASE}:/storage \
    pennbbl/qsiprep:0.9.0beta1 \
    --action=qc \
    --source=/storage






