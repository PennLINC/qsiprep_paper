import flywheel

"""
Check to see which subjects are available in our Flywheel instance
to compare to the downloaded minimally preprocessed images
"""
fw = flywheel.Client()
qsiprep = fw.lookup('gears/qsiprep-fw')
proj = fw.projects.find_first("label=ABCD")
with open("abcd_subjects.txt") as sublist:
    ndar_subjects = ["sub-" + line.strip() for line in sublist]
fw_subjects = [sub.label for sub in proj.subjects()]

in_both = set(fw_subjects).intersection(set(ndar_subjects))

with open("joint_abcd_subjects.txt", "w") as f:
    f.write("\n".join(in_both))
