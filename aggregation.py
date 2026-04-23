import pandas as pd
import numpy as np

# 1. LOAD RAW DATA & CLEAN ON THE FLY
matches = pd.read_csv('matches_1930_2022.csv')

# Standardize historical names
name_standardization = {'West Germany': 'Germany', 'Soviet Union': 'Russia', 'Czechoslovakia': 'Czech Republic'}
matches['home_team'] = matches['home_team'].replace(name_standardization)
matches['away_team'] = matches['away_team'].replace(name_standardization)
matches['Host'] = matches['Host'].replace(name_standardization)

# Drop missing scores
core_cols = ['Year', 'Host', 'home_team', 'away_team', 'home_score', 'away_score']
matches_clean = matches[core_cols].dropna(subset=['home_score', 'away_score'])

# 2. RESTRUCTURE TO TEAM-MATCH LEVEL
home_teams = matches_clean[['Year', 'Host', 'home_team', 'home_score', 'away_score']].copy()
home_teams.columns = ['Year', 'Host', 'Team', 'Goals_Scored', 'Goals_Conceded']

away_teams = matches_clean[['Year', 'Host', 'away_team', 'away_score', 'home_score']].copy()
away_teams.columns = ['Year', 'Host', 'Team', 'Goals_Scored', 'Goals_Conceded']

team_matches = pd.concat([home_teams, away_teams], ignore_index=True)

# Calculate Points and Host Status
team_matches['Points'] = team_matches.apply(
    lambda r: 3 if r['Goals_Scored'] > r['Goals_Conceded'] else (1 if r['Goals_Scored'] == r['Goals_Conceded'] else 0), 
    axis=1
)
team_matches['Is_Host'] = team_matches['Team'] == team_matches['Host']

# 3. CONTINENT MAPPING
continent_map = {
    'Uruguay': 'South America', 'Italy': 'Europe', 'France': 'Europe', 'Brazil': 'South America', 
    'Switzerland': 'Europe', 'Sweden': 'Europe', 'Chile': 'South America', 'England': 'Europe', 
    'Mexico': 'North America', 'Germany': 'Europe', 'Argentina': 'South America', 'Spain': 'Europe', 
    'United States': 'North America', 'South Africa': 'Africa', 'Russia': 'Europe', 
    'Qatar': 'Asia', 'South Korea': 'Asia', 'Japan': 'Asia'
}

team_matches['Host_Continent'] = team_matches['Host'].map(continent_map)
team_matches['Team_Continent'] = team_matches['Team'].map(continent_map)

# Flag if the team is playing on their home continent
team_matches['Same_Continent'] = team_matches['Host_Continent'] == team_matches['Team_Continent']

mapped_teams = team_matches.dropna(subset=['Team_Continent', 'Host_Continent']).copy()

# 4. DATA AGGREGATION (Ch. 10)
continent_agg = mapped_teams.groupby(['Same_Continent', 'Is_Host'])['Points'].mean().unstack()

print("--- Average Points by Continental Proximity ---")
print(continent_agg)