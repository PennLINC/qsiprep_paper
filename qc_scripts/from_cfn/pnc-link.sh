#!/bin/bash
DATA=/data/joy/BBL/studies/pnc/processedData/diffusion/pncDTI_2016_04/
SIMG=/data/jux/BBL/projects/csdsi/qsiprep080.simg
OUT=/data/jux/BBL/projects/csdsi/pnc_srcs
NPREFIX=$(echo $DATA | wc -c)
mkdir -p pnc_preprocd
while read subject
do
    nii=`ls $DATA/$subject/*/DTI_64/dico_corrected/*_dico_dico.nii.gz | head -n 1`
    ln -s ${nii} pnc_preprocd/${subject}_roalf.nii.gz
done < pnc_subjects.csv
