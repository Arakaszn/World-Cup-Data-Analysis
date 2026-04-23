import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


# 1. LOAD RAW DATA
# Load the raw files directly 
matches = pd.read_csv('matches_1930_2022.csv')
world_cups = pd.read_csv('world_cup.csv')

# 2. CLEAN & STANDARDIZE
name_standardization = {'West Germany': 'Germany', 'Soviet Union': 'Russia', 'Czechoslovakia': 'Czech Republic'}
matches['home_team'] = matches['home_team'].replace(name_standardization)
matches['away_team'] = matches['away_team'].replace(name_standardization)
matches['Host'] = matches['Host'].replace(name_standardization)

core_cols = ['Year', 'Host', 'home_team', 'away_team', 'home_score', 'away_score', 'Round']
matches_clean = matches[core_cols].dropna(subset=['home_score', 'away_score'])

# 3. RESTRUCTURE & FEATURE ENGINEERING
home_teams = matches_clean[['Year', 'Host', 'home_team', 'home_score', 'away_score', 'Round']].copy()
home_teams.columns = ['Year', 'Host', 'Team', 'Goals_Scored', 'Goals_Conceded', 'Round']

away_teams = matches_clean[['Year', 'Host', 'away_team', 'away_score', 'home_score', 'Round']].copy()
away_teams.columns = ['Year', 'Host', 'Team', 'Goals_Scored', 'Goals_Conceded', 'Round']

team_matches = pd.concat([home_teams, away_teams], ignore_index=True)

# Calculate Points (3 for win, 1 for draw, 0 for loss)
team_matches['Points'] = team_matches.apply(
    lambda r: 3 if r['Goals_Scored'] > r['Goals_Conceded'] else (1 if r['Goals_Scored'] == r['Goals_Conceded'] else 0), 
    axis=1
)

# Flag Host Status
team_matches['Is_Host'] = team_matches['Team'] == team_matches['Host']

# Create Group Stage vs Knockout Stage column
team_matches['Stage'] = team_matches['Round'].apply(
    lambda x: 'Group Stage' if 'Group' in str(x) else 'Knockouts'
)

# 4. PLOT 1: THE PRESSURE INDEX 
plt.style.use('ggplot')
pressure_data = team_matches.groupby(['Stage', 'Is_Host'])['Points'].mean().reset_index()

sns.barplot(
    data=pressure_data, 
    x='Stage', 
    y='Points', 
    hue='Is_Host', 
    palette=['#bdc3c7', '#e74c3c'],
    errorbar=None
)

plt.title('The Pressure Index: Host Advantage by Tournament Stage')
plt.xlabel('Tournament Stage')
plt.ylabel('Average Points Per Match')
plt.legend(title='Is Host', labels=['Non-Host', 'Host Nation'])
plt.savefig('pressure_index.png', bbox_inches='tight')
plt.clf() # Clear plot so the next one doesn't overlap

# 5. PLOT 2: STRENGTH SCATTER
host_nations = team_matches[team_matches['Is_Host'] == True]['Team'].unique()

delta_data = []
for nation in host_nations:
    nat_data = team_matches[team_matches['Team'] == nation]
    
    host_ppm = nat_data[nat_data['Is_Host'] == True]['Points'].mean()
    non_host_ppm = nat_data[nat_data['Is_Host'] == False]['Points'].mean()
    strength = nat_data['Points'].mean()
    delta = host_ppm - non_host_ppm
    
    delta_data.append({'Team': nation, 'Strength': strength, 'Host_Delta': delta})

delta_df = pd.DataFrame(delta_data)

sns.scatterplot(data=delta_df, x='Strength', y='Host_Delta', s=100, color='#3498db')

# Add text labels to the dots
for i in range(delta_df.shape[0]):
    plt.text(
        x=delta_df.Strength[i] + 0.02, 
        y=delta_df.Host_Delta[i] + 0.02, 
        s=delta_df.Team[i], 
        fontsize=9
    )

plt.title('Does Hosting Help Good Teams More?')
plt.xlabel('Historical Strength (Lifetime Points Per Match)')
plt.ylabel('Host Performance Delta (+/- Points)')
plt.axhline(0, color='black', linestyle='--', alpha=0.5)

plt.savefig('strength_scatter.png', bbox_inches='tight')
plt.clf()

print("Success! Both plots have been generated from the raw data.")
