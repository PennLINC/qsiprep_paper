#!/bin/bash


###### HCP #########
SMOOTHCSV=/storage/mcieslak/multishell_qc/hcp_smoothness_vals.csv
# echo "subject,hcp_fwhm,qsiprep_fwhm" > $SMOOTHCSV
HCPBASE=/storage/mcieslak/multishell_qc/hcp_preprocd
BASE=/storage/mcieslak/multishell_qc/tome_output/qsiprep
smoothd=/storage/mcieslak/multishell_qc/smoothness/hcp
mkdir -p $smoothd

while read subject
do
    # The QSIPrep data
    sub_base=${BASE}/sub-${subject}/ses-1/dwi/sub-${subject}_ses-1
    nii=${sub_base}_space-T1w_desc-preproc_dwi.nii.gz
    bval=${sub_base}_space-T1w_desc-preproc_dwi.bval
    bvec=${sub_base}_space-T1w_desc-preproc_dwi.bvec
    smoothed=${smoothd}/sub-${subject}_space-T1w_desc-preprocblurto_dwi.nii.gz
    smoothedsrc=${outd}/sub-${subject}_ses-1_space-T1w_desc-preprocblurto_dwi.src.gz
    #dwiextract -fslgrad ${bvec} ${bval} ${nii} -bzero - | mrmath - mean $qb0 -axis 3

    # The NDAR data
    hcp_nii=${HCPBASE}/sub-${subject}_ses-1_dwi.nii.gz 
    hcp_bval=${HCPBASE}/sub-${subject}_ses-1_dwi.bval
    hcp_bvec=${HCPBASE}/sub-${subject}_ses-1_dwi.bvec
    hb0=${smoothd}/sub-${subject}_desc-hcp_b0ref.nii.gz

    #dwiextract -fslgrad ${hcp_bvec} ${hcp_bval} ${hcp_nii} -bzero - | mrmath - mean $hb0 -axis 3
    #hcp_fwhm=$(3dFWHMx -automask -input ${hb0} | sed 's/  */ /g' )
    #wanted_fwhm=$(python /storage/mcieslak/multishell_qc/get_fwhm.py ${hcp_fwhm})

    #qp_fwhm=$(3dFWHMx -automask -input ${qb0} | sed 's/  */ /g' )
    #qp_fwhm1=$(python /storage/mcieslak/multishell_qc/get_fwhm.py ${qp_fwhm})

    #echo ${subject},${wanted_fwhm},${qp_fwhm1} >> $SMOOTHCSV

done < tome_subjects.txt



###### PNC #########
SMOOTHCSV=/storage/mcieslak/multishell_qc/pnc_smoothness_vals.csv
echo "subject,other_fwhm,qsiprep_fwhm" > $SMOOTHCSV
HCPBASE=/storage/mcieslak/multishell_qc/pnc_preprocd
BASE=/storage/mcieslak/multishell_qc/pnc_qsiprep_outputs
smoothd=/storage/mcieslak/multishell_qc/smoothness/roalf
mkdir -p $smoothd

while read subject
do
    # The QSIPrep data
    sub_base=${BASE}/sub-${subject}_ses-PNC1
    nii=${sub_base}_space-T1w_desc-preproc_dwi.nii.gz
    bval=${sub_base}_space-T1w_desc-preproc_dwi.bval
    bvec=${sub_base}_space-T1w_desc-preproc_dwi.bvec
    qb0=${smoothd}/sub-${subject}_desc-qsiprep_b0ref.nii.gz
    if [ ! -f ${qb0} ]; then
        dwiextract -fslgrad ${bvec} ${bval} ${nii} -bzero - | mrmath - mean $qb0 -axis 3
    fi

    # The NDAR data
    hcp_nii=${HCPBASE}/${subject}_roalf.nii.gz 
    hcp_bval=${HCPBASE}/${subject}_roalf.bval
    hcp_bvec=${HCPBASE}/${subject}_roalf.bvec
    hb0=${smoothd}/sub-${subject}_desc-roalf_b0ref.nii.gz
    if [ ! -f ${hb0} ]; then
        dwiextract -fslgrad ${hcp_bvec} ${hcp_bval} ${hcp_nii} -bzero - | mrmath - mean $hb0 -axis 3
    fi

    hcp_fwhm=$(3dFWHMx -automask -input ${hb0} | sed 's/  */ /g' )
    hcp_fwhm1=$(python /storage/mcieslak/multishell_qc/get_fwhm.py ${hcp_fwhm})

    qp_fwhm=$(3dFWHMx -automask -input ${qb0} | sed 's/  */ /g' )
    qp_fwhm1=$(python /storage/mcieslak/multishell_qc/get_fwhm.py ${qp_fwhm})

    echo ${subject},${hcp_fwhm1},${qp_fwhm1} >> $SMOOTHCSV

done < pnc_subjects.csv



