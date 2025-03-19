#! /bin/bash

PSQL="psql --username=freecodecamp --dbname=salon --tuples-only -c"

MENU(){
  echo -e "\n~~~~~ MY SALON ~~~~\n"

  if [[ -z $1 ]]
  then
    echo -e "Welcome to My Salon, how can I help you?\n"
  else
    echo -e "I could not find that service. What would you like today?"
  fi

  echo -e "1) cut\n2) color\n3) perm\n4) style\n5) trim)"
  read SERVICE_ID_SELECTED

  case $SERVICE_ID_SELECTED in
    1)
      APPOINTMENT_MENU 1
      ;;
    2)
      APPOINTMENT_MENU 2
      ;;
    3)
      APPOINTMENT_MENU 3
      ;;
    4)
      APPOINTMENT_MENU 4
      ;;
    5)
      APPOINTMENT_MENU 5
      ;;
    *)
      MENU "ERROR"
    ;;
  esac
}

APPOINTMENT_MENU(){
  SERVICE_ID_SELECTED=$1

  echo -e "\nWhat's your phone number?"
  read CUSTOMER_PHONE

  CUSTOMER_NAME=$($PSQL "SELECT name FROM customers WHERE phone='$CUSTOMER_PHONE'")
  if [[ -z $CUSTOMER_NAME ]]
  then
    echo -e "\nI don't have a record for that phone number, what's your name?"
    read CUSTOMER_NAME
    NEW_CUSTOMER_NAME=$($PSQL "INSERT INTO customers(name, phone) VALUES('$CUSTOMER_NAME','$CUSTOMER_PHONE')")
  fi

  CUSTOMER_NAME=$(echo "$CUSTOMER_NAME" | sed 's/^[ \t]*//;s/[ \t]*$//')
  SERVICE_NAME=$($PSQL "SELECT name FROM services WHERE service_id=$SERVICE_ID_SELECTED")
  SERVICE_NAME=$(echo "$SERVICE_NAME" | sed 's/^[ \t]*//;s/[ \t]*$//')
  echo -e "\nWhat time would you like your $SERVICE_NAME, $CUSTOMER_NAME?"
  read SERVICE_TIME
  
  CUSTOMER_ID=$($PSQL "SELECT customer_id FROM customers WHERE name='$CUSTOMER_NAME'")
  NEW_APPOINTMENT=$($PSQL "INSERT INTO appointments(customer_id, service_id, time) VALUES($CUSTOMER_ID, $SERVICE_ID_SELECTED, '$SERVICE_TIME')")

  if [[ NEW_APPOINTMENT ]]
  then
    echo -e "\nI have put you down for a $SERVICE_NAME at $SERVICE_TIME, $CUSTOMER_NAME."
  fi
}

MENU $1