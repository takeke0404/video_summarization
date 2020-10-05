#!/bin/sh
positions="../get_clip_position/positions/*"
for filename in $positions; do
    name=${filename##*/}
    name=${name%.*}
    python get_clip_comment.py "../get_video/comments/$name.json"
done
echo "get_clip_comment is done"
