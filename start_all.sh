#!/bin/sh
FLOWDIR=/home/flow/TheFlow
case "$1" in
    "start")
        $FLOWDIR/Flow & >stdout.log 2>stderr.log
        echo $! >> pids
        disown
        $FLOWDIR/Equal  & >stdout.log 2>stderr.log
        echo $! >> pids
        disown
        $FLOWDIR/FFMPEG  & >stdout.log 2>stderr.log
        echo $! >> pids
        disown
        $FLOWDIR/Link & >stdout.log 2>stderr.log
        echo $! >> pids
        disown
        $FLOWDIR/Tarot & >stdout.log 2>stderr.log
        echo $! >> pids
        disown
        $FLOWDIR/Youtube & >stdout.log 2>stderr.log
        echo $! >> pids
        disown
        $FLOWDIR/Telegram & >stdout.log 2>stderr.log
        echo $! >> pids
        disown
    ;;
    "stop")
        for pid in $(cat $FLOWDIR/pids) ; do
            kill -9 $pids
        done
    ;;
esac
