#!/bin/bash

cd /home/flow/TheFlow

function start {
	./Flow >>stdout.log 2>>stderr.log &
        echo $! > pids
#        disown
        ./Equal.py >>stdout.log 2>>stderr.log &
        echo $! >> pids
#        disown
        ./FFMPEG.py >>stdout.log 2>>stderr.log &
        echo $! >> pids
#        disown
        ./Link.py >>stdout.log 2>>stderr.log &
        echo $! >> pids
#        disown
        ./Tarot.py >>stdout.log 2>>stderr.log &
        echo $! >> pids
#        disown
        ./Youtube.py >>stdout.log 2>>stderr.log &
        echo $! >> pids
#        disown
        ./Telegram.py >>stdout.log 2>>stderr.log &
        echo $! >> pids
#        disown
}

function stop {
	for pid in $(cat pids) ; do
            kill -9 $pid
        done
        rm pids
}

case "$1" in
    "start")
	start
        exit 0
    ;;
    "stop")
	stop
        exit 0
    ;;
    "restart")
	stop
	start
        exit 0
    ;;
esac

stop
start
exit 0
