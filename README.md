# World Cup Match Predictor

This project predicts the outcome of a match between two nations based on their historical head-to-head record in FIFA World Cup matches (1930–2014). Given two team names, it looks up every past match between them and reports the win/draw/loss percentage for the first team.

Available both as a command-line tool and as a Flask web app.

## Built With
- Python
- Flask
- PostgreSQL
- psycopg2
- Docker (Dev Containers)

## Setup

1. Install [Docker](https://www.docker.com/) and [VS Code](https://code.visualstudio.com/) with the **Dev Containers** extension.
2. Clone this repository and open the folder in VS Code.
3. Open the Command Palette (`Cmd+Shift+P`) and run **Dev Containers: Reopen in Container**. This builds a Python + PostgreSQL environment automatically, and installs Flask, psycopg2, and pandas.
4. Once inside the container, connect to the database:
```bash
   psql -h db -U postgres -d world_cup
```
   (password: `postgres`)
5. Create the tables:
```sql
   \i setup.sql
   \i staging.sql
```
6. Load the match data:
```sql
   \copy matches_staging FROM '/workspace/WorldCupMatches.csv' WITH (FORMAT csv, HEADER true);
```
   Then populate the real `matches` table:
```sql
   INSERT INTO matches (match_id, year, home_team_name, away_team_name, home_team_goals, away_team_goals)
   SELECT match_id, year, home_team_name, away_team_name, home_team_goals, away_team_goals
   FROM matches_staging;
```

## Usage

### Command Line
```bash
python3 predict.py
```
You'll be prompted to enter two team names (case-insensitive). Example:

Enter the first team name: france
Enter the second team name: mexico
win rate: 50.0 %
loss rate: 25.0 %
draw rate: 25.0 %


### Web App
```bash
python3 app.py
```
Then open `http://localhost:5000` in your browser. Enter two team names in the form and submit to see the head-to-head prediction.

Both versions handle edge cases gracefully — if the two teams have never played each other, or if the same team is entered twice, you'll get a clear message instead of a crash.

## Data Source
[WorldCupMatches.csv](https://www.kaggle.com/datasets/anairamcosta/worldcupmatches) — FIFA World Cup match data, 1930–2014, via Kaggle.

## Possible Future Improvements
- Handle typos/unknown team names distinctly from "never played"
- Weight more recent matches more heavily in the prediction
- Expand dataset to include matches after 2014
- Deploy the web app so it's publicly accessible