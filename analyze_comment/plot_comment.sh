#!/bin/sh
positions="../get_clip_position/positions/*"
for filename in $positions; do
    name=${filename##*/}
    name=${name%.*}
    python plot_comment.py "../get_video/comments/$name.json"
done
echo "plot_comment is done"
