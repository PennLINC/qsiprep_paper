import flywheel
import datetime
import pandas as pd
from tqdm import tqdm
now = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M")
fw = flywheel.Client()
qsiprep = fw.lookup('gears/qsiprep-fw')
proj = fw.projects.find_first("label=ABCD")
analysis_label = 'qsiprep_{}_{}'.format(qsiprep.gear.version, now)

inputs = {
    "freesurfer_license": proj.files[0]
}

config = {
    'output_resolution': 1.7,
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

with open("joint_abcd_subjects.txt") as f:
    subjects_to_run = [line.strip() for line in f]

fails = []
for ses in sessions:
    if ses.subject.label not in subjects_to_run:
        continue

    try:
        _id = qsiprep.run(analysis_label=analysis_label,
                          config=config, inputs=inputs, destination=ses)
        analysis_ids.append(_id)
    except Exception as e:
        print(e)
        fails.append(ses)


with open(analysis_label+"_jobs.txt", "w") as jobsfile:
    jobsfile.write("\n".join(analysis_ids))


# Figure out which scanner each was run on and add this to a csv
scanner_info = []
missing_t1 = []
for ses in tqdm(sessions):
    if ses.subject.label not in subjects_to_run:
        continue
    acqs = ses.acquisitions()
    if not acqs:
        continue
    t1ws = [acq for acq in acqs if acq.label.lower() == "t1w"]
    if not t1ws:
        missing_t1.append(ses)
        continue
    t1w = t1ws[0]
    if not len(t1w.files):
        missing_t1.append(ses)
        continue
    t1w_image = t1w.files[0]
    details = fw.get_acquisition_file_info(t1w.id, t1w.files[0].name).info
    scanner_info.append(
        {
            "subject": ses.subject.label,
            "manufacturer": details.get("Manufacturer"),
            "software": details.get("SoftwareVersions"),
            "scanner": details.get("ManufacturersModelName")
        }
    )
scanner_df = pd.DataFrame(scanner_info)
scanner_df.to_csv("abcd_scanner_info.csv", index=False)
