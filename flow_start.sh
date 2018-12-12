#!/bin/sh

FLOWPATH=/home/flow/TheFlow

case $1 in
  start)
    screen -d -S flow -m sh -c $FLOWPATH/Flow
    screen -d -S telegram -m sh -c $FLOWPATH/Telegram.py
    screen -d -S equal -m sh -c $FLOWPATH/Equal.py
    screen -d -S tarot -m sh -c $FLOWPATH/Tarot.py
  ;;
  stop)
    screen -X -S flow kill
    screen -X -S telegram kill
    screen -X -S equal kill
    screen -X -S tarot kill
  ;;
esac
