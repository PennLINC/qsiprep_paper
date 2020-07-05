import flywheel
import datetime
import csv
from pathlib import Path
import random

now = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M")
fw = flywheel.Client()
qsiprep = fw.lookup('gears/qsiprep-fw')
proj = fw.projects.find_first("label=GRMPY_822831")
analysis_label = 'qsiprep_{}_{}'.format(qsiprep.gear.version, now)

inputs = {
    "freesurfer_license": proj.files[3]
}

config = {
    'output_resolution': 1.5,
    'dwi_denoise_window': 5,
    'do_reconall': False,
    'shoreline_iters': 0,
    'intramodal_template_iters': 0,
    'b0_threshold': 100,
    'hmc_model': 'eddy',
    'save_outputs': True,
    'unringing_method': 'mrdegibbs',
    'combine_all_dwis': False,
    'denoise_before_combining': True,
    'output_space': 'T1w',
    'sloppy': False,
    'force_spatial_normalization': True
}

analysis_ids = []
sessions = proj.sessions()

fails = []
for ses in sessions:
    try:
        _id = qsiprep.run(analysis_label=analysis_label,
                          config=config, inputs=inputs, destination=ses)
        analysis_ids.append(_id)
    except Exception as e:
        print(e)
        fails.append(ses)


with open(analysis_label+"_jobs.txt", "w") as jobsfile:
    jobsfile.write("\n".join(analysis_ids))
