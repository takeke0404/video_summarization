#!/bin/sh
bash get_video.sh
bash get_comment.sh
bash get_clip_position_multiple.sh
bash speech_segmentation.sh
bash summarization_by_comment_count.sh
bash summarization_by_bert.sh
bash summarization_by_comment_count_and_bert.sh
bash plot.sh
