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

# DataFrame since 2000, excluding 2020
pitching_df["season"] = pitching_df["date"].dt.year
pitching_df_since_2000 = pitching_df[(pitching_df["season"] >= 2000) & (pitching_df["season"] <= 2025) & (pitching_df["season"] != 2020)]

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
# Combining the qualified starters and all other pitchers who appeared in relief into separate dataframes
qualified_starters_in_relief_appearances = []
all_others_in_relief_appearances = []

for index, appearance in postseason_df.iterrows():
    if appearance["p_seq"] > 1:
        matching_starter = qualified_starters_df[
            (qualified_starters_df["id"] == appearance["id"]) &
            (qualified_starters_df["season"] == appearance["season"])
        ]
        if len(matching_starter) > 0:
            qualified_starters_in_relief_appearances.append(appearance)
        else:
            all_others_in_relief_appearances.append(appearance)
# print(len(qualified_starters_in_relief_appearances))
# print(len(all_others_in_relief_appearances))

# Convert lists into DataFrames
qualified_starters_in_relief_df = pd.DataFrame(qualified_starters_in_relief_appearances).reset_index(drop=True)
all_others_in_relief_df = pd.DataFrame(all_others_in_relief_appearances).reset_index(drop=True)
# print(qualified_starters_in_relief_df)
# print(all_others_in_relief_df)

# Research Questions

# Which pitchers do it most?
appearances_by_pitcher = (qualified_starters_in_relief_df["id"].value_counts())
# print(appearances_by_pitcher[appearances_by_pitcher > 6])

# How many of these guys started a game in that same series or in that same playoffs?


# Has this become more or less common over time?
count_by_season = (qualified_starters_in_relief_df.groupby("season")["id"].count())
# print(count_by_season)

# Determining ERA and WHIP for the qualified starters in relief
qualified_starters_in_relief_outs = qualified_starters_in_relief_df["p_ipouts"].sum()
qualified_starters_in_relief_earned_runs = qualified_starters_in_relief_df["p_er"].sum()
qualified_starters_in_relief_hits = qualified_starters_in_relief_df["p_h"].sum()
qualified_starters_in_relief_walks = qualified_starters_in_relief_df["p_w"].sum()

qualified_starters_in_relief_era = (qualified_starters_in_relief_earned_runs * 27) / qualified_starters_in_relief_outs
qualified_starters_in_relief_whip = ((qualified_starters_in_relief_hits + qualified_starters_in_relief_walks) * 3) / qualified_starters_in_relief_outs

# print(round(qualified_starters_in_relief_era, 2)) # >>> 4.05
# print(round(qualified_starters_in_relief_whip, 2)) # >>> 1.35

# Determining ERA and WHIP for all others in relief
all_others_in_relief_outs = all_others_in_relief_df["p_ipouts"].sum()
all_others_in_relief_earned_runs = all_others_in_relief_df["p_er"].sum()
all_others_in_relief_hits = all_others_in_relief_df["p_h"].sum()
all_others_in_relief_walks = all_others_in_relief_df["p_w"].sum()

all_others_in_relief_era = (all_others_in_relief_earned_runs * 27) / all_others_in_relief_outs
all_others_in_relief_whip = ((all_others_in_relief_hits + all_others_in_relief_walks) * 3) / all_others_in_relief_outs

# print(round(all_others_in_relief_era, 2)) # >>> 3.52
# print(round(all_others_in_relief_whip, 2)) # >>> 1.24

# Determining K% and BB% for Qualified Starters
qualified_starters_in_relief_strikeouts = qualified_starters_in_relief_df["p_k"].sum()
qualified_starters_in_relief_batters_faced = qualified_starters_in_relief_df["p_bfp"].sum()

qualified_starters_in_relief_k_percentage = (
    qualified_starters_in_relief_strikeouts /
    qualified_starters_in_relief_batters_faced
) * 100
# print(round(qualified_starters_in_relief_k_percentage, 2)) # >>> 21.49%

qualified_starters_in_relief_bb_percentage = (
    qualified_starters_in_relief_walks /
    qualified_starters_in_relief_batters_faced
) * 100
# print(round(qualified_starters_in_relief_bb_percentage)) # >>> 9.76%

# Determining K% and BB% for All Other Pitchers
all_others_in_relief_strikeouts = all_others_in_relief_df["p_k"].sum()
all_others_in_relief_batters_faced = all_others_in_relief_df["p_bfp"].sum()

all_others_in_relief_k_percentage = (
    all_others_in_relief_strikeouts /
    all_others_in_relief_batters_faced
) * 100
# print(round(all_others_in_relief_k_percentage, 2)) # >>> 23.33%

all_others_in_relief_bb_percentage = (
    all_others_in_relief_walks /
    all_others_in_relief_batters_faced
) * 100
# print(round(all_others_in_relief_bb_percentage, 2)) # >>> 9.47%


# OTHER PITCHING STRATEGIES TO ANALYZE
# 1. Starters in relief
# 2. Starters pitching 100+ pitches
# 3. Bullpen Games # Maybe >= 5 Pitchers and Starter went <= 3 innings ?? 
# 4. Starters pitching on little rest # Need to calculate the date and determine what "little" rest means - Maybe 2 or less full days of rest