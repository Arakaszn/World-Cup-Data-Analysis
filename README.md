# World-Cup-Data-Analysis
DATA SCIENCE PROJECT PROPOSAL

The 12th Man: Quantifying the Host Nation 
Advantage in FIFA World Cups (1930–2022)

Project Objective & Scope

• Problem Statement: This project investigates the "Home Field Advantage" 
phenomenon by comparing the performance of host nations against their historical 
averages in non-host years. Specifically, we will look at whether hosting leads to a 
statistically significant increase in win rates, goals scored, and tournament 
progression.
• Target Audience: Sports analysts, national football associations (for strategic 
planning), and urban planners interested in the sporting impact of hosting major 
events.
• Expected Outcomes: We aim to determine if hosts win at a rate higher than the 
standard 50% probability and if certain factors, like "home continent" status, further 
amplify this advantage.
Data Acquisition & Management

• Data Source: We will primarily utilize the "FIFA World Cup 1930-2022 All Match 
Dataset" from Kaggle, supplemented by the "WorldCups.csv" summary table for 
tournament-level statistics.
• Data Description: The dataset contains approximately 964 rows of match logs. 
Variables include categorical data (Home/Away Team Names, Stadium, City, Stage) 
and numerical data (Year, Home/Away Goals, Attendance).
• Storage Format: Data will be managed and merged using Pandas DataFrames to 
allow for the creation of a "is_host" boolean flag for each match
Methodology & Tools

• Proposed Analysis: We will use data aggregation to calculate the average win rate 
and goal differential for every country when they are hosts vs. when they are guests. 
We will also perform correlation analysis between home attendance and match 
outcomes.
• Technical Stack: The project will utilize Python, NumPy for numerical calculations, 
and Pandas for data wrangling.
• Visualization Plan: Using Matplotlib, we will create a grouped bar chart
comparing "Host Performance" vs. "Lifetime Average Performance" for all 17 host 
nations to highlight the performance delta.
Ethical Considerations & Bias

• Privacy & Compliance: The dataset consists of public historical sports records and 
contains no personally identifiable information (PII) regarding individual fans or 
players.
• Algorithmic Bias: We acknowledge a historical bias toward European and South 
American teams, as they have hosted most tournaments. Our analysis will 
acknowledge that "Host Advantage" might be skewed by the fact that stronger 
footballing nations are more likely to win hosting bids.
