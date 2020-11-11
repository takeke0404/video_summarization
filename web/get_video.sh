#!/bin/sh
youtube-dl -x --extract-audio --audio-quality 0 --audio-format wav --no-post-overwrites $1 -o "tmp/%(title)s.%(ext)s"
name=""
tmp="tmp/*"
for filename in $tmp; do
    name=("$filename")
done
ffmpeg -hide_banner -loglevel panic -i "$name" -ar 48000 -ac 1 "tmp/output.wav" </dev/null &>/dev/null
mv -f "tmp/output.wav" "$name"
name=${name##*/}
name=${name%.*}
