#!/bin/sh
FLOWDIR=/home/flow/TheFlow
case "$1" in
    "start")
        $FLOWDIR/Flow >>stdout.log 2>>stderr.log &
        echo $! >> $FLOWDIR/pids
#        disown
        $FLOWDIR/Equal.py >>stdout.log 2>>stderr.log &
        echo $! >> $FLOWDIR/pids
#        disown
        $FLOWDIR/FFMPEG.py >>stdout.log 2>>stderr.log &
        echo $! >> $FLOWDIR/pids
#        disown
        $FLOWDIR/Link.py >>stdout.log 2>>stderr.log &
        echo $! >> $FLOWDIR/pids
#        disown
        $FLOWDIR/Tarot.py >>stdout.log 2>>stderr.log &
        echo $! >> $FLOWDIR/pids
#        disown
        $FLOWDIR/Youtube.py >>stdout.log 2>>stderr.log &
        echo $! >> $FLOWDIR/pids
#        disown
        $FLOWDIR/Telegram.py >>stdout.log 2>>stderr.log &
        echo $! >> $FLOWDIR/pids
#        disown
    ;;
    "stop")
        for pid in $(cat $FLOWDIR/pids) ; do
            kill -9 $pid
        done
        rm $FLOWDIR/pids
    ;;
esac
