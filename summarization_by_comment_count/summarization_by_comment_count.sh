#!/bin/sh
positions="../get_clip_position/positions/*"
for filename in $positions; do
    name=${filename##*/}
    name=${name%.*}
    python summarization_by_comment_count.py "$name"
done
echo "summarization_by_comment_count is done"
