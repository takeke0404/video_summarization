import os
import sys
import numpy as np
import json
import csv
import wave

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
clip_length=300

def main(name):
    predict=[]
    with open('./predict_result/'+name+'.csv') as f:
        for t,s,e,a,b in csv.reader(f):
            predict.append([float(s),float(e),float(a),float(b)])

    # 読み込み
    comments_json = json.load(open('./comments/'+name+'.json', "r", encoding="UTF-8"))

    # 時刻と内容の抽出
    comments_list = []
    for comment in comments_json:
        if(time2sec(comment["time"])<0):
            continue
        comments_list.append((time2sec(comment["time"]), comment["text"]))

    # 時間当たりコメント数(30秒までの畳み込み和)
    comment_begin = comments_list[0][0]
    comment_end = comments_list[-1][0]
    comments_per_sec = np.zeros(comment_end - comment_begin + 1)
    for comment in comments_list:
        comments_per_sec[comment[0] - comment_begin] += 1
    comment_count = np.convolve(comments_per_sec,[2]*20+[1]*10,)[30:]

    seg=[]
    with open("./segmentation/"+name+".csv") as f:
        for row in csv.reader(f):
            seg.append(row)

    m=np.percentile(predict,q=95,axis=0)[3]
    print(m)
    n=0
    pre_len=0
    flag=True
    clip_segments = []
    while flag:
        n+=1
        if( len(comment_count)<n ):
            break
        # 時間当たりコメント数(30秒までの畳み込み和,要約の長さまで上位n件)
        time = np.argpartition(comment_count, -n)[-n:]
        time = time[0]

        # コメントが多かった部分を含む音声区間を抽出
        prev = ("",0,0)
        for type,start,end in seg:
            if(float(start)<=time and time<=float(end)):
                x=0
                for s,e,a,b in predict:
                    if(float(e)==float(end)):
                        x=b
                if( x<m ):
                    break
                # 検出された区間のひとつ前のnoEnergy,noise以外の区間を結合
                clip_segments.append(prev)
                # 検出された区間の結合
                clip_segments.append((type,float(start),float(end)))
                break
            if (type != "noEnergy" and type != "noise"):
                prev = (type,float(start),float(end))
        clip_segments = list(dict.fromkeys(clip_segments))
        clip_segments.sort(key=lambda x: x[1])
        if( len(clip_segments)==0 ):
            continue
        # 前の区間と5秒以上空いていない区間同士を結合
        clip_segments = taple_join(clip_segments,5)
        length=0
        for t,s,e in clip_segments:
            if(e-s<5):
                clip_segments.remove((t,s,e))
            else:
                length+=e-s
        if (length>clip_length):
            flag=False
        else:
            if(pre_len!=len(clip_segments)):
                print(str(int(length/clip_length*100))+"/100")
                pre_len=len(clip_segments)
    print(clip_segments)
    output_comment(name,clip_segments,comments_list)
    # urlを先頭につけてcsvで書き出し
    url=""
    with open('./name_list.txt') as f:
        for video_url,video_name in csv.reader(f):
            if(video_name==name):
                url=video_url
    with open('result_by_comment_count_and_bert/'+name+".csv",mode='w') as f:
        print(*url, sep='',file=f)
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
        if(sr<=st and et<=er):
            result[-1]=(typer,sr,er)
        elif(er+n>=st):
            result[-1]=(typer,sr,et)
        else:
            result.append((typet,st,et))
    return result

def output_comment(name,clip_segments,comments_list):
    #  範囲のコメントをファイル出力
    clip_comment = []
    for type,start,end in clip_segments:
        t=""
        for comment in comments_list:
            time,text = comment
            if( start+10<time and time<end+10 ):
                t+=text.replace(',','').replace("　","")
        clip_comment.append(t)
    with open('comments_by_comment_count_and_bert/'+name+".txt",mode='w') as f:
        for row in clip_comment:
            print(*row, sep='', file=f)
    return

if __name__ == "__main__":
    args = sys.argv
    main(args[1])
