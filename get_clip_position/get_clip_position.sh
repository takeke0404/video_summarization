#!/bin/sh
video_id=${1##*=}
mkdir positions
mkdir output
mkdir clips
if [ -f "./positions/$2.csv" ]; then
    echo "positions/$2.csv exists"
else
    echo "get clip_position $2"
    python -B -u -c "import get_clip_position; import sys; get_clip_position.get_clip_position(sys.argv[1],sys.argv[2])" "../get_video/videos/$2.wav" "../get_video/clips/$2.wav" 2>&1 | tee "output/$2.txt"
    chmod 777 "output/$2.txt"
    chmod 777 "positions/$2.csv"
    chmod 777 "clips/$2.wav"
    echo "end get clip_position $2"
fi
