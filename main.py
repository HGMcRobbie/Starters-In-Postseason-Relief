# Hunter Galusha-McRobbie
# Starters-In-Postseason-Relief
# 18 September 2026 -

# Import Statements
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Initial DataFrame
pitching_df = pd.read_csv("pitching.csv")
pitching_df["date"] = pd.to_datetime(pitching_df["date"].astype(str), format="%Y%m%d")

# DataFrame since 2000
pitching_df["season"] = pitching_df["date"].dt.year
pitching_df_since_2000 = pitching_df[pitching_df["season"] >= 2000]

# Data Cleaning
# print(pitching_df_since_2000.isna().sum())
pitching_df_since_2000[["wp", "lp", "save", "p_gs", "p_gf", "p_cg"]] = \
    (pitching_df_since_2000[["wp", "lp", "save", "p_gs", "p_gf", "p_cg"]].fillna(0))
# print(pitching_df_since_2000.isna().sum())

# Identifying Qualified Starting Pitchers in Each Season
regular_df = pitching_df_since_2000[pitching_df_since_2000["gametype"] == "regular"]



