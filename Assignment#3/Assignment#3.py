import pandas as pd
import random
import sqlite3

#Question #1: Create a notebook that data engineers can use to generate dummy data

#Static Parameters
Teams_total = 20
Matches_total = 200

#List of names for the Team naming
Names = pd.read_csv("English_Names.csv")

#Convert the DataFrame into list 
List_Names = Names.stack().tolist()

#Name Randomizer and add the Team on their name
def Team_names_Randomizer():
    Random_Names=random.choice(List_Names)
    return f"Team {Random_Names}"

#Choose 20 Names for the Team Names
Team_Names = set() #no identical names 
while len(Team_Names) < Teams_total:
    Chosen_names = Team_names_Randomizer()
    Team_Names.add(Chosen_names)   

#Adding Unique Index to team names and converting the List into DataFrame
Teams=[]
for i, name in enumerate(Team_Names):
    Teams.append({'ID': i+1, 'Team': name})

#Convert the list into DataFrame
Teams_df = pd.DataFrame(Teams)

#Choosing a Winner and Loser randomly per match
Matches=[]
while len(Matches) < Matches_total:
    Team_A, Team_B = random.sample(range(1, Teams_total+1), 2) #Random Pairing
    Winner_ID = random.choice([Team_A, Team_B]) #Chooses a winner randomly
    Loser_ID = Team_A if Winner_ID == Team_B else Team_B #The unchosen becomes the loser
        
    Matches.append({'Winner_ID': Winner_ID,'Loser_ID': Loser_ID})

#Convert the list into DataFrame
Matches_df = pd.DataFrame(Matches)

#Saving both DataFrame into CSV files
Teams_df.to_csv('Teams.csv', index=False)
Matches_df.to_csv('Matches.csv', index=False)

# Question #2: Using SQL, tell me the top 10 teams by wins and their total number of wins 
# for the 2023 season given the tables described in Programming Question 1. 

#Creating a SQL database using SQLite3
database = sqlite3.connect('Team_Match.db')

#Importing the data from Question #1 into the database
Teams_df.to_sql("Teams", database, if_exists="replace", index=False)
Matches_df.to_sql("Matches", database, if_exists="replace", index=False)

#SQL Query to get the top 10 teams by wins
query = '''
SELECT name.Team, COUNT(matches.Winner_ID) AS Wins
FROM Matches matches
JOIN Teams name ON matches.Winner_ID = name.ID
GROUP BY name.Team
ORDER BY Wins DESC
LIMIT 10;
'''
# Execute the query and fetch results
Top_teams = pd.read_sql_query(query, database)  # Execute the SQL query and store results in a DataFrame
Top_teams.index += 1

# Display the top 10 teams by wins
print("Top 10 Sport Teams for the 2023 Season")
print(Top_teams)

# Close the database connection
database.close()

