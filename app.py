from flask import Flask, request
import psycopg2
app = Flask(__name__)
@app.route("/")
def home():
    if 'team1' in request.args:
        team_name_1 = request.args['team1']
        team_name_2 = request.args['team2']
        conn = psycopg2.connect(host="db", port=5432, dbname="world_cup", user="postgres", password="postgres")
        cur = conn.cursor()
        cur.execute("SELECT * FROM matches WHERE (home_team_name = %s AND away_team_name = %s) OR (home_team_name = %s AND away_team_name = %s)", (team_name_1, team_name_2, team_name_2, team_name_1))
        rows = cur.fetchall()
        wins = 0
        losses = 0
        draws = 0
        total_games = 0
        for row in rows:
            row_home_team = row[2]
            row_away_team = row[3]
            home_team_goals = row[4]
            away_team_goals = row[5]
            if row_home_team == team_name_1:
                if home_team_goals > away_team_goals:
                    wins += 1
                    total_games += 1
                elif home_team_goals < away_team_goals:
                    losses += 1
                    total_games += 1
                else:
                    draws += 1
                    total_games += 1
            elif row_away_team == team_name_1:
                if home_team_goals < away_team_goals:
                    wins += 1
                    total_games += 1
                elif home_team_goals > away_team_goals:
                    losses += 1
                    total_games += 1
                else:
                    draws += 1
                    total_games += 1
        if team_name_1 == team_name_2:
            return "You have entered the same team name twice. Please enter two different team names."
        elif total_games == 0:
            return "These teams have never played each other in the past"
        else:
            win_percentage = wins / total_games * 100
            loss_percentage = losses / total_games * 100
            draw_percentage = draws / total_games * 100
            return f"Total games played: {total_games} \n {team_name_1} | previous record against | {team_name_2} \n win rate: {win_percentage} % \n loss rate: {loss_percentage} % \n draw rate: {draw_percentage} %"
        cur.close()
        conn.close()
    else:
        return '''
            <form> 
                <input type="text" name="team1" placeholder="Team 1"> 
                <input type="text" name="team2" placeholder="Team 2"> 
                <button type="submit">Predict</button> 
            </form>
        '''

app.run(host="0.0.0.0", port=5000)