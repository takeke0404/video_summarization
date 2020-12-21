#!/bin/sh
video_id=${1##*=}
if [ -f "./clip_position/$2.csv" ]; then
    echo "clip_position/$2.csv exists"
else
    echo "get clip_position $2"
    python -B -u -c "import get_clip_position; import sys; get_clip_position.get_clip_position(sys.argv[1],sys.argv[2])" "./videos/$2.wav" "./clips/$2.wav" 2>&1 | tee "clip_position_output/$2.txt"
    echo "end get clip_position $2"
fi
