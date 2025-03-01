#!/bin/bash
PSQL="psql --username=freecodecamp --dbname=number_guessing -t --no-align -c"

echo "Enter your username:"
read USERNAME
if [[ -z $($PSQL "SELECT username FROM users WHERE username='$USERNAME'") ]]
then
  #Insert usuario
  INSERTED_USER=$($PSQL "INSERT INTO users(username, games_played, best_game) VALUES('$USERNAME', 0, 1000)")
  echo "Welcome, $USERNAME! It looks like this is your first time here."
  else
    #get games_played, best_games
    GAMES_PLAYED=$($PSQL "SELECT games_played FROM users WHERE username='$USERNAME'")
    BEST_GAME=$($PSQL "SELECT best_game FROM users WHERE username='$USERNAME'")
    echo "Welcome back, $USERNAME! You have played $GAMES_PLAYED games, and your best game took $BEST_GAME guesses."
fi

echo "Guess the secret number between 1 and 1000:"
SECRET_NUMBER=$((RANDOM % 1000 + 1))
NUMBER_OF_GUESSES=0

while true
do
  read GUESS
  ((NUMBER_OF_GUESSES++))
  if [[ "$GUESS" =~ ^[0-9]+$ ]]
  then
    if [[ "$GUESS" -eq $SECRET_NUMBER ]]
    then
       #get number_of_guesses and secret number
       echo "You guessed it in $NUMBER_OF_GUESSES tries. The secret number was $SECRET_NUMBER. Nice job!"
       USER_ID=$($PSQL "SELECT user_id FROM users WHERE username='$USERNAME'")
       NEW_PLAY=$($PSQL "INSERT INTO plays(user_id, secret_number, number_of_guesses) VALUES($USER_ID, $SECRET_NUMBER, $NUMBER_OF_GUESSES)")
       NEW_BEST_GAME=$($PSQL "UPDATE users SET best_game = LEAST(best_game, $NUMBER_OF_GUESSES) WHERE username='$USERNAME'")
       MORE_ONE_GAME=$($PSQL "UPDATE users SET games_played = games_played + 1 WHERE username='$USERNAME'")
       break
    elif [[ "$GUESS" -gt $SECRET_NUMBER ]]
    then
      echo "It's lower than that, guess again:"
    else
      echo "It's higher than that, guess again:"
    fi
  else
    echo "That is not an integer, guess again:"
  fi
done

