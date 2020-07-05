import os
import pdb


def create_key(template, outtype=('nii.gz',), annotation_classes=None):
    if template is None or not template:
        raise ValueError('Template must be a valid format string')
    return template, outtype, annotation_classes


# Create Keys
t1w = create_key(
   'sub-{subject}/{session}/anat/sub-{subject}_{session}_T1w')
t2w = create_key(
   'sub-{subject}/{session}/anat/sub-{subject}_{session}_T2w')

# Fmaps
epi_fmap_AP = create_key(
    'sub-{subject}/{session}/fmap/sub-{subject}_{session}_dir-AP_epi')
epi_fmap_PA = create_key(
    'sub-{subject}/{session}/fmap/sub-{subject}_{session}_dir-PA_epi')

# fmri scans
rest_ap_run1 = create_key(
    'sub-{subject}/{session}/func/sub-{subject}_{session}_task-rest_dir-AP_run-01_bold')
rest_ap_run1_sbref = create_key(
    'sub-{subject}/{session}/func/sub-{subject}_{session}_task-rest_dir-AP_run-01_sbref')
rest_pa_run2 = create_key(
    'sub-{subject}/{session}/func/sub-{subject}_{session}_task-rest_dir-PA_run-02_bold')
rest_pa_run2_sbref = create_key(
    'sub-{subject}/{session}/func/sub-{subject}_{session}_task-rest_dir-PA_run-02_sbref')
rest_ap_run3 = create_key(
    'sub-{subject}/{session}/func/sub-{subject}_{session}_task-rest_dir-AP_run-03_bold')
rest_ap_run3_sbref = create_key(
    'sub-{subject}/{session}/func/sub-{subject}_{session}_task-rest_dir-AP_run-03_sbref')
rest_pa_run4 = create_key(
    'sub-{subject}/{session}/func/sub-{subject}_{session}_task-rest_dir-PA_run-04_bold')
rest_pa_run4_sbref = create_key(
    'sub-{subject}/{session}/func/sub-{subject}_{session}_task-rest_dir-PA_run-04_sbref')


dwi_ap_run1 = create_key(
   'sub-{subject}/{session}/dwi/sub-{subject}_{session}_acq-98_dir-AP_run-01_dwi')
dwi_ap_run1_sbref = create_key(
   'sub-{subject}/{session}/dwi/sub-{subject}_{session}_acq-98_dir-AP_run-01_sbref')
dwi_pa_run2 = create_key(
   'sub-{subject}/{session}/dwi/sub-{subject}_{session}_acq-98_dir-PA_run-02_dwi')
dwi_pa_run2_sbref = create_key(
   'sub-{subject}/{session}/dwi/sub-{subject}_{session}_acq-98_dir-PA_run-02_sbref')
dwi_ap_run3 = create_key(
   'sub-{subject}/{session}/dwi/sub-{subject}_{session}_acq-99_dir-AP_run-03_dwi')
dwi_ap_run3_sbref = create_key(
   'sub-{subject}/{session}/dwi/sub-{subject}_{session}_acq-99_dir-AP_run-03_sbref')
dwi_pa_run4 = create_key(
   'sub-{subject}/{session}/dwi/sub-{subject}_{session}_acq-99_dir-PA_run-04_dwi')
dwi_pa_run4_sbref = create_key(
   'sub-{subject}/{session}/dwi/sub-{subject}_{session}_acq-99_dir-PA_run-04_sbref')


