#!/bin/bash
DATA=/data/jux/BBL/projects/multishell_diffusion/processedData/multishellPipelineFall2017
NIIS=$DATA/*/*/prestats/eddy/*_eddied_sls.nii.gz
mkdir -p grmpy_preprocd
for fname in ${NIIS}
do
    subject=`echo $fname | cut -d "/" -f 9`
    ln -s ${fname} $PWD/grmpy_preprocd/${subject}_pines.nii.gz
done

