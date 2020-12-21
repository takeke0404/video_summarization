#!/bin/sh
positions="../get_clip_position/positions/*"
for filename in $positions; do
    name=${filename##*/}
    name=${name%.*}
    python make_data.py "$name"
    python predict.py "$name"
    python make_summarization.py "$name"
done
echo "summarization_by_bert is done"