def infotodict(seqinfo):
    """Heuristic evaluator for determining which runs belong where

    allowed template fields - follow python string module:

    item: index within category
    subject: participant id
    seqitem: run number during scanning
    subindex: sub index within group
    """

    last_run = len(seqinfo)

    info = {
        t1w: [], t2w: [], epi_fmap_AP: [], epi_fmap_PA: [],

        rest_ap_run1: [], rest_pa_run2: [],
        rest_ap_run3: [], rest_pa_run4: [],
        rest_ap_run1_sbref: [], rest_pa_run2_sbref: [],
        rest_ap_run3_sbref: [], rest_pa_run4_sbref: [],

        dwi_ap_run1: [], dwi_pa_run2: [],
        dwi_ap_run3: [], dwi_pa_run4: [],
        dwi_ap_run1_sbref: [], dwi_pa_run2_sbref: [],
        dwi_ap_run3_sbref: [], dwi_pa_run4_sbref: []
    }

    def get_latest_series(key, s):
    #    if len(info[key]) == 0:
        info[key].append(s.series_id)
    #    else:
    #        info[key] = [s.series_id]

    for s in seqinfo:
        if "abort" in s.protocol_name.lower():
            continue

        if s.protocol_name == 'SpinEchoFieldMap_AP':
            get_latest_series(epi_fmap_AP, s)

        elif s.protocol_name == 'SpinEchoFieldMap_PA':
            get_latest_series(epi_fmap_PA, s)

        elif s.protocol_name == 'rfMRI_REST_AP_Run1':
            if s.dim3 > 1:
                get_latest_series(rest_ap_run1, s)
            else:
                get_latest_series(rest_ap_run1_sbref, s)

        elif s.protocol_name == 'rfMRI_REST_PA_Run2':
            if s.dim3 > 1:
                get_latest_series(rest_pa_run2, s)
            else:
                get_latest_series(rest_pa_run2_sbref, s)

        elif s.protocol_name == 'rfMRI_REST_AP_Run3':
            if s.dim3 > 1:
                get_latest_series(rest_ap_run3, s)
            else:
                get_latest_series(rest_ap_run3_sbref, s)

        elif s.protocol_name == 'rfMRI_REST_PA_Run4':
            if s.dim3 > 1:
                get_latest_series(rest_pa_run4, s)
            else:
                get_latest_series(rest_pa_run4_sbref, s)

        # dMRI naming conventions switch half-way through. Some end with _RunX
        elif s.protocol_name.startswith('dMRI_dir98_AP'):
            if s.dim3 > 1:
                get_latest_series(dwi_ap_run1, s)
            else:
                get_latest_series(dwi_ap_run1_sbref, s)

        elif s.protocol_name.startswith('dMRI_dir98_PA'):
            if s.dim3 > 1:
                get_latest_series(dwi_pa_run2, s)
            else:
                get_latest_series(dwi_pa_run2_sbref, s)

        elif s.protocol_name.startswith('dMRI_dir99_AP'):
            if s.dim3 > 1:
                get_latest_series(dwi_ap_run3, s)
            else:
                get_latest_series(dwi_ap_run3_sbref, s)

        elif s.protocol_name.startswith('dMRI_dir99_PA'):
            if s.dim3 > 1:
                get_latest_series(dwi_pa_run4, s)
            else:
                get_latest_series(dwi_pa_run4_sbref, s)

        elif s.protocol_name == 'T1w_MPR':
            get_latest_series(t1w, s)

        elif s.protocol_name == 'T2w_SPC':
            get_latest_series(t2w, s)

        else:
            print("Series not recognized!: ", s.protocol_name, s.dcm_dir_name)
    return info

IntendedFor = {
    epi_fmap_AP: [
        '{session}/func/sub-{subject}_{session}_task-rest_dir-PA_run-02_bold.nii.gz',
        '{session}/func/sub-{subject}_{session}_task-rest_dir-PA_run-04_bold.nii.gz',
        '{session}/dwi/sub-{subject}_{session}_acq-98_dir-PA_run-02_dwi.nii.gz',
        '{session}/dwi/sub-{subject}_{session}_acq-99_dir-PA_run-04_dwi.nii.gz'
    ],
    epi_fmap_PA: [
        '{session}/func/sub-{subject}_{session}_task-rest_dir-AP_run-01_bold.nii.gz',
        '{session}/func/sub-{subject}_{session}_task-rest_dir-AP_run-03_bold.nii.gz',
        '{session}/dwi/sub-{subject}_{session}_acq-98_dir-AP_run-01_dwi.nii.gz',
        '{session}/dwi/sub-{subject}_{session}_acq-99_dir-AP_run-03_dwi.nii.gz'
    ]
}

def ReplaceSubject(label):
    return label.lstrip("TOME_")

def ReplaceSession(label):
    # These are all session 1
    return "1"
