#!/bin/bash
PSQL="psql --username=freecodecamp --dbname=periodic_table -t --no-align -c"
a="atomic_number"
b="symbol"
c="name"
r=""

response() {
  a=$1
  r=$2
  ELEMENT_NAME=$($PSQL "SELECT name FROM elements WHERE $a = $r")
  ELEMENT_SYMBOL=$($PSQL "SELECT symbol FROM elements WHERE $a = $r")
  ELEMENT_MASS=$($PSQL "SELECT atomic_mass FROM properties WHERE $a = $r")
  ELEMENT_TYPE_ID=$($PSQL "SELECT type_id FROM properties WHERE $a = $r")
  ELEMENT_TYPE=$($PSQL "SELECT type FROM types WHERE type_id = $ELEMENT_TYPE_ID")
  ELEMENT_MELT=$($PSQL "SELECT melting_point_celsius FROM properties WHERE $a = $r")
  ELEMENT_BOIL=$($PSQL "SELECT boiling_point_celsius FROM properties WHERE $a = $r")
  echo -e "The element with atomic number $r is $ELEMENT_NAME ($ELEMENT_SYMBOL). It's a $ELEMENT_TYPE, with a mass of $ELEMENT_MASS amu. $ELEMENT_NAME has a melting point of $ELEMENT_MELT celsius and a boiling point of $ELEMENT_BOIL celsius."
}

if [[ -z $1 ]]; then
  echo "Please provide an element as an argument."
  else
    if [[ $($PSQL "SELECT * FROM elements WHERE $a = '$1'") ]]; then
      r=$1
      response $a $r
    elif [[ $($PSQL "SELECT * FROM elements WHERE $b = '$1'") ]]; then
      r="$($PSQL "SELECT atomic_number FROM elements WHERE $b = '$1'")"
      response $a $r
    elif [[ $($PSQL "SELECT * FROM elements WHERE $c = '$1'") ]]; then
      r="$($PSQL "SELECT atomic_number FROM elements WHERE $c = '$1'")"
      response $a $r
    else
      echo "I could not find that element in the database."
    fi
fi


