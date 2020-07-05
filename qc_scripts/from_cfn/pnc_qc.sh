#!/bin/bash
SIMG=/data/jux/BBL/projects/csdsi/qsiprep080.simg
OUT=/data/jux/BBL/projects/csdsi/pnc_srcs

singularity exec -B $OUT:/sngl/out \
    $SIMG \
    dsi_studio --action=qc \
    --source=/sngl/out
