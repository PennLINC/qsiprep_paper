#!/bin/bash
#cd /storage/mcieslak/ndar_minimal/abcdtestdmri/fmriresults01
BASE=/storage/mcieslak/ndar_minimal/abcdtestdmri/fmriresults01
outd=/storage/mcieslak/multishell_qc/abcd_src

while read subject
do
    niis=$(ls ${BASE}/bids/${subject}/ses-baselineYear1Arm1/dwi/${subject}_ses-baselineYear1Arm1_run-*_dwi.nii* | sort) 
    bvals=$(ls ${BASE}/bids/${subject}/ses-baselineYear1Arm1/dwi/${subject}_ses-baselineYear1Arm1_run-*_dwi.bval | sort) 
    bvecs=$(ls ${BASE}/bids/${subject}/ses-baselineYear1Arm1/dwi/${subject}_ses-baselineYear1Arm1_run-*_dwi.bvec | sort) 
    num_niis=$(echo ${niis} | wc -w )
    merged_mif=${BASE}/bids/${subject}/ses-baselineYear1Arm1/dwi/${subject}_ses-baselineYear1Arm1_dwi.mif
    merged_nii=${BASE}/bids/${subject}/ses-baselineYear1Arm1/dwi/${subject}_ses-baselineYear1Arm1_desc-merged_dwi.nii.gz


    mifs=
    for nii_file in ${niis}
    do
	    mif=${nii_file/nii/mif}
	    bval=${nii_file/nii/bval}
	    bvec=${nii_file/nii/bvec}
	    mrconvert -force -fslgrad ${bvec} ${bval} ${nii_file} ${mif}
	    mifs="${mifs} ${mif}"
    done

    if [ $num_niis -gt 1 ]; then
        echo merging $mifs
        mrcat -force $mifs $merged_mif
    else
	merged_mif=$mifs
    fi
    
    new_bval=${BASE}/bids/${subject}/ses-baselineYear1Arm1/dwi/${subject}_ses-baselineYear1Arm1_desc-merged_dwi.bval
    new_bvec=${BASE}/bids/${subject}/ses-baselineYear1Arm1/dwi/${subject}_ses-baselineYear1Arm1_desc_merged_dwi.bvec
    mrinfo -force -export_grad_fsl $new_bvec $new_bval $merged_mif
    mrconvert -force $merged_mif $merged_nii

    src_file=${outd}/${subject}_ses-baselineYear1Arm1_desc-merged_dwi.src.gz
    docker run --rm -t \
        --entrypoint dsi_studio \
	-v /storage:/storage \
	pennbbl/qsiprep:0.8.0 \
	--action=src \
	--source=$merged_nii \
	--bval=$new_bval \
	--bvec=$new_bvec \
	--output=$src_file

done < joint_abcd_subjects.txt

docker run --rm -t --entrypoint dsi_studio \
    -v ${outd}:/storage \
    pennbbl/qsiprep:0.8.0 \
    --action=qc \
    --source=/storage






