import flywheel
import datetime

now = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M")
fw = flywheel.Client()
qsiprep = fw.lookup('gears/qsiprep-fw-hpc')
proj = fw.projects.find_first("label=Glymphatic")


inputs = {
    "freesurfer_license": proj.files[4]
}

analysis_ids = []
fails = []
for ses in proj.sessions():

    try:
        config = {
            "hmc_model": "eddy",
            "use_syn_sdc": False,
            'save_outputs': True,
            'dwi_denoise_window': 5,
            'do_reconall': False,
            'b0_to_t1w_transform': 'Rigid',
            'combine_all_dwis': False,
            'unringing_method': 'mrdegibbs',
            'force_spatial_normalization': True,
            'intramodal_template_iters': 2,
            'intramodal_template_transform': 'BSplineSyN',
            'output_resolution': 3.0,
            'shoreline_iters': 0,
            'b0_threshold': 100,
            'output_space': 'T1w',
            'sloppy': False
        }
        _id = qsiprep.run(analysis_label='qsiprep_0.8.0_3_{}_{}'.format(ses.label, now),
                          config=config, inputs=inputs, destination=ses)
        analysis_ids.append(_id)
    except Exception as e:
        print(e)
        fails.append(ses)
