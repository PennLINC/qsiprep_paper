import flywheel
import datetime
import pandas as pd
from tqdm import tqdm
now = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M")
fw = flywheel.Client()
proj = fw.projects.find_first("label=tome")
analyses = fw.get_analyses('projects', proj.id, 'sessions')
hcp_results = [ana for ana in analyses if
               ana.label.startswith("hcp-diff v0.1.5")]
fwheudiconv = fw.lookup('gears/fw-heudiconv')
analysis_label = 'fw-heudiconv_{}_{}'.format(fwheudiconv.gear.version, now)

inputs = {
    "heuristic": proj.files[19]
}

config = {
    'action': 'Curate',
    'do_whole_project': False,
    'dry_run': False
}

analysis_ids = []
fails = []
for hcp_result in hcp_results:
    ses = fw.get(hcp_result.parent.id)
    try:
        _id = fwheudiconv.run(analysis_label=analysis_label,
                              config=config, inputs=inputs, destination=ses)
        analysis_ids.append(_id)
    except Exception as e:
        print(e)
        fails.append(ses)
