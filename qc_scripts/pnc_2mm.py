import flywheel
import datetime
import csv
from pathlib import Path
import random

now = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M")
fw = flywheel.Client()
qsiprep = fw.lookup('gears/qsiprep-fw-hpc')
proj = fw.projects.find_first("label=PNC_CS_810336")
analysis_label = 'test_hpc_{}_{}'.format(qsiprep.gear.version, now)

inputs = {
    "freesurfer_license": proj.files[5]
}

config = {
    'output_resolution': 2.0,
    'dwi_denoise_window': 5,
    'do_reconall': False,
    'shoreline_iters': 0,
    'intramodal_template_iters': 0,
    'b0_threshold': 100,
    'hmc_model': 'eddy',
    'save_outputs': True,
    'unringing_method': 'mrdegibbs',
    'combine_all_dwis': True,
    'denoise_before_combining': True,
    'output_space': 'T1w',
    'sloppy': False,
    'force_spatial_normalization': True
}

analysis_ids = []
sessions = proj.sessions()

test_sessions = random.sample(sessions, k=125)
fails = []
for ses in test_sessions:
    try:
        _id = qsiprep.run(analysis_label=analysis_label,
                          config=config, inputs=inputs, destination=ses)
        analysis_ids.append(_id)
    except Exception as e:
        print(e)
        fails.append(ses)
    break

with open(analysis_label+"2mm_jobs.txt", "w") as jobsfile:
    jobsfile.write("\n".join(analysis_ids))
