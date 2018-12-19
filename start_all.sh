#!/bin/bash

FLOWDIR=/home/flow/TheFlow

function start {
	$FLOWDIR/Flow >>$FLOWDIR/stdout.log 2>>$FLOWDIR/stderr.log &
        echo $! > $FLOWDIR/pids
#        disown
        $FLOWDIR/Equal.py >>$FLOWDIR/stdout.log 2>>$FLOWDIR/stderr.log &
        echo $! >> $FLOWDIR/pids
#        disown
        $FLOWDIR/FFMPEG.py >>$FLOWDIR/stdout.log 2>>$FLOWDIR/stderr.log &
        echo $! >> $FLOWDIR/pids
#        disown
        $FLOWDIR/Link.py >>$FLOWDIR/stdout.log 2>>$FLOWDIR/stderr.log &
        echo $! >> $FLOWDIR/pids
#        disown
        $FLOWDIR/Tarot.py >>$FLOWDIR/stdout.log 2>>$FLOWDIR/stderr.log &
        echo $! >> $FLOWDIR/pids
#        disown
        $FLOWDIR/Youtube.py >>$FLOWDIR/stdout.log 2>>$FLOWDIR/stderr.log &
        echo $! >> $FLOWDIR/pids
#        disown
        $FLOWDIR/Telegram.py >>$FLOWDIR/stdout.log 2>>$FLOWDIR/stderr.log &
        echo $! >> $FLOWDIR/pids
#        disown
}

function stop {
	for pid in $(cat $FLOWDIR/pids) ; do
            kill -9 $pid
        done
        rm $FLOWDIR/pids
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
