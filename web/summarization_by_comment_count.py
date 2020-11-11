import os
import sys
import numpy as np
import json
import csv
import wave

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
clip_length=300

def main(name,video_id):
    # 読み込み
    comments_json = json.load(open('tmp/'+name+'.json', "r", encoding="UTF-8"))

    # 時刻と内容の抽出
    comments_list = []
    for comment in comments_json:
        if(time2sec(comment["time"])<0):
            continue
        comments_list.append((time2sec(comment["time"]), comment["text"]))

    n=0
    flag=True
    clip_segments = []
    while flag:
        n+=1
        # 時間当たりコメント数(5-30秒までの畳み込み和,要約の長さまで上位n件)
        comment_begin = comments_list[0][0]
        comment_end = comments_list[-1][0]
        comments_per_sec = np.zeros(comment_end - comment_begin + 1)
        for comment in comments_list:
            comments_per_sec[comment[0] - comment_begin] += 1
        comment_count = np.convolve(comments_per_sec,[2]*20+[1]*10,)[30:]
        times = np.sort(np.argpartition(comment_count, -n)[-n:])

        # コメントが多かった部分を含む音声区間を抽出
        segments = []
        with open("tmp/"+name+".csv") as f:
            prev = ("",0,0)
            for type,start,end in csv.reader(f):
                for time in times:
                    if(float(start)<=time and time<=float(end)):
                        # 検出された区間のひとつ前のnoEnergy,noise以外の区間を結合
                        segments.append(prev)
                        # 検出された区間の結合
                        segments.append((type,float(start),float(end)))
                if (type != "noEnergy" and type != "noise"):
                    prev = (type,float(start),float(end))
            segments = list(dict.fromkeys(segments))
        # 前の区間と5秒以上空いていない区間同士を結合
        segments = taple_join(segments,5)
        len=0
        for t,s,e in segments:
            len+=e-s
        if (len>clip_length):
            flag=False
        else:
            clip_segments=segments

    print(clip_segments)
    with open('summarization_by_comment_count/'+video_id+".csv",mode='w') as f:
        print(*video_id, sep='',file=f)
        for type,start,end in clip_segments:
            print(*(round(start,2),round(end,2)), sep=',', file=f)
    return

def time2sec(time_str):
    sec = 0
    if time_str.startswith("-"):
        ts = time_str[1 : ]
        mul = - 1
    else:
        ts = time_str
        mul = 1
    l = ts.split(":")
    for a in l[::-1]:
        sec += int(a) * mul
        mul *= 60
    return sec

def taple_join(taple,n):
    result = [taple[0]]
    for typet,st,et in taple:
        typer,sr,er = result[-1]
        if (er+n>=st):
            result[-1]=(typer,sr,et)
        else:
            result.append((typet,st,et))
    return result

if __name__ == "__main__":
    args = sys.argv
    main(args[1],args[2])
