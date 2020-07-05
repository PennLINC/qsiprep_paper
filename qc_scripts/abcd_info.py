import flywheel
from glob import glob
import pandas as pd
from io import BytesIO
from tqdm import tqdm
import os.path as op
import os

fw = flywheel.Client()
proj = fw.projects.find_first("label=ABCD")
analyses = fw.get_analyses('projects', proj.id, 'sessions')
qsiprep_results = [ana for ana in analyses if
                   ana.label.startswith("qsiprep_0.3.17_0.8.0")]

def check_outputs(analysis):
    # Safely get a list of files
    analysis_files = analysis.files or []
    # Search for a non-html zip file
    zip_files = [f_obj for f_obj in analysis_files if
                 f_obj.name.endswith('.zip') and
                 not f_obj.name.endswith('.html.zip')]

    # if it succeeded, there will be exactly one results zip
    if not len(zip_files) == 1:
        print("found", len(zip_files), "zip files")
        return 0
    zip_obj = zip_files[0]
    zip_members = analysis.get_file_zip_info(zip_obj.name)['members']
    dwi_files = [f_obj for f_obj in zip_members if '_dwi.nii.gz' in f_obj.path]
    return len(dwi_files)

image_counts = []
for result in tqdm(qsiprep_results):
    subj = fw.get(result.parents.subject)
    image_counts.append({"subject": subji.label, "dwi_files": check_outputs(result)

failed_analyses = []
out_dir = "/storage/mcieslak/multishell_qc/grmpy_qsiprep_outputs"
os.makedirs(out_dir, exist_ok=True)
for result in tqdm(qsiprep_results):
    subj = fw.get(result.parents.subject)
    print(subj.label)
    out_files = glob(out_dir + "/sub-" + subj.label + "*nii.gz")
    if not out_files:
        try:
            download_qc_files(result, out_dir)
        except Exception as e:
            print(e)
            failed_analyses.append(result)

