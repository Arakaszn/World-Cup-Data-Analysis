import pandas as pd
import numpy as np

# Load datasets
matches = pd.read_csv('matches_1930_2022.csv')
world_cups = pd.read_csv('world_cup.csv')
fifa_ranking_2022 = pd.read_csv('fifa_ranking_2022-10-06.csv')  

# Transformation: Map historical team names
name_standardization = {'West Germany': 'Germany', 'Soviet Union': 'Russia', 'Czechoslovakia': 'Czech Republic'}
matches['home_team'] = matches['home_team'].replace(name_standardization)
matches['away_team'] = matches['away_team'].replace(name_standardization)
matches['Host'] = matches['Host'].replace(name_standardization)

# Cleaning: Focus on core columns and drop missing scores
core_cols = ['Year', 'Host', 'home_team', 'away_team', 'home_score', 'away_score']
matches_clean = matches[core_cols].dropna(subset=['home_score', 'away_score'])

# Transformation: Flag if the Host is playing using NumPy 
matches_clean['Is_Host_Playing'] = np.where(
    (matches_clean['home_team'] == matches_clean['Host']) | 
    (matches_clean['away_team'] == matches_clean['Host']), 
    True, False
)

# Join Data: Merge on the 'Year' column
final_dataset = pd.merge(matches_clean, world_cups[['Year', 'Champion', 'AttendanceAvg']], on='Year', how='left')
print("Merge Successful. Cleaned rows:", len(final_dataset))

import pandas as pd
import numpy as np

# 1. Load the raw Kaggle files
matches = pd.read_csv('matches_1930_2022.csv')
world_cups = pd.read_csv('world_cup.csv')

# 2. Clean & Standardize
name_standardization = {'West Germany': 'Germany', 'Soviet Union': 'Russia', 'Czechoslovakia': 'Czech Republic'}
matches['home_team'] = matches['home_team'].replace(name_standardization)
matches['away_team'] = matches['away_team'].replace(name_standardization)
matches['Host'] = matches['Host'].replace(name_standardization)

core_cols = ['Year', 'Host', 'home_team', 'away_team', 'home_score', 'away_score']
matches_clean = matches[core_cols].dropna(subset=['home_score', 'away_score'])

# 3. Restructure to Team-Match Level
home_teams = matches_clean[['Year', 'Host', 'home_team', 'home_score', 'away_score']].copy()
home_teams.columns = ['Year', 'Host', 'Team', 'Goals_Scored', 'Goals_Conceded']

away_teams = matches_clean[['Year', 'Host', 'away_team', 'away_score', 'home_score']].copy()
away_teams.columns = ['Year', 'Host', 'Team', 'Goals_Scored', 'Goals_Conceded']

team_matches = pd.concat([home_teams, away_teams], ignore_index=True)

# 4. Feature Engineering
team_matches['Goal_Differential'] = team_matches['Goals_Scored'] - team_matches['Goals_Conceded']

def calculate_points(row):
    if row['Goals_Scored'] > row['Goals_Conceded']:
        return 3
    elif row['Goals_Scored'] == row['Goals_Conceded']:
        return 1
    else:
        return 0

team_matches['Points'] = team_matches.apply(calculate_points, axis=1)
team_matches['Is_Host'] = team_matches['Team'] == team_matches['Host']

# 5. Export the file needed for EDA
team_matches.to_csv('team_matches_enhanced.csv', index=False)
print("File 'team_matches_enhanced.csv' successfully generated!")