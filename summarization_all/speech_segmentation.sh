#!/bin/sh
positions="./videos/*"
for filename in $positions; do
    name=${filename##*/}
    name=${name%.*}
    if [ -f "./segmentation/$name.csv" ]; then
        echo "./segmentation/$name.csv exists"
    else
        python speech_segmentation.py "$name"
    fi
done
echo "speech_segmentation is done"
