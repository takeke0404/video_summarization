#!/bin/sh
positions="../get_clip_position/positions/*"
for filename in $positions; do
    name=${filename##*/}
    name=${name%.*}
    python speech_segmentation.py "$name"
done
echo "speech_segmentation is done"
