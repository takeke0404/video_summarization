#!/bin/sh
positions="../get_clip_position/positions/*"
for filename in $positions; do
    name=${filename##*/}
    name=${name%.*}
    python make_bert_data.py "../get_video/comments/$name.json"
done
echo "make_bert_data is done"
