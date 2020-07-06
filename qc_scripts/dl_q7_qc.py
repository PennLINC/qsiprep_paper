import flywheel
import pandas as pd
from io import BytesIO
from tqdm import tqdm
import os.path as op
import os

fw = flywheel.Client()
proj = fw.projects.find_first("label=Q7DSI")
analyses = fw.get_analyses('projects', proj.id, 'sessions')
qsiprep_results = [ana for ana in analyses if
                   ana.label.startswith("DSI_Preproc_qsiprep-fw-hpc_0.3.17_0.8.0_2020-04-08_12:38")]

def download_qc_files(analysis, output_dir):
    # Safely get a list of files
    analysis_files = analysis.files or []
    # Search for a non-html zip file
    zip_files = [f_obj for f_obj in analysis_files if
                 f_obj.name.endswith('.zip') and
                 not f_obj.name.endswith('.html.zip')]

    # if it succeeded, there will be exactly one results zip
    if not len(zip_files) == 1:
        return False
    zip_obj = zip_files[0]
    zip_members = analysis.get_file_zip_info(zip_obj.name)['members']
    confounds_files = [f_obj for f_obj in zip_members if 'confounds.tsv' in f_obj.path]
    qc_files = [f_obj for f_obj in zip_members if 'ImageQC' in f_obj.path]
    # We need both files
    if not confounds_files and qc_files:
        return False
    # check if the output already exists
    for confound_file in confounds_files:
        confounds_file = confound_file.path
        downloaded_confounds_file = output_dir + "/" + op.split(confounds_file)[1]
        if not op.exists(downloaded_confounds_file):
            analysis.download_file_zip_member(zip_obj.name,
                                              confounds_file,
                                              downloaded_confounds_file)

    for qc_file in qc_files:
        qc_file_path = qc_file.path
        downloaded_qc_file = output_dir + "/" + op.split(qc_file_path)[1]
        if not op.exists(downloaded_qc_file):
            analysis.download_file_zip_member(zip_obj.name,
                                              qc_file_path,
                                              downloaded_qc_file)
    return True

failed_analyses = []
out_dir = "/Users/mcieslak/projects/writing/qsiprep_paper/qc_scripts/q7_tsvs"
os.makedirs(out_dir, exist_ok=True)
for result in tqdm(qsiprep_results):
    if not download_qc_files(result, out_dir):
        failed_analyses.append(result)

from glob import glob
glymphatic_files = glob(out_dir + "/*ImageQC*csv")

dfs = [pd.read_csv(fname) for fname in glymphatic_files]
glymphatic_df = pd.concat(dfs, axis=0)
glymphatic_df.to_csv("q7_qc.csv", index=False)
