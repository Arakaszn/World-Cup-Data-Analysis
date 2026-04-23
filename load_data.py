import pandas as pd
import numpy as np

# Load the raw match logs
fifa_ranking_2022 = pd.read_csv('fifa_ranking_2022-10-06.csv') 
matches = pd.read_csv('matches_1930_2022.csv')
world_cups = pd.read_csv('world_cup.csv')

# Clean: Drop rows with missing match scores
matches_clean = matches.dropna(subset=['home_score', 'away_score'])

# Transform: Create a boolean flag for host matches
matches_clean['Is_Host_Playing'] = np.where(
    (matches_clean['home_team'] == matches_clean['Host']) | 
    (matches_clean['away_team'] == matches_clean['Host']), 
    True, False
)

# Join: Merge tournament-wide data (Attendance and Champion)
final_dataset = pd.merge(matches_clean, world_cups[['Year', 'Champion', 'AttendanceAvg']], on='Year', how='left')
print(final_dataset)


 