###### grmpy #########
SMOOTHCSV=/storage/mcieslak/multishell_qc/grmpy_smoothness_vals.csv
echo "subject,other_fwhm,qsiprep_fwhm" > $SMOOTHCSV
HCPBASE=/storage/mcieslak/multishell_qc/grmpy_preprocd
BASE=/storage/mcieslak/multishell_qc/grmpy_qsiprep_outputs
smoothd=/storage/mcieslak/multishell_qc/smoothness/pines
mkdir -p $smoothd

while read subject
do
    # The QSIPrep data
    sub_base=${BASE}/sub-${subject}_ses-
    nii=${sub_base}*_desc-preproc_dwi.nii*
    bval=${sub_base}*_space-T1w_desc-preproc_dwi.bval
    bvec=${sub_base}*_space-T1w_desc-preproc_dwi.bvec
    qb0=${smoothd}/sub-${subject}_desc-qsiprep_b0ref.nii.gz
    if [ ! -f $qb0 ]; then
        dwiextract -fslgrad ${bvec} ${bval} ${nii} -bzero - | mrmath - mean $qb0 -axis 3
    fi

    # The NDAR data
    hcp_nii=${HCPBASE}/${subject}_pines.nii.gz 
    hcp_bval=${HCPBASE}/${subject}_pines.bval
    hcp_bvec=${HCPBASE}/${subject}_pines.bvec
    hb0=${smoothd}/sub-${subject}_desc-pines_b0ref.nii.gz
    if [ ! -f $hb0 ]; then
        dwiextract -fslgrad ${hcp_bvec} ${hcp_bval} ${hcp_nii} -bzero - | mrmath - mean $hb0 -axis 3
    fi

    hcp_fwhm=$(3dFWHMx -automask -input ${hb0} | sed 's/  */ /g' )
    hcp_fwhm1=$(python /storage/mcieslak/multishell_qc/get_fwhm.py ${hcp_fwhm})

    qp_fwhm=$(3dFWHMx -automask -input ${qb0} | sed 's/  */ /g' )
    qp_fwhm1=$(python /storage/mcieslak/multishell_qc/get_fwhm.py ${qp_fwhm})

    echo ${subject},${hcp_fwhm1},${qp_fwhm1} >> $SMOOTHCSV

done < grmpy_subjects.txt



###### ABCD #########
SMOOTHCSV=/storage/mcieslak/multishell_qc/abcd_smoothness_vals.csv
echo "subject,other_fwhm,qsiprep_fwhm" > $SMOOTHCSV
HCPBASE=/storage/mcieslak/ndar_minimal/abcdtestdmri/fmriresults01
BASE=/storage/mcieslak/multishell_qc/abcd_qsiprep_outputs
smoothd=/storage/mcieslak/multishell_qc/smoothness/abcd
mkdir -p $smoothd

while read subject
do
    # The QSIPrep data
    sub_base=${BASE}/${subject}_ses-baselineYear1Arm1_space-T1w_desc-preproc_dwi
    nii=${sub_base}.nii.gz
    bval=${sub_base}.bval
    bvec=${sub_base}.bvec
    qb0=${smoothd}/${subject}_desc-qsiprep_b0ref.nii.gz
    if [ ! -f $qb0 ]; then
        dwiextract -fslgrad ${bvec} ${bval} ${nii} -bzero - | mrmath - mean $qb0 -axis 3
    fi

    # The NDAR data can be spread across multiple scans
    niis=$(ls ${HCPBASE}/bids/${subject}/ses-baselineYear1Arm1/dwi/${subject}_ses-baselineYear1Arm1_run-*_dwi.nii* | sort) 
    bvals=$(ls ${HCPBASE}/bids/${subject}/ses-baselineYear1Arm1/dwi/${subject}_ses-baselineYear1Arm1_run-*_dwi.bval | sort) 
    bvecs=$(ls ${HCPBASE}/bids/${subject}/ses-baselineYear1Arm1/dwi/${subject}_ses-baselineYear1Arm1_run-*_dwi.bvec | sort) 
    num_niis=$(echo ${niis} | wc -w )
    merged_mif=${HCPBASE}/bids/${subject}/ses-baselineYear1Arm1/dwi/${subject}_ses-baselineYear1Arm1_dwi.mif
    merged_nii=${HCPBASE}/bids/${subject}/ses-baselineYear1Arm1/dwi/${subject}_ses-baselineYear1Arm1_desc-merged_dwi.nii.gz


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
    hb0=${smoothd}/sub-${subject}_desc-mmps_b0ref.nii.gz

    dwiextract -fslgrad ${new_bvec} ${new_bval} ${merged_nii} -bzero - | mrmath - mean $hb0 -axis 3
    hcp_fwhm=$(3dFWHMx -automask -input ${hb0} | sed 's/  */ /g' )
    hcp_fwhm1=$(python /storage/mcieslak/multishell_qc/get_fwhm.py ${hcp_fwhm})

    qp_fwhm=$(3dFWHMx -automask -input ${qb0} | sed 's/  */ /g' )
    qp_fwhm1=$(python /storage/mcieslak/multishell_qc/get_fwhm.py ${qp_fwhm})

    echo ${subject},${hcp_fwhm1},${qp_fwhm1} >> $SMOOTHCSV

done < joint_abcd_subjects.txt
