#!/usr/bin/env python3
import youtube_chat_replay_crawler as yc
import json
def get_comment_json(video_id,output_filename):
 s=yc.get_chat_replay_data(video_id)
 if s==[]:
     return
 with open(output_filename, mode='w') as f:
      f.write(json.dumps(s,ensure_ascii=False))
