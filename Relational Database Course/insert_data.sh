#! /bin/bash

if [[ $1 == "test" ]]
then
  PSQL="psql --username=postgres --dbname=worldcuptest -t --no-align -c"
else
  PSQL="psql --username=freecodecamp --dbname=worldcup -t --no-align -c"
fi
echo $($PSQL "TRUNCATE teams, games")

# Do not change code above this line. Use the PSQL variable above to query your database.
cat games.csv | while IFS="," read YEAR ROUND WINNER OPPONENT WINNER_GOALS OPPONENT_GOALS
do
  if [[ $WINNER != "winner" ]]
  then
    #check if team has id
    TEAM_ID="$($PSQL "SELECT team_id FROM teams WHERE name='$WINNER'")"

    # if not found
    if [[ -z $TEAM_ID ]]
    then
      INSERT_GANHADOR="$($PSQL "INSERT INTO teams(name) VALUES('$WINNER')")"
      # if [[ $INSERT_GANHADOR == "INSERT 0 1" ]]
      # then
      #   echo $WINNER inserido.
      # fi
    fi
  fi

  if [[ $OPPONENT != "opponent" ]]
  then
    #check if team has id
    TEAM_ID="$($PSQL "SELECT team_id FROM teams WHERE name='$OPPONENT'")"

    if [[ -z $TEAM_ID ]]
    then
      INSERT_OPONENTE="$($PSQL "INSERT INTO teams(name) VALUES('$OPPONENT')")"
      # if [[ $INSERT_OPONENTE == "INSERT 0 1" ]]
      # then
      #   echo $OPPONENT inserido.
      # fi
    fi
  fi

  if [[ $YEAR != "year" ]]
  then
    WINNER_ID="$($PSQL "SELECT team_id FROM teams WHERE name='$WINNER'")"
    OPPONENT_ID="$($PSQL "SELECT team_id FROM teams WHERE name='$OPPONENT'")"

    if [[ -n $WINNER_ID && -n $OPPONENT_ID ]]
    then
      GAME="$($PSQL "INSERT INTO games(year, round, winner_id, opponent_id, winner_goals, opponent_goals) VALUES('$YEAR', '$ROUND', $WINNER_ID, $OPPONENT_ID, '$WINNER_GOALS', '$OPPONENT_GOALS')")" 
      echo Inserção foi $GAME
    fi
  fi

  # year,round,winner,opponent,winner_goals,opponent_goals
  # 2018,Final,France,Croatia,4,2
  #  game_id | year | round | winner_id | opponent_id | winner_goals | opponent_goals 
done