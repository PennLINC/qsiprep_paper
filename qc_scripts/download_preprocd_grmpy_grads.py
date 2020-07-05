import flywheel
from glob import glob
import pandas as pd
from io import BytesIO
from tqdm import tqdm
import os.path as op
import os

fw = flywheel.Client()
proj = fw.projects.find_first("label=GRMPY_822831")
analyses = fw.get_analyses('projects', proj.id, 'sessions')
qsiprep_results = [ana for ana in analyses if
                   ana.label.startswith("qsiprep_0.3.17_0.8.0")]

def download_qc_files(analysis, output_dir):
    # Safely get a list of files
    analysis_files = analysis.files or []
    # Search for a non-html zip file
    zip_files = [f_obj for f_obj in analysis_files if
                 f_obj.name.endswith('.zip') and
                 not f_obj.name.endswith('.html.zip')]

    # if it succeeded, there will be exactly one results zip
    if not len(zip_files) == 1:
        print("found", len(zip_files), "zip files")
        return False
    zip_obj = zip_files[0]
    zip_members = analysis.get_file_zip_info(zip_obj.name)['members']
    confounds_files = [f_obj for f_obj in zip_members if '.bval' in f_obj.path
                       or '.bvec' in f_obj.path]

    # We need both files
    if not confounds_files:
        return False
    # check if the output already exists
    for confound_file in confounds_files:
        confounds_file = confound_file.path
        downloaded_confounds_file = output_dir + "/" + op.split(confounds_file)[1]
        if not op.exists(downloaded_confounds_file):
            print("downloading", downloaded_confounds_file)
            analysis.download_file_zip_member(zip_obj.name,
                                              confounds_file,
                                              downloaded_confounds_file)
        else:
            print("found", downloaded_confounds_file)

    return True


failed_analyses = []
out_dir = "/storage/mcieslak/multishell_qc/grmpy_qsiprep_outputs"
os.makedirs(out_dir, exist_ok=True)
for result in tqdm(qsiprep_results):
    try:
        download_qc_files(result, out_dir)
    except Exception as e:
        print(e)
        failed_analyses.append(result)

