import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ==========================================
# 1. LOAD & CLEAN DATA
# ==========================================
matches = pd.read_csv('matches_1930_2022.csv')

# Standardize names
name_standardization = {'West Germany': 'Germany', 'Soviet Union': 'Russia', 'Czechoslovakia': 'Czech Republic'}
matches['home_team'] = matches['home_team'].replace(name_standardization)
matches['away_team'] = matches['away_team'].replace(name_standardization)
matches['Host'] = matches['Host'].replace(name_standardization)

# Drop missing scores
core_cols = ['Year', 'Host', 'home_team', 'away_team', 'home_score', 'away_score']
matches_clean = matches[core_cols].dropna(subset=['home_score', 'away_score'])

# ==========================================
# 2. RESTRUCTURE & CALCULATE POINTS
# ==========================================
home_teams = matches_clean[['Year', 'Host', 'home_team', 'home_score', 'away_score']].copy()
home_teams.columns = ['Year', 'Host', 'Team', 'Goals_Scored', 'Goals_Conceded']

away_teams = matches_clean[['Year', 'Host', 'away_team', 'away_score', 'home_score']].copy()
away_teams.columns = ['Year', 'Host', 'Team', 'Goals_Scored', 'Goals_Conceded']

team_matches = pd.concat([home_teams, away_teams], ignore_index=True)

# Points: 3 for win, 1 for draw, 0 for loss
team_matches['Points'] = team_matches.apply(
    lambda r: 3 if r['Goals_Scored'] > r['Goals_Conceded'] else (1 if r['Goals_Scored'] == r['Goals_Conceded'] else 0), 
    axis=1
)

# Flag Host Status
team_matches['Is_Host'] = team_matches['Team'] == team_matches['Host']

# ==========================================
# 3. GENERATE THE SLIDE 2 CHART
# ==========================================
plt.style.use('ggplot')
plt.figure(figsize=(8, 6))

# Plot the data
sns.barplot(
    data=team_matches, 
    x='Is_Host', 
    y='Points', 
    errorbar=None, 
    palette=['#3498db', '#e74c3c']
)

# Add titles and labels for the presentation
plt.title('Average Match Points: Non-Host vs. Host Nations', fontsize=14, fontweight='bold')
plt.xlabel('Host Status')
plt.ylabel('Average Points per Match')
plt.xticks([0, 1], ['Non-Host (Baseline: 1.35)', 'Host Nation (2.05)'])
plt.ylim(0, 2.5) # Sets a clean Y-axis height

# Save the plot
plt.savefig('average_match_points.png', bbox_inches='tight')
plt.clf()

print("Success! 'average_match_points.png' is ready for Slide 2.")