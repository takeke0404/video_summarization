import json
import os
import sys
import csv

def main(comment_file):
    print("LOAD", comment_file)
    comments_json = json.load(open(comment_file, "r", encoding="UTF-8"))
    comment_file_name = os.path.splitext(os.path.basename(comment_file))[0]

    # 時刻と内容の抽出
    comments_list = []
    for comment in comments_json:
        comments_list.append((time2sec(comment["time"]), comment["text"]))

    # 切り抜き動画の範囲のコメントとそれ以外の範囲のコメントに分類
    clip_comment = []
    ignore_comment = []
    with open("../get_clip_position/positions/"+comment_file_name+".csv") as f:
        for row in csv.reader(f):
            a,b = row
            for time,text in comments_list:
                if( int(int(a)/48000)+10<=time and time<=int(int(b)/48000)+10 ):
                    clip_comment.append((time,text))

    comments = []
    for time,text in comments_list:
        if( (time,text) in clip_comment ):
            comments.append((time,text,1))
        elif( (time,text) in ignore_comment ):
            continue
        else:
            comments.append((time,text,0))

    data = []
    with open("../speech_segmentation/segmentation/"+comment_file_name+".csv") as f:
        for type,start,end in csv.reader(f):
            data.append(("noEnergy",0,0,"",None))
            pre = None
            for time,text,is_clip in comments:
                if( float(start)+10<time and time<float(end)+10 ):
                    if (pre != None and pre != is_clip):
                        data.append((type,start,end,text.replace(',','').replace("　",""),is_clip))
                        pre = is_clip
                    else:
                        a,s,e,t,b = data.pop(-1)
                        t += text.replace(',','').replace("　","")
                        b = is_clip
                        pre = b
                        data.append((type,start,end,t,b))

    with open('comments/'+comment_file_name+".csv",mode='w') as f:
        for row in data:
            t,s,e,a,b = row
            if (b!=None):
                print(*row, sep=',', file=f)

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

if __name__ == "__main__":
    args = sys.argv
    main(args[1])
