#!/bin/sh
positions="./videos/*"
for filename in $positions; do
    name=${filename##*/}
    name=${name%.*}
    python plot.py "$name"
done
echo "speech_segmentation is done"
