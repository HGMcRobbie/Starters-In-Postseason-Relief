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
pitching_df_since_2000 = pitching_df[(pitching_df["season"] >= 2000) & (pitching_df["season"] <= 2025)]

# Data Cleaning
# print(pitching_df_since_2000.isna().sum())
pitching_df_since_2000[["wp", "lp", "save", "p_gs", "p_gf", "p_cg"]] = \
    (pitching_df_since_2000[["wp", "lp", "save", "p_gs", "p_gf", "p_cg"]].fillna(0))
# print(pitching_df_since_2000.isna().sum())

# Identifying Qualified Starting Pitchers in Each Season
regular_df = pitching_df_since_2000[pitching_df_since_2000["gametype"] == "regular"]
starters_df = regular_df.groupby(["id", "season"]).agg(
    starts = ("p_gs", "sum"),
    outs = ("p_ipouts", "sum")
).reset_index()
qualified_starters_df = starters_df[(starters_df["starts"] >= 20) & (starters_df["outs"] >= 486)]
# print(qualified_starters_df)

# Identifying Instances where these Starters pitched in relief in the postseason
# print(pitching_df_since_2000["gametype"].value_counts())
playoff_game_types = ["divisionseries", "lcs", "worldseries", "wildcard", "playoff"] # playoff corresponds to game 163s,
# which we will include as those are strategically more similar to playoff games than regular season games
postseason_df = pitching_df_since_2000[pitching_df_since_2000["gametype"].isin(playoff_game_types)]
# print(postseason_df)
# Combining the starters who pitched in relief in the postseason into one dataframe
starters_in_relief_appearances = []
for index, appearance in postseason_df.iterrows():
    if appearance["p_seq"] > 1:
        matching_starter = qualified_starters_df[
            (qualified_starters_df["id"] == appearance["id"]) &
            (qualified_starters_df["season"] == appearance["season"])
        ]
        if len(matching_starter) > 0:
            starters_in_relief_appearances.append(appearance)
# print(len(starters_in_relief_appearances))

# Convert list into DataFrame
starters_in_relief_df = pd.DataFrame(starters_in_relief_appearances).reset_index(drop=True)
# print(starters_in_relief_df)

# Research Questions

# Which pitchers do it most?
appearances_by_pitcher = (starters_in_relief_df["id"].value_counts())
# print(appearances_by_pitcher[appearances_by_pitcher > 6])

# How many of these guys started a game in that same series or in that same playoffs?


# Has this become more or less common over time?
count_by_season = (starters_in_relief_df.groupby("season")["id"].count())
# print(count_by_season)

# Determining ERA, WHIP, and other basic stats for the starters in relief appearances
starters_in_relief_outs = starters_in_relief_df["p_ipouts"].sum()
starters_in_relief_earned_runs = starters_in_relief_df["p_er"].sum()
starters_in_relief_hits = starters_in_relief_df["p_h"].sum()
starters_in_relief_walks = starters_in_relief_df["p_w"].sum()

starters_in_relief_era = (starters_in_relief_earned_runs * 27) / starters_in_relief_outs
starters_in_relief_whip = ( (starters_in_relief_hits + starters_in_relief_walks) * 3) / starters_in_relief_outs

# print(round(starters_in_relief_era, 2)) # >>> 4.05
# print(round(starters_in_relief_whip, 2)) # >>> 1.35


