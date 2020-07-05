import flywheel
from glob import glob
import pandas as pd
from io import BytesIO
from tqdm import tqdm
import os.path as op
import os

fw = flywheel.Client()
proj = fw.projects.find_first("label=tome")
analyses = fw.get_analyses('projects', proj.id, 'sessions')
hcp_results = [ana for ana in analyses if
                   ana.label.startswith("hcp-diff v0.1.5")]

def download_qc_files(analysis, output_dir):
    # Safely get a list of files
    analysis_files = analysis.files or []
    # Search for a non-html zip file
    zip_files = [f_obj for f_obj in analysis_files if
                 f_obj.name.endswith('hcpdiff.zip')]
    subject_label = fw.get(analysis.parents.subject).label[5:]
    # if it succeeded, there will be exactly one results zip
    if not len(zip_files) == 1:
        print("found", len(zip_files), "zip files")
        return False
    zip_obj = zip_files[0]
    zip_members = analysis.get_file_zip_info(zip_obj.name)['members']
    to_download = [
        ('TOME_%s/T1w/All_DTI_acqs/nodif_brain_mask.nii.gz' % subject_label,
         'sub-%s_ses-1_desc-brain_mask.nii.gz' % subject_label),
        ('TOME_%s/T1w/All_DTI_acqs/data.nii.gz' % subject_label,
         'sub-%s_ses-1_dwi.nii.gz' % subject_label),
        ('TOME_%s/T1w/All_DTI_acqs/bvals' % subject_label,
         'sub-%s_ses-1_dwi.bval' % subject_label),
        ('TOME_%s/T1w/All_DTI_acqs/bvecs' % subject_label,
         'sub-%s_ses-1_dwi.bvec' % subject_label),
    ]

    # check if the output already exists
    for fw_file, local_file in to_download:
        downloaded_file = output_dir + "/" + local_file
        if not op.exists(downloaded_file):
            print("downloading", downloaded_file)
            analysis.download_file_zip_member(zip_obj.name,
                                              fw_file,
                                              downloaded_file)
        else:
            print("found", downloaded_file)

    return True


failed_analyses = []
out_dir = "/storage/mcieslak/multishell_qc/hcp_preprocd"
os.makedirs(out_dir, exist_ok=True)
for result in tqdm(hcp_results[-2:]):
    subj = fw.get(result.parents.subject)
    print(subj.label)
    out_files = glob(out_dir + "/" + subj.label + "*nii.gz")
    if not out_files:
        try:
            download_qc_files(result, out_dir)
        except Exception as e:
            print(e)
            failed_analyses.append(result)

