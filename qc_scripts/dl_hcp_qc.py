import pandas as pd
from glob import glob
glymphatic_files = glob("hcp_tsvs/*ImageQC*csv")

dfs = [pd.read_csv(fname) for fname in glymphatic_files]
glymphatic_df = pd.concat(dfs, axis=0)
glymphatic_df.to_csv("hcp_qsiprep_qc.csv", index=False)
