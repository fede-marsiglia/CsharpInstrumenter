#!/usr/bin/env bash
ADB=adb.exe
SLEEP=15
DEVICE=ea9a0d2b1e0f29d4
PROCESS_NAME="net.mattiascibien.openglsimplecrasher"

$ADB -s $DEVICE logcat -c
RESULT=`$ADB -s $DEVICE shell ps | grep $PROCESS_NAME | wc -l`
while [ $RESULT -eq 1 ]
do 
	echo 'Process is running OK!'
    sleep $SLEEP
    RESULT=`$ADB -s $DEVICE shell ps | grep $PROCESS_NAME | wc -l`
done

echo 'Process is not running dumping logcats'
$ADB -s $DEVICE logcat > log_`date +"%Y_%m_%d_%H_%M_%S"`.txt